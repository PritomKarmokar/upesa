from typing import Optional

from django.conf import settings
from django.utils import timezone
from django.db import models, transaction, IntegrityError
from django.contrib.auth.hashers import make_password, check_password

from applibs.logger import get_logger
from applibs.helpers import generate_new_ulid
from applibs.choice_fields import UserType, StatusType

from wallets.exceptions import DuplicateUserWalletException

logger = get_logger(__name__)

class WalletUserManager(models.Manager):

    def check_wallet_exists(self, mobile_no: str) -> bool:
        logger.info({"step": "check_wallet_exists"})
        exists = self.filter(mobile_no=mobile_no).exists()
        if not exists:
            logger.info({"message": "no existing wallet found with this mobile no."})
            return False

        return True

    def fetch_active_user(self, mobile_no: str) -> Optional["WalletUser"]:
        logger.info({"step": "fetch_active_user"})
        try:
            return self.get(mobile_no=mobile_no, status=StatusType.ACTIVE)
        except self.model.DoesNotExist:
            logger.error({"message": f"wallet user with the following {mobile_no} does not exist"})
            return None

    def fetch_active_user_by_id(self, user_id: str) -> Optional["WalletUser"]:
        logger.info({"step": "fetch_wallet_by_id"})
        try:
            return self.get(id=user_id, status=StatusType.ACTIVE)
        except self.model.DoesNotExist:
            logger.error({"message": f"wallet user with the following {user_id} id does not exist"})
            return None

    def create_new_user(
            self,
            username: str,
            mobile_no: str,
            user_type: str,
            password: str
    ) -> Optional["WalletUser"]:

        logger.info({"step": "create_new_user"})
        try:
            with transaction.atomic():
                return self.create(
                    username=username,
                    mobile_no=mobile_no,
                    user_type=user_type,
                    password_hash=make_password(password)
                )
        except IntegrityError as e:
            logger.error({
                "message": "error occurred while creating new wallet",
                "error": str(e)
            })
            raise DuplicateUserWalletException("User Wallet already exists with this phone number.")
        except Exception as e:
            logger.error({
                "message": "unexpected error occurred while creating new wallet",
                "error": str(e)
            })
            return None

class WalletUser(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_new_ulid, editable=False)

    username = models.CharField(max_length=55)
    mobile_no = models.CharField(max_length=16, unique=True)
    user_type = models.CharField(max_length=10, choices=UserType, default=UserType.CUSTOMER)
    status = models.CharField(max_length=10, choices=StatusType, default=StatusType.ACTIVE)

    password_hash = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_login = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)

    # Incremented on logout to invalidate all previously issued tokens
    token_version = models.PositiveIntegerField(default=0)

    objects = WalletUserManager()

    class Meta:
        db_table = "wallet_users"
        verbose_name = "WalletUser"
        verbose_name_plural = "WalletUsers"

    def __str__(self) -> str:
        return f"{self.username} {self.user_type} {self.status}"

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == StatusType.ACTIVE

    @property
    def is_locked(self) -> bool:
        return self.locked_until is not None and self.locked_until > timezone.now()

    def set_password(self, raw_password: str):
        self.password_hash = make_password(raw_password)


    def check_password(self, password: str) -> bool:
        return check_password(password, self.password_hash)

    def register_successful_login_attempt(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.token_version += 1
        self.last_login = timezone.now()
        self.save(update_fields=["failed_login_attempts", "locked_until", "token_version", "last_login"])

    def register_failed_login_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
            self.locked_until = timezone.now() + settings.LOCK_DURATION_TILL_MINUTES
        self.save(update_fields=["failed_login_attempts", "locked_until"])

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    def perform_logout_operation(self) -> bool:
        self.token_version += 1
        self.updated_at = timezone.now()
        self.save(update_fields=["token_version", "updated_at"])
        return True