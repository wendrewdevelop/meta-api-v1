from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from user.models import User
from user.api.serializers import UserSerializer
from user.permissions import UserPermission


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    # authentication_classes = [TokenAuthentication]
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
            last_name=data['last_name']
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