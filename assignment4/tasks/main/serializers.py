from rest_framework import serializers
from .models import SecureUserInfoModel

class SecureUserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureUserInfoModel
        fields = ['id', 'name', 'age', 'website', 'encrypted_bin']
