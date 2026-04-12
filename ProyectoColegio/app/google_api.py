import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def obtener_servicio():
    with open('token.json', 'r') as token_file:
        creds_data = json.load(token_file)
    
    creds = Credentials.from_authorized_user_info(creds_data)
    
    service = build('calendar', 'v3', credentials=creds)
    return service


def obtener_servicio_forms():
    # 1. Leemos el mismo archivo token.json que ya usas
    with open('token.json', 'r') as token_file:
        creds_data = json.load(token_file)
    
    # 2. Cargamos las credenciales (esto maneja el refresh_token automáticamente)
    creds = Credentials.from_authorized_user_info(creds_data)
    
    # 3. Construimos el servicio para Forms v1
    service = build('forms', 'v1', credentials=creds)
    
    return service

