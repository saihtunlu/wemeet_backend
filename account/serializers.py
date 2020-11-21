from rest_framework.fields import ReadOnlyField
from .models import User
from rest_framework import serializers
# from permission.serializers import UserRoleSerializers


class UserSerializer(serializers.ModelSerializer):
    # role = UserRoleSerializers(many=False, read_only=True)
    details = serializers.JSONField()

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'first_name',
                  'last_name', 'email', 'avatar', 'username', 'details', 'user_role']
