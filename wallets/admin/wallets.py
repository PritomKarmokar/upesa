from django.contrib import admin

from wallets.models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    show_full_result_count = False
    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    raw_id_fields = ("wallet_user",)

    list_display = (
        "id",
        "wallet_type",
        "currency",
        "status",
        "ledger_balance",
        "held_balance",
        "available_balance",
        "created_at",
    )

    list_filter = (
        "wallet_type",
        "currency",
        "status",
        "created_at",
    )

    search_fields = (
        "=id",
        "=wallet_user__id",
        "=wallet_user__mobile_no",
    )

    readonly_fields = (
        "id",
        "ledger_balance",
        "held_balance",
        "available_balance",
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.resolver_match and request.resolver_match.url_name.endswith("_changelist"):
            return qs.only(*self.list_display)
        return qs

    fieldsets = (
        (
            "Wallet Information",
            {
                "fields": (
                    "id",
                    "wallet_user",
                    "wallet_type",
                    "currency",
                    "status",
                )
            },
        ),
        (
            "Balance Information",
            {
                "fields": (
                    "ledger_balance",
                    "held_balance",
                    "available_balance",
                )
            },
        ),
        (
            "Timestamps Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

