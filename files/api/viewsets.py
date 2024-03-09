from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from files.models import File
from files.api.serializers import FileSerializer
from user.permissions import UserPermission


class FileViewset(ModelViewSet):
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual' 
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
    
    @action(detail=False, methods=["POST"])
    def update_file_status(self, request):
        file_id = request.data.get("file_id")
        file_object = File.objects.get(id=file_id)

        try:
            file_object.status = request.data.get("status")
            file_object.save()

            return Response({"Message": f"Status do arquivo ({file_object.file_name}) foi atualizado com sucesso!"})
        except Exception as error:
            print(error)
            return Response({"Message": f"Status do arquivo ({file_object.file_name}) não pode ser atualizado!"})
        
    @action(detail=True, methods=["GET"])
    def get_user_files(self, request, pk=None):
        file_instance = File.objects.filter(user_id=pk).all()
        serializer = FileSerializer(file_instance, many=True)  # Serializa os objetos File

        try:
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response({"Message": "Erro ao retornar as informações do arquivo", "Erro": f"{error}"})