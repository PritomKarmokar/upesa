from django.urls import path

api_base_url = "api/v1"

from wallets.views import CreateWalletAPIView

api_urls = [
    path(
        f"{api_base_url}/create-wallet/",
        CreateWalletAPIView.as_view(),
        name="api_v1_create_wallet",
    )
]

urlpatterns = api_urls