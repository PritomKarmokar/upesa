from typing import Optional

from django.db.models import Q
from django.db import models, transaction, IntegrityError

from applibs.logger import get_logger
from applibs.helpers import generate_new_ulid
from applibs.choice_fields import StatusType, WalletType, CurrencyType

from wallets.models import WalletUser
from wallets.exceptions import DuplicateWalletException

logger = get_logger(__name__)

class WalletManager(models.Manager):

    def create_new_wallet(
            self,
            wallet_user: WalletUser,
            wallet_type: str = WalletType.CUSTOMER,
    ) -> Optional["Wallet"]:

        logger.info({"step": "create_new_wallet"})
        try:
            with transaction.atomic():
                return self.create(wallet_user=wallet_user, wallet_type=wallet_type)
        except IntegrityError as e:
            logger.error({
                "message": "error occurred while creating new wallet",
                "error": str(e)
            })
            raise DuplicateWalletException("Wallet already exists with this user.")
        except Exception as e:
            logger.error({
                "message": "unexpected error occurred while creating new wallet",
                "error": str(e)
            })
            return None


class Wallet(models.Model):
    id = models.CharField(max_length=26, primary_key=True, default=generate_new_ulid, editable=False)

    wallet_user = models.ForeignKey(WalletUser, on_delete=models.PROTECT, related_name="wallets")
    wallet_type = models.CharField(max_length=20, choices=WalletType, default=WalletType.CUSTOMER)
    currency = models.CharField(max_length=10, choices=CurrencyType, default=CurrencyType.BDT)
    status = models.CharField(max_length=10, choices=StatusType, default=StatusType.ACTIVE)

    ledger_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    held_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    available_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WalletManager()

    class Meta:
        db_table = "wallets"
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        constraints = [
            models.UniqueConstraint(
                fields=["wallet_user", "wallet_type", "currency"],
                name="unique_wallet_per_user_type_currency"
            ),
            models.CheckConstraint(
                condition=Q(ledger_balance__gte=0),
                name="wallet_ledger_balance_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(held_balance__gte=0),
                name="wallet_held_balance_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(available_balance__gte=0),
                name="wallet_available_balance_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return f"ID: {self.id} Wallet Type: {self.wallet_type} Status: {self.status}"

