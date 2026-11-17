from typing import Optional

from django.contrib.auth.hashers import make_password
from django.db import models, transaction, IntegrityError

from applibs.logger import get_logger
from applibs.helpers import generate_new_ulid
from applibs.choice_fields import UserType, StatusType

logger = get_logger(__name__)

class WalletUserManager(models.Manager):

    def check_wallet_exists(self, mobile_no: str) -> bool:
        logger.info({"step": "check_wallet_exists"})
        exists = self.filter(mobile_no=mobile_no).exists()
        if not exists:
            logger.info({"message": "no existing wallet found with this mobile no."})
            return False

        return True

    def create_new_wallet(
            self,
            username: str,
            mobile_no: str,
            user_type: str,
            password: str
    ) -> Optional["WalletUser"]:

        logger.info({"step": "create_new_wallet"})
        try:
            with transaction.atomic():
                return self.create(
                    username=username,
                    mobile_no=mobile_no,
                    user_type=user_type,
                    password=make_password(password)
                )
        except IntegrityError as e:
            logger.error({
                "message": "error occurred while creating new wallet",
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

    objects = WalletUserManager()

    class Meta:
        db_table = "wallet_users"
        verbose_name = "WalletUser"
        verbose_name_plural = "WalletUsers"

    def __str__(self) -> str:
        return f"{self.username} {self.user_type} {self.status}"