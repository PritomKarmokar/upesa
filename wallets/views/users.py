from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from applibs.logger import get_logger
from applibs.response import error_response, success_response

from wallets.models import WalletUser
from wallets.exceptions import DuplicateWalletException
from wallets.serializers import CreateWalletUserSerializer

logger = get_logger(__name__)

class CreateWalletUserAPIView(APIView):
    serializer_class = CreateWalletUserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.error(f"invalid serializer data: {serializer.errors}")
            return error_response(
                code="INVALID_DATA", message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        wallet_exists = WalletUser.objects.check_wallet_exists(mobile_no=data["mobile_no"])
        if wallet_exists:
            return error_response(
                code="DUPLICATE_WALLET", message="Wallet already exists with this phone number.",
                status_code=status.HTTP_409_CONFLICT
            )

        try:
            new_user = WalletUser.objects.create_new_user(
                username=data["username"], mobile_no=data["mobile_no"], user_type=data["user_type"], password=data["password"]
            )
        except DuplicateWalletException:
            return error_response(
                code="DUPLICATE_WALLET", message="Wallet already exists with this phone number.",
                status_code=status.HTTP_409_CONFLICT
            )

        if new_user is None:
            return error_response(
                code="WALLET_CREATION_FAILED", message="Wallet creation failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = {
            "user_id": new_user.id,
            "user_type": new_user.user_type,
            "created_at": new_user.created_at,
        }
        return success_response(
            data=response_data, status_code=status.HTTP_201_CREATED
        )