from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from applibs.logger import get_logger
from wallets.models import WalletUser
from applibs.response import error_response, success_response

from wallets.serializers import LoginSerializer

logger = get_logger(__name__)

class WalletUserLoginView(APIView):
    permission_classes = []
    serializers_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializers_class(data=request.data)
        if not serializer.is_valid():
            logger.error(f"invalid serializer data: {serializer.errors}")
            return error_response(
                code="INVALID_DATA", message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        mobile_no = data["mobile_no"]
        password = data["password"]

        wallet_user = WalletUser.objects.fetch_active_user(mobile_no=mobile_no)
        if not wallet_user:
            return error_response(
                code="INVALID_CREDENTIALS", message="Invalid credentials.", status_code=status.HTTP_401_UNAUTHORIZED
            )

        valid_password = wallet_user.check_password(password)
        if not valid_password:
            return error_response(
                code="INVALID_CREDENTIALS", message="Invalid credentials.", status_code=status.HTTP_401_UNAUTHORIZED
            )

        wallet_user.update_last_login()

        refresh_token = RefreshToken.for_user(wallet_user)
        access_token = refresh_token.access_token
        response_data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "header_token": settings.JWT_AUTH_HEADER_TYPES,
            "expires_in": int(access_token.lifetime.total_seconds()),
            "token_type": "Bearer"
        }
        return success_response(
            data=response_data, status_code=status.HTTP_200_OK
        )