from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import logout


from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import logout

class LoginRequiredMiddleware:
    EXEMPT_URL_NAMES = [
        "login:login",
        "login:logout",
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [str(reverse_lazy(name)) for name in self.EXEMPT_URL_NAMES]

    def __call__(self, request):
        path = request.path_info

        # Permitir URLs exentas
        if any(path.startswith(url) for url in self.exempt_urls):
            return self.get_response(request)

        # Si no está autenticado
        if not request.user.is_authenticated:
            return self.redirect_to_login(path)

        # 🔥 FORZAR ACTUALIZACIÓN DESDE BD
        request.user.refresh_from_db()

        print("Estado user:", request.user.estado)
        # 🔥 VALIDACIÓN
        if hasattr(request.user, "estado"):
            if not request.user.estado:
                print("Usuario inactivo, cerrando sesión")
                logout(request)
                return self.redirect_to_login(path)

        return self.get_response(request)

    # 👇 ESTO ES LO QUE TE FALTABA
    def redirect_to_login(self, path):
        login_url = str(reverse_lazy(settings.LOGIN_URL))
        return redirect(f'{login_url}?next={path}')