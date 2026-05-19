import os
import json

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError


SCOPES = [
    'https://www.googleapis.com/auth/calendar'
]


def obtener_servicio():

    creds = None

    # Leer token guardado
    if os.path.exists('token.json'):

        creds = Credentials.from_authorized_user_file(
            'token.json',
            SCOPES
        )

    # Si no existe o expiró
    if not creds or not creds.valid:

        # Refrescar token
        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Guardar token nuevo
        with open('token.json', 'w') as token:

            token.write(creds.to_json())

    service = build(
        'calendar',
        'v3',
        credentials=creds
    )

    return service


def crear_evento(
    titulo,
    descripcion,
    fecha_inicio,
    fecha_fin
):

    servicio = obtener_servicio()

    evento = {

        "summary": titulo,

        "description": descripcion,

        "start": {
            "dateTime": fecha_inicio.isoformat(),
            "timeZone": "America/Bogota",
        },

        "end": {
            "dateTime": fecha_fin.isoformat(),
            "timeZone": "America/Bogota",
        },
    }

    evento_creado = servicio.events().insert(
        calendarId='primary',
        body=evento
    ).execute()

    return evento_creado


def actualizar_evento(
    google_event_id,
    titulo,
    descripcion,
    fecha_inicio,
    fecha_fin
):
    try:
        servicio = obtener_servicio()
        evento_actualizado = {
            "summary":titulo,
            "description":descripcion,
            "start":{
                "dateTime":fecha_inicio.isoformat(),
                "timeZone":"America/Bogota",
                },
            "end":{
                "dateTime":fecha_fin.isoformat(),
                "timeZone":"America/Bogota",
                },
        }
        resultado = servicio.events().update(
            calendarId = 'primary',
            eventId=google_event_id,
            body=evento_actualizado
        ).execute()
        return resultado
    
    except HttpError as error:
        print("Error actualizando el evento" , error)
        return None
    
    
    
def eliminar_evento(google_event_id):
    try:
        servicio = obtener_servicio()
        
        servicio.events().delete(
            calendarId = 'primary',
            eventId = google_event_id
        ).execute()
        print("Evento eliminado del Google Calendar")
    
    except Exception as e:
        print("Error al eliminar el evento ",e)