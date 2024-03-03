from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework import status
from user.models import User
from user.api.serializers import UserSerializer, CustomAuthTokenSerializer
from user.permissions import UserPermission
from meta.utils import generate_temporary_password


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.all()
    
    def list(self, request, *args, **kwargs):
        return super(UserViewset, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        print(f'DATA::: {data}')
        hashed_password = make_password(data['password'])

        user = User.objects.create(
            email=data['email'],
            password=hashed_password,
            first_name=data['first_name'],
            last_name=data['last_name'],
            folder_name=data['folder_name'],
            phone=data['phone'],
            cpf_cnpj=data['cpf_cnpj']
        )
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        return super(UserViewset, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewset, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewset, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(UserViewset, self).partial_update(request, *args, **kwargs)
    

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

class PasswordResetViewSet(ModelViewSet):
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=email, password=password)

        if user:
            # Generate or retrieve user's token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'})

    @action(detail=False, methods=['post'])
    def password_reset(self, request):
        email = request.data.get('username')

        try:
            user = User.objects.get(email=email)
            temporary_password = generate_temporary_password()
            print(temporary_password)
            user.temporary_password = make_password(temporary_password)
            user.save()

            # Send email with temporary password
            # send_mail(
            #     'Temporary Password',
            #     f'Your temporary password is: {temporary_password}',
            #     'from@example.com',
            #     [email],
            #     fail_silently=False,
            # )

            return Response({'detail': 'Temporary password sent to your email'})
        except User.DoesNotExist:
            return Response({'detail': 'User with this email does not exist'})
