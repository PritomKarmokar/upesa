from rest_framework import serializers

from applibs.choice_fields import WalletType

class CreateWalletSerializer(serializers.Serializer):
    # user_id = serializers.CharField()
    wallet_type = serializers.ChoiceField(choices=WalletType.choices, default=WalletType.CUSTOMER)