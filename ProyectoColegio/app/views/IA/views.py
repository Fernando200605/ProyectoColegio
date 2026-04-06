import os
from app.models import *
from openai import OpenAI
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
client = OpenAI(api_key=os.getenv("KEY_PASSWORD_IA") ,base_url="https://api.deepseek.com")
@csrf_exempt
def preguntar_ia(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mensaje = data.get("mensaje")
        
        respuesta = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": mensaje}
            ]
        )
        return JsonResponse({
            "respuesta": respuesta.choices[0].message.content
        })