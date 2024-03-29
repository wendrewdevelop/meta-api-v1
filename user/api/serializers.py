from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'password',
            'cpf_cnpj',
            'phone',
            'birthday'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['folder_name'] = instance.folder_name

        return data
    

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = User.objects.filter(email=email).first()

        if not user:
            msg = "Unable to log in with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        if not email or not password:
            msg = "Must include 'email' and 'password'."
            raise serializers.ValidationError(msg, code="authorization")

        if password == user.temporary_password:
            data = {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "temporary_password": True
                }
            }
        else:
            if not check_password(password, user.password):
                msg = "Incorrect password."
                raise serializers.ValidationError(msg, code="authorization")

            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "folder_name": user.folder_name,
                    "phone": user.phone,
                    "cpf_cnpj": user.cpf_cnpj,
                    "birthday": user.birthday,
                    "is_staff": user.is_staff
                }
            }

        return data

    
class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value
