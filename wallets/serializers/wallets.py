from rest_framework import serializers

from applibs.helpers import clean_mobile_no
from applibs.validators import is_valid_mobile_no

class CreateWalletSerializer(serializers.Serializer):
    full_name = serializers.CharField(min_length=4, max_length=255)
    mobile_no = serializers.CharField(min_length=10, max_length=16)
    pin = serializers.CharField(min_length=4, max_length=8)

    @staticmethod
    def _check_mobile_no(value: str) -> str:
        if not is_valid_mobile_no(value):
            raise serializers.ValidationError(code="invalid mobile no format")

        value = clean_mobile_no(value)
        return value

    def validate(self, attrs: dict) -> dict:
        attrs["mobile_no"] = self._check_mobile_no(attrs["mobile_no"])
        return attrs