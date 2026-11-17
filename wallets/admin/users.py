from django.contrib import admin

from wallets.models import WalletUser

@admin.register(WalletUser)
class WalletUserAdmin(admin.ModelAdmin):
    show_full_result_count = False
    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    list_display = (
        "id",
        "username",
        "mobile_no",
        "user_type",
        "status",
        "created_at",
    )

    list_filter = (
        "user_type",
        "status",
        "created_at",
    )

    search_fields = (
        "=id",
        "=mobile_no",
        "username",
    )

    readonly_fields = (
        "id",
        "password_hash",
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only restrict columns on the changelist; the edit/detail view needs all fields.
        if request.resolver_match and request.resolver_match.url_name.endswith("_changelist"):
            return qs.only(*self.list_display)
        return qs

    fieldsets = (
        (
            "User Details",
            {
                "fields": (
                    "id",
                    "username",
                    "mobile_no",
                )
            },
        ),
        (
            "Type & Status",
            {
                "fields": (
                    "user_type",
                    "status",
                )
            },
        ),
        (
            "Security",
            {
                "classes": ("collapse",),
                "fields": ("password_hash",),
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