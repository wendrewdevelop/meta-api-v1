import datetime
import json
from datetime import datetime, date
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import UserRateThrottle
from rest_framework.authentication import TokenAuthentication
from notifications.models import Notification
from notifications.api.serializers import NotificationSerializer
from user.permissions import UserPermission
from files.models import File
from files.api.serializers import FileSerializer
from meta.utils import _send_email


class NotificationViewset(ModelViewSet):
    """Viewset to notify user docs expiration

        {
            "id": "8485032e-a5ec-4d1d-9b8d-818ee0111e35", # ID do arquivo
            "file_name": "manage.py", # nome do arquivo
            "folder_name": "pessoal", # nome da pasta
            "uploaded_at": "2024-01-15",# data de upload do arquivo
            "expires_at": "2024-06-10", # data original de expiração do arquivo
            "period_to_expiration": "30", # periodo, definido pelo usuário, em que o documento começará a ser notificado sobre a expiração
            "expire_notification": "2024-05-11", # Data em que o usuário começará a ser notificado
            "user": "87366039-c2e3-40e6-872f-9c6ead940c86" 
        }
    """
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user_individual' 
    serializer_class = FileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    @action(detail=False, methods=['GET'])
    def send(self, request):
        query = File.objects.filter(
            user=self.request.user,
            expire_notification__lte=date.today()
        )
        if query:
            for data in query:
                message = f'Olá, o ser arquivo {data.file_name} irá expirar em {data.expires_at}.'
                print(data.user.email)
                print(message)
                _send_email(message=message, recipients=data.user.email)

        serializer = FileSerializer(query, many=True)
        return Response({"notification": serializer.data})