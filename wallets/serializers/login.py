from rest_framework import serializers

from applibs.helpers import clean_mobile_no
from applibs.validators import is_valid_mobile_no

class LoginSerializer(serializers.Serializer):
    mobile_no = serializers.CharField(min_length=11, max_length=16)
    password = serializers.CharField(min_length=8, max_length=255, write_only=True, trim_whitespace=False)

    @staticmethod
    def _check_mobile_no(value: str) -> str:
        if not is_valid_mobile_no(value):
            raise serializers.ValidationError(code="invalid_mobile_no_format")

        value = clean_mobile_no(value)
        return value

    def validate(self, attrs: dict) -> dict:
        attrs["mobile_no"] = self._check_mobile_no(attrs["mobile_no"])
        return attrs