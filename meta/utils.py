import httpx
import base64
import smtplib
import os
import secrets
import traceback
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import render


# OAuth Microsoft Configuration
client_id = "82d6aea6-5d83-41de-9a32-58758704def1"
client_secret = "Uwx8Q~BsjB~o6JDBXXwIKbhiICrR86NmUvBp7a3-"
tenant_id = "1e5db031-a870-4c8c-b55d-06e4a7a743b1"
redirect_uri = "https://api.metasolucoesambientais.com.br/api/v1/callback"
# redirect_uri = "http://127.0.0.1:8000/api/v1/callback"
scope = "https://graph.microsoft.com/.default"
access_token = None
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
state = secrets.token_urlsafe(16)
drive_id = '4cb9b710-d164-45d6-838e-ae8e66070056'
URL = f'http://localhost:8000' if not "production" in os.environ else f'http://193.203.174.195:8000'

async def exchange_code_for_token(code: str):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        token_data = response.json()
        print(f'ACCESS TOKEN::: {token_data.get("access_token")}')

    return token_data.get("access_token")


def get_user_drive_id(token: str):
    with httpx.Client() as client:
        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = client.get(
            "https://graph.microsoft.com/v1.0/me/drive",
            headers=headers
        )

    if response.status_code == 200:
        response_data = response.json()
        drive_id = response_data.get("id")
        return {"drive_id": drive_id}
    else:
        # Handle HTTP errors here
        print(f"HTTP error: {response.status_code} - {response.text}")


def list_available_drives(token: str):
    with httpx.Client() as client:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = client.get(
            "https://graph.microsoft.com/v1.0/me/drives",
            headers=headers
        )

    if response.status_code == 200:
        response_data = response.json()

        # Print information about available drives
        for drive in response_data.get("value"):
            drive_id = drive.get("id")
            drive_name = drive.get("name")
            print(f"Drive Name: {drive_name}, Drive ID: {drive_id}")
    else:
        # Handle HTTP errors here
        print(f"HTTP error: {response.status_code}")


def get_folder_id_by_name(token: str, folder_name: str):
    folder_id = ''

    with httpx.Client() as client:
        # Define the authorization header
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Make a request to list the root folders in the user's drive
        response = client.get(
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children",
            headers=headers
        )
    
        if response.status_code == 200:
            response_data = response.json()

            for item in response_data.get("value"):
                if item.get("folder") and item.get("name") == folder_name:
                    folder_id = item.get("id")
                    break
        else:
            # Handle HTTP errors here
            print(f"HTTP error: {response.status_code} - {response.text}")
            
    return {"folder_id": folder_id}


def get_subfolder_id_by_name(token: str, parent_folder_id, subfolder: str = None):
    folder_id = ''
    print(parent_folder_id)

    with httpx.Client() as client:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "$filter": f"name eq '{subfolder}'",
        }
        response = client.get(
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{parent_folder_id}/children", 
            headers=headers, 
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('value') and len(data['value']) > 0:
                # Assuming there's only one subfolder with the given name, return its ID
                folder_id = data['value'][0]['id']
            else:
                return None
        else:
            return None
            
    return {"folder_id": folder_id}


def list_items_in_drive(token: str, folder_name: str, default_folder: str, subfolder: str = None):
    print(f'DEFAULT USER FOLDER::: {default_folder}')
    # microsoft OneDrive API just accept a single path to folder, so we created a default folder path,
    # i.e. the var below contains the full path folder configuration to user folder and subfolder if exists.
    folder_path = f"{default_folder}/{folder_name}/{subfolder}" if subfolder else f"{default_folder}/{folder_name}"
    items = []

    with httpx.Client() as client:
        # Define the authorization header
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Make a request to list items in the root of the user's drive
        response = client.get(
            # f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{default_folder}:/{folder_name}:/children",
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder_path}:/children",
            headers=headers
        )

        if response.status_code == 200:
            response_data = response.json()

            for item in response_data.get("value"):
                item_name = item.get("name")
                items.append(item_name)
        else:
            # Handle HTTP errors here
            print(f"HTTP error: {response.status_code} - {response.text}")

    return items


async def encode_file_to_base64(file):
    file_binary_data = await file.read()

    try:
        base64_encoded_content = base64.b64encode(file_binary_data).decode('utf-8')
        return base64_encoded_content
    except Exception as e:
        print(f"Error encoding file to base64: {e}")
        return None
    

def _send_email(message, recipients):
    subject = 'Meta - Notificação de expiração de documento.'
    from_email = 'wendrewoliveira@onemancompany682.onmicrosoft.com'
    recipient_list = [recipients]

    try:
        send_mail(
            subject, 
            message, 
            from_email, 
            recipient_list,
            fail_silently=False
        )
    except Exception as error:
        print(f"Error sending email: {error}")
        traceback.print_exc()


def format_date(raw_date: str):
    formats_to_try = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']
    parsed_date = None

    for format_str in formats_to_try:
        try:
            parsed_date = datetime.strptime(raw_date, format_str)
            if parsed_date is not None:
                # Format the parsed date to the desired format
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                return formatted_date
            else:
                print("Failed to parse the date.")
        except ValueError:
            pass


def generate_temporary_password():
    temporary_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return temporary_password
