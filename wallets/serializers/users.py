from rest_framework import serializers

from applibs.choice_fields import UserType
from applibs.helpers import clean_mobile_no
from applibs.validators import is_valid_mobile_no

class CreateWalletUserSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=55)
    mobile_no = serializers.CharField(min_length=11, max_length=16)
    user_type = serializers.ChoiceField(choices=UserType.choices, default=UserType.CUSTOMER)
    password = serializers.CharField(min_length=8, max_length=255, write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(min_length=8, max_length=255, write_only=True, trim_whitespace=False)

    @staticmethod
    def _check_password_fields(attrs: dict) -> dict:
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(code="password_mismatch")

        attrs.pop("confirm_password")
        return attrs

    @staticmethod
    def _check_mobile_no(value: str) -> str:
        if not is_valid_mobile_no(value):
            raise serializers.ValidationError(code="invalid_mobile_no_format")

        value = clean_mobile_no(value)
        return value

    def validate(self, attrs: dict) -> dict:
        attrs = self._check_password_fields(attrs)
        attrs["mobile_no"] = self._check_mobile_no(attrs["mobile_no"])
        return attrs