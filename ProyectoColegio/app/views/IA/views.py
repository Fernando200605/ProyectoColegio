import os
import requests
from app.models import *
from openai import OpenAI
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from app.utils import obtener_rutas

client = OpenAI(
    api_key=os.getenv("KEY_PASSWORD_IA") , base_url="https://api.deepseek.com",

    api_key= os.getenv("IA_SECRET_KEY"), base_url="https://api.deepseek.com"

)
import re


@csrf_exempt
def preguntar_ia(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mensaje = data.get("mensaje")

        respuesta = client.chat.completions.create(
            model="deepseek-chat", messages=[{"role": "user", "content": mensaje}]
        )
        return JsonResponse({"respuesta": respuesta.choices[0].message.content})


LOCAL_HOST = os.getenv("APP_HOST", "http://127.0.0.1:8000")


def normalizar_ruta(r):
    r = "/" + r.strip("/ \t")
    r = r.replace("^", "").replace("$", "")
    return r

@csrf_exempt
def preguntar_ia_local(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mensaje = data.get("mensaje", "")

        rutas_validas = obtener_rutas()
        rutas_normalizadas = [normalizar_ruta(r) for r in rutas_validas]
        print("Rutas normalizadas:", rutas_normalizadas)

        # Mejoramos el prompt para guiar mejor a Qwen
        prompt_completo = f"""
Estas son las rutas válidas de la app: {', '.join(rutas_normalizadas)}.
Cuando menciones una ruta, escríbela SIEMPRE entre comillas invertidas (backticks), exactamente como aparece en la lista.
Responde al usuario usando solo estas rutas válidas de forma concisa , en dado caso de no existir decir que no se encontro

Usuario pregunta: {mensaje}
"""

        try:
            # NOTA: Cambiamos /api/generate por /api/chat que es más eficiente para diálogos,
            # o mantenemos /api/generate pero corrigiendo las opciones.
            respuesta = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen3:8b",  # Ya confirmamos que este es el nombre real
        "prompt": prompt_completo,
        "stream": False,
        "options": {
            "num_predict": 150,  # Lo bajamos un poco de 250 a 150 para que responda más rápido
            "temperature": 0.3,
            "top_k": 100,
        },
    },
    timeout=200, 
)
            respuesta.raise_for_status()  # Lanza error si Ollama responde un 400 o 500
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con Ollama: {e}")
            return JsonResponse(
                {"respuesta": "Error de comunicación con la IA local."}, status=500
            )

        resultado = respuesta.json()
        ia_texto = resultado.get("response", "")
        print("Texto IA:", ia_texto)

        rutas_detectadas = re.findall(r"`(/[^`]+)`", ia_texto)
        print("Rutas detectadas:", rutas_detectadas)

        ia_texto_con_links = ia_texto

        for ruta in set(rutas_detectadas):
            ruta_limpia = normalizar_ruta(ruta)
            ruta_match = None
            if ruta_limpia in rutas_normalizadas:
                ruta_match = ruta_limpia
            elif ruta_limpia + "/" in rutas_normalizadas:
                ruta_match = ruta_limpia + "/"
            elif ruta_limpia.rstrip("/") in rutas_normalizadas:
                ruta_match = ruta_limpia.rstrip("/")

            if ruta_match:
                url_completa = f"{LOCAL_HOST}{ruta_match}"
                link_html = (
                    f'<a href="{url_completa}" target="_blank">{ruta_match}</a>'
                )
                ia_texto_con_links = ia_texto_con_links.replace(
                    f"`{ruta}`", link_html
                )

        return JsonResponse({"respuesta": ia_texto_con_links})