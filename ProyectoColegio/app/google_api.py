import os
import json

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from django.conf import settings

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


TOKEN_PATH = os.path.join(
    settings.BASE_DIR,
    "token.json"
)

CREDENTIALS_PATH = os.path.join(
    settings.BASE_DIR,
    "credentials.json"
)


def obtener_servicio():

    creds = None

    # Leer token guardado
    if os.path.exists(TOKEN_PATH):

        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH,
            SCOPES
        )

    # Si no existe o expiró
    if not creds or not creds.valid:

        # Refrescar automáticamente
        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):

            creds.refresh(Request())

        else:
            # Solo la primera vez
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH,
                SCOPES
            )

            creds = flow.run_local_server(
                port=8080,
                prompt="consent",
                access_type="offline"
            )

        # Guardar token actualizado
        with open(TOKEN_PATH, "w") as token:

            token.write(
                creds.to_json()
            )

    service = build(
        "calendar",
        "v3",
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