from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from applibs.auth import UserAuthentication
from applibs.response import error_response, success_response
from wallets.models import WalletUser


logger = get_logger(__name__)

class WalletLogoutView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user_id = request.user.id
        wallet_user = WalletUser.objects.fetch_active_user_by_id(user_id)
        if not wallet_user:
            logger.error({"message": f"user with id {user_id} does not exist."})
            return error_response(
                code="INVALID_DATA", message="Invalid request", status_code=status.HTTP_400_BAD_REQUEST
            )

        logout_success = wallet_user.perform_logout_operation()
        if not logout_success:
            return error_response(
                code="LOGOUT_FAILED", message="Logout failed.", status_code=status.HTTP_400_BAD_REQUEST
            )
        return success_response(data={"message": "Logout successful."})