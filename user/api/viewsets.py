import random
import string
import httpx
from decouple import config
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle
from user.models import User
from user.api.serializers import UserSerializer, CustomAuthTokenSerializer


class UserViewset(ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual' 
    serializer_class = UserSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST' and self.request.path.endswith('recover_password/'):
            return [AllowAny()]
        if self.request.method == 'POST' and self.request.path.endswith('update_password/'):
            return [AllowAny()]
        return super().get_permissions()

    def get_authenticators(self):
        if self.request.method == 'POST' and self.request.path.endswith('recover_password/'):
            return []
        if self.request.method == 'POST' and self.request.path.endswith('update_password/'):
            return []
        return super().get_authenticators()

    def get_queryset(self):
        return User.objects.all()
    
    def list(self, request, *args, **kwargs):
        return super(UserViewset, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        access_token = request.data.get('access_token')
        hashed_password = make_password(data['password'])
        default_user_folder = f'{data["first_name"]}_{data["last_name"]}_{data["cpf_cnpj"][:5]}'
        data["folder_name"] = default_user_folder.replace(" ", "_")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        drive_id = config('drive_id')

        try:
            user = User.objects.create(
                email=data['email'],
                password=hashed_password,
                first_name=data['first_name'],
                last_name=data['last_name'],
                folder_name=default_user_folder.replace(" ", "_"),
                phone=data['phone'],
                cpf_cnpj=data['cpf_cnpj'],
                birthday=data['birthday']
            )
            serializer = UserSerializer(user)

            response = httpx.post(
                f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children",
                headers=headers,
                json={
                    "name": default_user_folder.replace(" ", "_"),
                    "folder": {}
                }
            )
            print(response)
            return Response(serializer.data)
        except Exception as error:
            print(error)
        
    def destroy(self, request, *args, **kwargs):
        return super(UserViewset, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewset, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewset, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(UserViewset, self).partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def recover_password(self, request):
        email = request.data.get('email')

        temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        subject = 'Senha temporaria'
        message = f'Segue a sua senha temporaria: {temporary_password}'
        from_email = 'WendrewOliveira@ONEMANCOMPANY682.onmicrosoft.com'
        recipient_list = [email]

        try:
            user_instance = User.objects.get(email=email)
            user_instance.temporary_password = temporary_password
            user_instance.save()

            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "Senha temporária enviada para o email fornecido."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Erro ao gerar a senha temporaria."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['put'])
    def update_password(self, request, pk=None):
        user = User.objects.get(id=pk)
        password = request.data.get('password')

        if password:
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()

            # Invalidate existing tokens by deleting them
            Token.objects.filter(user=user).delete()

            # Generate a new token for the user
            new_token, _ = Token.objects.get_or_create(user=user)

            return Response({"message": "Password updated successfully.", "token": new_token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "New password not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['put'])
    def update_birthday(self, request, pk=None):
        user_instance = User.objects.get(id=pk)

        try:
            user_instance.birthday = request.data.get('birthday')
            user_instance.save()
            return Response({"Message": "Data de aniversario atualizada com sucesso."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"Message": error}, status=status.HTTP_400_BAD_REQUEST)


    
class CustomObtainAuthToken(ObtainAuthToken):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual' 
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

