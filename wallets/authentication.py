from typing import Optional

from django.db import transaction

from applibs.logger import get_logger
from applibs.choice_fields import StatusType

from wallets.models import WalletUser
from wallets.exceptions import InvalidCredentials, AccountLocked, AccountNotActive

logger = get_logger(__name__)

def authenticate_user(mobile_no: str, password: str) -> WalletUser:
    with transaction.atomic():
        user = (
            WalletUser.objects.
            select_for_update().
            filter(mobile_no=mobile_no).
            first()
        )

        if user is None:
            raise InvalidCredentials()

        if user.is_locked:
            raise AccountLocked()

        if not user.check_password(password):
            user.register_failed_login_attempts()
            raise InvalidCredentials()

        if user.status != StatusType.ACTIVE:
            raise AccountNotActive()

        user.register_successful_login_attempt()
        return user


