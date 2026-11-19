from django.urls import path

from wallets.views import (
    CreateWalletView,
    CreateWalletUserAPIView
)

api_base_url = "api/v1"

api_urls = [
    path(
        f"{api_base_url}/create-user/",
        CreateWalletUserAPIView.as_view(),
        name="api_v1_create_wallet_user",
    ),
    path(
        f"{api_base_url}/create-wallet/",
        CreateWalletView.as_view(),
        name="api_v1_create_wallet",
    )
]

urlpatterns = api_urls