from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from applibs.logger import get_logger
from applibs.response import error_response, success_response

from wallets.models import WalletUser
from wallets.serializers import CreateWalletSerializer

logger = get_logger(__name__)

class CreateWalletAPIView(APIView):
    serializer_class = CreateWalletSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            logger.error(f"Invalid data: {serializer.errors}")
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

        new_wallet = WalletUser.objects.create_new_wallet(
            full_name=data["full_name"],
            mobile_no=data["mobile_no"],
            role=data.get("role", ""),
            pin=data["pin"],
        )
        if not new_wallet:
            return error_response(
                code="WALLET_CREATION_FAILED", message="Wallet creation failed.",
                status_code=status.HTTP_409_CONFLICT
            )

        response_data = {
            "wallet_id": new_wallet.id,
            "full_name": new_wallet.full_name,
            "created_at": new_wallet.created_at,
        }
        return success_response(
            data=response_data, status_code=status.HTTP_201_CREATED
        )