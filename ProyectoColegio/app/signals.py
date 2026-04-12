from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from app.models import Usuario, Notificacion ,Curso



@receiver(post_migrate)
def inicializar_roles(sender, **kwargs):
    grupos = ['Administrador', 'Docente', 'Estudiante', 'Acudiente']
    for nombre in grupos:
        Group.objects.get_or_create(name=nombre)
    admin, _ = Group.objects.get_or_create(name='Administrador')
    admin.permissions.set(Permission.objects.all())
    docente, _ = Group.objects.get_or_create(name='Docente')
    docente.permissions.set(
        Permission.objects.filter(
            codename__in=[
                'view_usuario',
                'view_curso',
            ]
        )
    )




@receiver(post_save, sender=Usuario)
def notificar_usuario(sender, instance, created, **kwargs):
    update_fields = kwargs.get('update_fields')
    if update_fields and 'last_login' in update_fields and len(update_fields) == 1:
        return
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

    for admin in administradores:
        Notificacion.objects.create(
            titulo=titulo,
            mensaje=mensaje,
            fecha_envio=now().date(),
            estado='Activo',
            tipo="Sistema",
            receptor_id=admin.id
        )

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


# 🔹 3. CREAR NOTIFICACIÓN Y ENVIAR CORREO AL CREAR/EDITAR UN CURSO
@receiver(post_save, sender=Curso)
def notificar_curso(sender, instance, created, **kwargs):

    # Obtener administradores
    administradores = [u for u in Usuario.objects.all() if u.get_rol() == "Administrador"]

    # Definir mensajes dinámicos
    if created:
        titulo = "Se ha creado un nuevo curso"
        mensaje = f"Se creó el curso {instance.codigo} — Grado: {instance.grado}"
        asunto = "Nuevo curso creado"
        cuerpo = f"El curso {instance.codigo} ha sido creado y está disponible en el sistema."
    else:
        titulo = "Se ha actualizado un curso"
        mensaje = f"Se editó el curso {instance.codigo} — Grado: {instance.grado}"
        asunto = "Curso actualizado"
        cuerpo = f"El curso {instance.codigo} ha sido actualizado en el sistema."

    # 🔸 Crear notificaciones para administradores
    for admin in administradores:
        Notificacion.objects.create(
            titulo=titulo,
            mensaje=mensaje,
            fecha_envio=now().date(),
            estado='Activo',
            tipo="Actualización",
            receptor=admin
        )

    # 🔸 Enviar correo al docente del curso (HTML)
    # ✅ CORREGIDO: se verifica que el curso tenga docente asignado antes de enviar
    try:
        if instance.docenteid and hasattr(instance.docenteid, 'usuario'):
            docente_usuario = instance.docenteid.usuario
            html_content = render_to_string('emails/notificacion.html', {
                'titulo': titulo,
                'nombre': docente_usuario.nombre,
                'mensaje': cuerpo,
                'enlace': 'http://127.0.0.1:8000/login/'
            })

            text_content = strip_tags(html_content)

            correo = EmailMultiAlternatives(
                asunto,
                text_content,
                'davidfernandomonroy932@gmail.com',
                [docente_usuario.email]
            )

            correo.attach_alternative(html_content, "text/html")
            correo.send()

    except Exception as e:
        print("Error enviando correo al docente:", e)
