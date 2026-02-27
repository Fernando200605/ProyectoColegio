from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

class VerificarEstadoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario está autenticado, verificamos su campo 'estado'
        if request.user.is_authenticated:
            if not request.user.estado:
                logout(request)
                messages.error(request, "Tu cuenta ha sido desactivada.", extra_tags='danger')
                return redirect('app:login') 

        response = self.get_response(request)
        return response