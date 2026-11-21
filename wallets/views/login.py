from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from applibs.logger import get_logger
from applibs.response import error_response, success_response

from wallets.serializers import LoginSerializer
from wallets.authentication import authenticate_user
from wallets.exceptions import InvalidCredentials, AccountLocked, AccountNotActive

logger = get_logger(__name__)

class WalletUserLoginView(APIView):
    authentication_classes = []
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

        try:
            wallet_user = authenticate_user(mobile_no=mobile_no, password=password)
        except InvalidCredentials:
            return error_response(
                code="INVALID_CREDENTIALS", message="Invalid credentials.", status_code=status.HTTP_401_UNAUTHORIZED
            )
        except AccountLocked:
            return error_response(
                code="ACCOUNT_LOCKED", message="Too many failed attempts. Try again later.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )
        except AccountNotActive:
            return error_response(
                code="ACCOUNT_NOT_ACTIVE", message="Your account is not active. Contact support.",
                status_code=status.HTTP_403_FORBIDDEN,
            )


        refresh_token = RefreshToken.for_user(wallet_user)
        refresh_token["token_version"] = wallet_user.token_version  # adding token version to the refresh token
        access_token = refresh_token.access_token
        response_data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "expires_in": int(access_token.lifetime.total_seconds()),
            "token_type": settings.JWT_AUTH_HEADER_TYPES
        }
        return success_response(
            data=response_data, status_code=status.HTTP_200_OK
        )