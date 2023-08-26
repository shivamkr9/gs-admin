import re
from django.contrib.auth import (
    get_user_model,
)


from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "password", "password2", "name", "mobile"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        read_only_fields = ["id"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        mobile = attrs.get("mobile")
        if password and password2 and password != password2:
            raise serializers.ValidationError(
                "Passwoed and confirm Password dosen't match"
            )
        if not re.match(r"^[6-9]\d{9}$", str(mobile)):
            raise serializers.ValidationError("Mobile number is not valid")
        attrs.pop("password2")
        return attrs

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializerForUserOnly(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "mobile"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        if not re.match(r"^[6-9]\d{9}$", str(mobile)):
            raise serializers.ValidationError("Mobile number is not valid")
        return



class UserSerializerForAdmin(UserSerializerForUserOnly):
    """Serializer for the user object."""

    class Meta(UserSerializerForUserOnly.Meta):
        fields = UserSerializerForUserOnly.Meta.fields + [
            "is_active",
            "is_admin",
        ]

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        if not re.match(r"^[6-9]\d{9}$", str(mobile)):
            raise serializers.ValidationError("Mobile number is not valid")
        return attrs


