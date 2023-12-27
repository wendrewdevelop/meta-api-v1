from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from files.models import File
from files.api.serializers import FileSerializer
from user.permissions import UserPermission


class FileViewset(ModelViewSet):
    serializer_class = FileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get_queryset(self):
        return File.objects.all()
    
    def list(self, request, *args, **kwargs):
        return super(FileViewset, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(FileViewset, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(FileViewset, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(FileViewset, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(FileViewset, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(FileViewset, self).partial_update(request, *args, **kwargs)