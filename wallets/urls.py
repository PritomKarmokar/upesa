from django.urls import path

from wallets.views import CreateWalletUserAPIView

api_base_url = "api/v1"

api_urls = [
    path(
        f"{api_base_url}/create-wallet/",
        CreateWalletUserAPIView.as_view(),
        name="api_v1_create_wallet_user",
    )
]

urlpatterns = api_urls