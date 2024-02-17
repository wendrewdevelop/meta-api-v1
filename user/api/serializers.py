from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    folder_name = serializers.CharField(source='user.folder_name', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'password',
            'folder_name',
            'cpf_cnpj',
            'phone'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # If user is_staff is True, include the 'folder_name' in the response
        if instance.is_staff:
            data['folder_name'] = instance.folder_name

        return data