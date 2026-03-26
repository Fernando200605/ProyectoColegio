from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app.models import Usuario, Notificacion


# 🔹 1. CREAR ROLES AUTOMÁTICAMENTE
@receiver(post_migrate)
def inicializar_roles(sender, **kwargs):

    grupos = ['Administrador', 'Docente', 'Estudiante', 'Acudiente']

    # Crear grupos
    for nombre in grupos:
        Group.objects.get_or_create(name=nombre)

    # Administrador → todos los permisos
    admin, _ = Group.objects.get_or_create(name='Administrador')
    admin.permissions.set(Permission.objects.all())

    # Docente → permisos específicos
    docente, _ = Group.objects.get_or_create(name='Docente')
    docente.permissions.set(
        Permission.objects.filter(
            codename__in=[
                'view_usuario', 'change_usuario',
                'view_curso', 'change_curso'
            ]
        )
    )


# 🔹 2. CREAR NOTIFICACIÓN Y ENVIAR CORREO
@receiver(post_save, sender=Usuario)
def notificar_usuario(sender, instance, created, **kwargs):

    # Obtener administradores (ajusta según tu modelo)
    administradores = [u for u in Usuario.objects.all() if u.get_rol() == "Administrador"]

    # Definir mensajes dinámicos
    if created:
        titulo = "Se ha creado un nuevo usuario"
        mensaje = f"Se creó el usuario {instance.nombre}"
        asunto = "Creación de cuenta"
        cuerpo = "Tu cuenta ha sido creada correctamente."
    else:
        titulo = "Se ha editado un usuario"
        mensaje = f"Se editó el usuario {instance.nombre}"
        asunto = "Edición de cuenta"
        cuerpo = "Tu cuenta ha sido actualizada correctamente."

    # 🔸 Crear notificaciones para administradores
    for admin in administradores:
        Notificacion.objects.create(
            titulo=titulo,
            mensaje=mensaje,
            fecha_envio=now().date(),
            estado='Activo',
            tipo="Sistema",
            receptor_id=admin.id
        )

    # 🔸 Enviar correo al usuario afectado (HTML)
    try:
        html_content = render_to_string('emails/notificacion.html', {
            'titulo': titulo,
            'nombre': instance.nombre,
            'mensaje': cuerpo,
            'enlace': 'http://127.0.0.1:8000/login/'
        })

        text_content = strip_tags(html_content)

        correo = EmailMultiAlternatives(
            asunto,
            text_content,
            'davidfernandomonroy932@gmail.com',
            [instance.email]
        )

        correo.attach_alternative(html_content, "text/html")
        correo.send()

    except Exception as e:
        print("Error enviando correo:", e)