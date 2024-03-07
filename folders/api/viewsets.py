from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from folders.models import Folder
from folders.api.serializers import FolderSerializer
from user.permissions import UserPermission


class FolderViewset(ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual' 
    serializer_class = FolderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get_queryset(self):
        return Folder.objects.all()
    
    def list(self, request, *args, **kwargs):
        return super(FolderViewset, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(FolderViewset, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(FolderViewset, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(FolderViewset, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(FolderViewset, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(FolderViewset, self).partial_update(request, *args, **kwargs)
        
    @action(detail=True, methods=["GET"])
    def get_user_folders(self, request, pk=None):
        folder_instance = Folder.objects.filter(user_id=pk).all()
        serializer = FolderSerializer(folder_instance, many=True)

        try:
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response({"Message": f"Erro ao retornar as pastas do usuário.", "Erro": f"{error}"})