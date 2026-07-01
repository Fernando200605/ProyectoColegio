import os
import requests
from app.models import *
from openai import OpenAI
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from app.utils import obtener_rutas

client = OpenAI(
    api_key= "", base_url="https://api.deepseek.com"
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


def normalizar_ruta(r):
    r = "/" + r.strip("/ \t")
    r = r.replace("^", "").replace("$", "")
    return r


import json
import os
import re
import requests

from django.conf import settings
from django.http import JsonResponse

LOCAL_HOST = "http://127.0.0.1:8000"


def cargar_base_conocimiento():
    ruta_md = os.path.join(
        settings.BASE_DIR,
        "base_conocimiento_ia.md"
    )

    try:
        with open(ruta_md, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except Exception as e:
        print("Error leyendo markdown:", e)
        return ""


def buscar_fragmentos(texto, consulta, max_fragmentos=3):
    """
    Busca fragmentos relevantes dentro del markdown.
    """

    consulta = consulta.lower()

    bloques = texto.split("\n## ")

    puntuados = []

    palabras = consulta.split()

    for bloque in bloques:

        score = 0

        contenido = bloque.lower()

        for palabra in palabras:
            if palabra in contenido:
                score += 1

        if score > 0:
            puntuados.append((score, bloque))

    puntuados.sort(reverse=True)

    seleccionados = []

    for _, bloque in puntuados[:max_fragmentos]:
        seleccionados.append(bloque)

    return "\n\n".join(seleccionados)

@csrf_exempt
def preguntar_ia_local(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    try:

        data = json.loads(request.body)

        mensaje = data.get("mensaje", "").strip()

        if not mensaje:
            return JsonResponse(
                {"respuesta": "Debe escribir una pregunta."},
                status=400
            )

        rutas_validas = obtener_rutas()

        rutas_normalizadas = [
            normalizar_ruta(r)
            for r in rutas_validas
        ]

        conocimiento = cargar_base_conocimiento()

        contexto = buscar_fragmentos(
            conocimiento,
            mensaje,
            max_fragmentos=3
        )

        prompt_completo = f"""
Eres el asistente oficial del sistema.

Debes responder únicamente utilizando la información suministrada.

Si la respuesta no existe dentro del contexto responde:

"No se encontró información relacionada con esa consulta."

RUTAS DISPONIBLES:

{', '.join(rutas_normalizadas)}

CONTEXTO:

{contexto}

PREGUNTA:

{mensaje}

RESPUESTA:
"""

        print("Tamaño contexto:", len(contexto))
        print("Pregunta:", mensaje)

        respuesta = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:1.5b-base",
                "prompt": prompt_completo,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "top_k": 40,
                    "num_predict": 300,
                },
            },
            timeout=120,
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

        ia_texto = resultado.get(
            "response",
            "No se obtuvo respuesta."
        )

        rutas_detectadas = re.findall(
            r"`(/[^`]+)`",
            ia_texto
        )

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

                url_completa = (
                    f"{LOCAL_HOST}{ruta_match}"
                )

                link_html = (
                    f'<a href="{url_completa}" '
                    f'target="_blank">{ruta_match}</a>'
                )

                ia_texto = ia_texto.replace(
                    f"`{ruta}`",
                    link_html
                )

        return JsonResponse({
            "respuesta": ia_texto
        })

    except requests.exceptions.RequestException as e:

        print("Error Ollama:", e)

        if hasattr(e, "response") and e.response:
            print(e.response.text)

        return JsonResponse(
            {
                "respuesta":
                "Error de comunicación con la IA."
            },
            status=500
        )

    except Exception as e:

        print("Error:", e)

        return JsonResponse(
            {
                "respuesta":
                "Ocurrió un error inesperado."
            },
            status=500
        )

