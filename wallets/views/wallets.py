from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from applibs.auth import UserAuthentication
from applibs.response import error_response, success_response

from wallets.models import WalletUser, Wallet
from wallets.serializers import CreateWalletSerializer
from wallets.exceptions import DuplicateWalletException

logger = get_logger(__name__)

class CreateWalletView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateWalletSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.error(f"invalid serializer data: {serializer.errors}")
            return error_response(
                code="INVALID_DATA", message=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        user_id = request.user.id
        active_wallet_user = WalletUser.objects.fetch_active_user_by_id(user_id=user_id)
        if not active_wallet_user:
            return error_response(
                code="INVALID_USER", message="User does not exist.", status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_wallet = Wallet.objects.create_new_wallet(wallet_user=active_wallet_user, wallet_type=data["wallet_type"])
        except DuplicateWalletException:
            return error_response(
                code="DUPLICATE_WALLET", message="Wallet already exists with this user.",
                status_code=status.HTTP_409_CONFLICT
            )

        if new_wallet is None:
            return error_response(
                code="WALLET_CREATION_FAILED", message="Wallet creation failed.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = {
            "wallet_id": new_wallet.id,
            "wallet_type": new_wallet.wallet_type,
            "created_at": new_wallet.created_at,
        }
        return success_response(
            data=response_data, status_code=status.HTTP_200_OK
        )
