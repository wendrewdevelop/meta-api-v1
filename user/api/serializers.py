from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
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

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")

            token, _ = Token.objects.get_or_create(user=user)

            # Customize the data to return along with the token
            data = {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_staff": user.is_staff,
                    "folder_name": user.folder_name,
                    "phone": user.phone,
                    "cpf_cnpj": user.cpf_cnpj,
                    # Add more fields as needed
                }
            }
            return data
        else:
            msg = "Must include 'email' and 'password'."
            raise serializers.ValidationError(msg, code="authorization")
    

class UserPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value