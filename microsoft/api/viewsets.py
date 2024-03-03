import httpx
import requests
import traceback
import unicodedata
from decouple import config
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from user.permissions import UserPermission
from microsoft.api.serializers import MicrosoftSerializer
from files.models import File
from meta.utils import get_folder_id_by_name, list_items_in_drive


class MicrosoftViewSet(viewsets.ViewSet):
    serializer_class = MicrosoftSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get_queryset(self):
        return File.objects.all()
    
    def get_permissions(self):
        if self.action == 'upload_file':
            return [IsAdminUser()]
        return super().get_permissions()


    @action(detail=False, methods=['get'])
    def get_token(self, request):
        # Define your Microsoft Graph API credentials
        tenant_id = config('TENANT_ID')
        client_id = config('CLIENT_ID')
        client_secret = config('CLIENT_SECRET')

        # Define the token URL
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

        # Define the request parameters
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }

        try:
            # Make a POST request to obtain an access token
            with httpx.Client() as client:
                response = client.post(token_url, data=data)

            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                return Response({"Token": access_token})
            else:
                # Handle authentication error here
                print(f"Authentication error: {response.status_code}")
                return Response({"message": "Authentication failed"}, status=response.status_code)
        except Exception as e:
            # Handle other exceptions (e.g., network errors) here
            print(f"Error: {str(e)}")
            return Response({"message": "Error during authentication"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'])
    def upload_file(self, request):
        
        default_user_folder = self.request.user.folder_name
        access_token = self.request.data.get('access_token')
        folder_name = self.request.data['folder_name']
        uploaded_at = self.request.data['uploaded_at']
        expires_at = self.request.data['expires_at']
        period_to_expiration = self.request.data['period_to_expiration']
        file = self.request.data['file']
        subfolder_name = self.request.data.get('subfolder_name')

        drive_id = config('drive_id')

        upload_url = ''
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:"

        folder_id = get_folder_id_by_name(access_token, folder_name)
        if folder_id is None:
            return Response("Folder not found.", status=status.HTTP_404_NOT_FOUND)

        if subfolder_name:
            upload_url = f'{url}/{default_user_folder}/{folder_name}/{subfolder_name}/{file.name}:/content'
        else:
            upload_url = f'{url}/{default_user_folder}/{folder_name}/{file.name}:/content'

        media_content = file.read()

        try:
            with httpx.Client() as client:
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/octet-stream',  # Set content type for file upload
                }

                response = client.put(
                    upload_url,
                    headers=headers,
                    content=media_content,
                )
                print(response.text)

            if response.status_code == 201 or response.status_code == 200:
                metadata = {
                    "user_id": self.request.user.id,
                    "file_name": file.name,
                    "folder_name": folder_name,
                    "uploaded_at": uploaded_at,
                    "expires_at": expires_at,
                }
                File.register_file(files=metadata)
                return Response("File uploaded successfully.", status=status.HTTP_201_CREATED)
            else:
                return Response(f"Failed to upload file: {response.text}", status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response(f"Failed to upload file: {str(error)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def list_files(self, request):
        access_token = request.data.get('access_token', '')
        folder = request.data.get('folder', '')
        subfolder = request.data.get('subfolder', '')
        default_user_folder = self.request.user.folder_name

        items_in_drive = list_items_in_drive(access_token, folder, default_user_folder, subfolder)

        return Response(items_in_drive)
    
    @action(detail=False, methods=['get'])
    def download_file(self, request):
        access_token = self.request.data.get('access_token')
        folder = self.request.data.get('folder')
        item_name = self.request.data.get('item_name')
        subfolder_name = self.request.data.get('subfolder_name')

        download_link = ''
        drive_id = config('drive_id')

        # Adjust the logic based on your requirements
        folder_id = get_folder_id_by_name(access_token, folder)
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/root:"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        if subfolder_name:
            upload_url = f'{url}/{folder}/{subfolder_name}:/children/{item_name}'
        else:
            upload_url = f'{url}/{folder}:/children/{item_name}'

        try:
            with requests.get(upload_url, headers=headers) as response:
                response.raise_for_status()

                response_data = response.json()
                if "@microsoft.graph.downloadUrl" in response_data:
                    download_link = response_data["@microsoft.graph.downloadUrl"]
        except requests.exceptions.RequestException as e:
            # Handle HTTP errors here
            print(f"HTTP error: {e}")

        return Response({'download_link': download_link})

    @action(detail=False, methods=['post'])
    def create_folder(self, request):
        access_token = request.data.get('access_token')
        folder_name = request.data.get('folder_name')
        subfolder_name = request.data.get('subfolder_name')

        # Define drive_id and other necessary variables here
        drive_id = config('drive_id')

        # Your existing logic here to create the folder
        try:
            root_folder_id = get_folder_id_by_name(access_token, folder_name)

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            if root_folder_id.get('folder_id') != '':
                if subfolder_name:
                    normalized_subfolder_name = ''.join([c for c in unicodedata.normalize('NFD', subfolder_name) if not unicodedata.combining(c)])
                    normalized_subfolder_name = normalized_subfolder_name.replace(' ', '').lower()

                    data = {
                        "name": normalized_subfolder_name,
                        "folder": {}
                    }

                    # Make the request using httpx
                    response = httpx.post(
                        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{root_folder_id.get('folder_id')}/children",
                        headers=headers,
                        json=data
                    )

                    # Check the response status code
                    if response.status_code == 201:
                        return Response({"Message": "Folder created!"}, status=status.HTTP_201_CREATED)
                    else:
                        # Handle HTTP errors here
                        print(f"HTTP error: {response.text}")
                else:
                    return Response({"Message": "A folder with that name already exists. Try again using another name!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {
                    "name": folder_name,
                    "folder": {}
                }

                # Make the request using httpx
                response = httpx.post(
                    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children",
                    headers=headers,
                    json=data
                )

                # Check the response status code
                if response.status_code == 201:
                    return Response({"Message": "Folder created!"}, status=status.HTTP_201_CREATED)
                else:
                    # Handle HTTP errors here
                    print(f"HTTP error: {response.text}")
        except Exception:
            traceback.print_exc()
            return Response({"Message": "An error occurred while creating the folder."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
