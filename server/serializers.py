from rest_framework import serializers
from django.contrib.auth.models import User, Permission
from .models import UserProfile, CommonData


class UserSerializer(serializers.ModelSerializer):
    # ---- Inputs ----
    password     = serializers.CharField(write_only=True, required=True)
    municipios   = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of allowed municipalities in upper-case."
    )
    permissions  = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of permission *codenames* to assign to the user."
    )

    # ---- Outputs ----
    id_usuario   = serializers.IntegerField(source="id", read_only=True)
    date_joined  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    municipios_out = serializers.SerializerMethodField()
    permissions_out = serializers.SerializerMethodField()

    class Meta:
        model  = User
        # Expose everything the **client** needs (all in English):
        fields = [
            "id_usuario", "username", "first_name", "last_name", "email",
            "date_joined", "municipios", "municipios_out",
            "permissions", "permissions_out", "password",
        ]
        extra_kwargs = {"first_name": {"required": False},
                        "last_name":  {"required": False},
                        "email":      {"required": False}}

    # ---------- Helpers ----------
    def get_municipios_out(self, obj):
        try:
            return obj.profile.get_municipios_list()
        except Exception:
            return []

    def get_permissions_out(self, obj):
        return list(obj.user_permissions.values_list("codename", flat=True))

    # ---------- Create ----------
    def create(self, validated_data):
        municipios  = validated_data.pop("municipios", [])
        perms_input = validated_data.pop("permissions", [])

        # 1. Create user
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        # 2. Profile & municipalities
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if municipios:
            profile.municipios = ",".join([m.upper() for m in municipios])
            profile.save()

        # 3. Permissions
        if perms_input:
            perms = Permission.objects.filter(codename__in=perms_input)
            user.user_permissions.set(perms)

        return user

class CommonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CommonData
        fields = "__all__"