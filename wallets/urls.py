from django.urls import path

from wallets.views import (
    CreateWalletView,
    WalletUserLoginView,
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
    ),
    path(
        f"{api_base_url}/user/login/",
        WalletUserLoginView.as_view(),
        name="api_v1_user_login",
    )
]

urlpatterns = api_urls