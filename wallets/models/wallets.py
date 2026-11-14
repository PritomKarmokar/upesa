from typing import Optional

from django.db import models, transaction, IntegrityError
from django.contrib.auth.hashers import make_password, check_password

from applibs.logger import get_logger
from applibs.helpers import generate_ulid
from applibs.choice_fields import WalletRoleType, StatusType

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
            full_name: str,
            mobile_no: str,
            pin: str,
            role: str = WalletRoleType.CUSTOMER,
    ) -> Optional["WalletUser"]:
        logger.info({"step": "create_new_wallet"})
        try:
            with transaction.atomic():
                return self.create(
                    full_name=full_name,
                    mobile_no=mobile_no,
                    role=role,
                    pin_hash=make_password(pin),
                )
        except IntegrityError as e:
            logger.error({
                "message": "wallet already exists with this mobile no.",
                "error": str(e),
            })
            return None

class WalletUser(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_ulid, editable=False)

    full_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=16, unique=True)
    pin_hash = models.CharField(max_length=255, blank=True, null=True)

    role = models.CharField(max_length=10, choices=WalletRoleType, default=WalletRoleType.CUSTOMER)
    status = models.CharField(max_length=10, choices=StatusType, default=StatusType.ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WalletUserManager()

    class Meta:
        db_table = "wallet_users"
        verbose_name = "Wallet User"
        verbose_name_plural = "Wallet Users"


    def __str__(self) -> str:
        return f"mobile_no : {self.mobile_no} status : ({self.status})"