from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from wallets.models import WalletUser

class UserAuthentication(JWTAuthentication):
    def get_user(self, validated_token: dict):
        user_id = validated_token.get("user_id")
        user = WalletUser.objects.fetch_active_user_by_id(user_id)
        if not user:
            raise AuthenticationFailed(
                "User not found or not active"
            )
        return user