from rest_framework import serializers
from authentication.models import User, Role


class UserListSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'gender',
            'is_active', 'is_staff', 'date_joined', 'role', 'role_name',
        ]
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'gender', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'role', 'is_active', 'is_staff']


class RoleListSerializer(serializers.ModelSerializer):
    permissions_list = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions', 'permissions_list']
        read_only_fields = fields

    def get_permissions_list(self, obj):
        return obj.get_permissions_list()


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']
