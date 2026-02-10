from django.views.generic import CreateView
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from app.models import Usuario, Administrador, docente, Estudiante, Acudiente

from app.forms import UsuarioForm, UsuarioUpdateForm, AdministradorForm, DocenteForm, EstudianteForm, AcudienteForm

# --- FUNCIONES DE APOYO ---

def validar_formulario_rol(rol, data, instance=None):
    """
    Valida el formulario según el rol. 
    Pasar 'instance' es la clave para que el botón Actualizar funcione.
    """
    if rol == 'administrador':
        form = AdministradorForm(data, instance=instance)
    elif rol == 'docente':
        form = DocenteForm(data, instance=instance)
    elif rol == 'estudiante':
        form = EstudianteForm(data, instance=instance)
    elif rol == 'acudiente':
        form = AcudienteForm(data, instance=instance)
    else:
        return False, None
    
    return form.is_valid(), form

def guardar_perfil_rol(usuario, rol, data):
    """Crea un perfil nuevo."""
    if rol == 'administrador':
        Administrador.objects.create(usuario=usuario, cargo=data.get('cargo'))
    elif rol == 'docente':
        docente.objects.create(usuario=usuario, especialidad=data.get('especialidad'))
    elif rol == 'estudiante':
        Estudiante.objects.create(
            usuario=usuario,
            codigo=data.get('codigo'),
            fechaNacimiento=data.get('fechaNacimiento'),
            estadoMatricula=data.get('estadoMatricula'),
            fechaIngreso=data.get('fechaIngreso'),
            cursoId_id=data.get('cursoId')
        )
    elif rol == 'acudiente':
        Acudiente.objects.create(usuario=usuario, telefono=data.get('telefono'), direccion=data.get('direccion'))

# --- VISTAS ---
from django.db import connection
from django.utils import timezone
from django.http import JsonResponse


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Usuarios'
        context['crear_url'] = reverse_lazy('app:crear_usuario')
        context['limpiar_url'] = reverse_lazy('app:limpiar_usuario')
        return context

class UsuarioCreateView(View):
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('app:index_usuario')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.contraseña = form.cleaned_data['contraseña']

        usuario.save()

        rol = self.request.POST.get('rol')

        if rol == 'administrador':
            Administrador.objects.create(
                usuario=usuario, cargo='Administrador'
            )

        elif rol == 'docente':
            docente.objects.create(usuario=usuario
            )
        elif rol == 'acudiente':
            Acudiente.objects.create(usuario=usuario)

        messages.success(self.request, 'Usuario creado exitosamente.')
        return redirect(self.success_url)

    def get_context(self, **kwargs):
        context = {
            'usuario_form': UsuarioForm(),
            'admin_form': AdministradorForm(),
            'docente_form': DocenteForm(),
            'estudiante_form': EstudianteForm(),
            'acudiente_form': AcudienteForm(),
            'titulo': 'Crear Usuario',
            'listar_url': reverse_lazy('app:index_usuario'),
            'rol_actual': '',
            'btn_name': 'Guardar'
        }
        context.update(kwargs)
        if 'usuario_form' in context: context['form'] = context['usuario_form']
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context())

    @transaction.atomic
    def post(self, request):
        usuario_form = UsuarioForm(request.POST)
        rol = request.POST.get('rol')
        rol_valido, rol_form = validar_formulario_rol(rol, request.POST)

        if usuario_form.is_valid() and rol_valido:
            usuario = usuario_form.save()
            guardar_perfil_rol(usuario, rol, request.POST)
            messages.success(request, f'Usuario creado correctamente')
            return redirect('app:index_usuario')

        return render(request, self.template_name, self.get_context(usuario_form=usuario_form, rol_actual=rol))

class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioUpdateForm  # Cambiado para no pedir contraseña en edición
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('app:index_usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.object
        context.update({
            'titulo': 'Editar Usuario',
            'listar_url': self.success_url,
            'usuario_form': context.get('form'),
            'admin_form': AdministradorForm(),
            'docente_form': DocenteForm(),
            'estudiante_form': EstudianteForm(),
            'acudiente_form': AcudienteForm(),
            'btn_name': 'Actualizar'
        })

        # Cargar perfiles existentes para mostrar datos en los campos
        admin = Administrador.objects.filter(usuario=usuario).first()
        if admin: context.update({'rol_actual': 'administrador', 'admin_form': AdministradorForm(instance=admin)})
        
        doc = docente.objects.filter(usuario=usuario).first()
        if doc: context.update({'rol_actual': 'docente', 'docente_form': DocenteForm(instance=doc)})

        est = Estudiante.objects.filter(usuario=usuario).first()
        if est: context.update({'rol_actual': 'estudiante', 'estudiante_form': EstudianteForm(instance=est)})

        acu = Acudiente.objects.filter(usuario=usuario).first()
        if acu: context.update({'rol_actual': 'acudiente', 'acudiente_form': AcudienteForm(instance=acu)})
            
        return context

    def form_valid(self, form):
        usuario = form.save()
        nuevo_rol = self.request.POST.get('rol')

        # Buscar qué perfil tiene actualmente el usuario
        p_admin = Administrador.objects.filter(usuario=usuario).first()
        p_doc = docente.objects.filter(usuario=usuario).first()
        p_est = Estudiante.objects.filter(usuario=usuario).first()
        p_acu = Acudiente.objects.filter(usuario=usuario).first()
        
        perfil_previo = p_admin or p_doc or p_est or p_acu

        # Identificar la instancia que coincide con el rol seleccionado
        instancia_a_validar = None
        if nuevo_rol == 'administrador': instancia_a_validar = p_admin
        elif nuevo_rol == 'docente': instancia_a_validar = p_doc
        elif nuevo_rol == 'estudiante': instancia_a_validar = p_est
        elif nuevo_rol == 'acudiente': instancia_a_validar = p_acu

        # Validar pasando la instancia para que Django sepa que es una EDICIÓN
        valido, rol_form = validar_formulario_rol(nuevo_rol, self.request.POST, instance=instancia_a_validar)

        if not valido:
            messages.error(self.request, 'Errores en los campos del perfil.')
            return self.render_to_response(self.get_context_data(form=form))

        # Lógica de guardado
        if perfil_previo and instancia_a_validar is None:
            # Si el rol cambió (ej: de docente a admin), borramos el anterior y creamos nuevo
            perfil_previo.delete()
            guardar_perfil_rol(usuario, nuevo_rol, self.request.POST)
        else:
            # Si es el mismo rol, actualizamos los datos existentes
            obj = rol_form.save(commit=False)
            obj.usuario = usuario
            obj.save()

        messages.success(self.request, 'Usuario actualizado correctamente')
        return redirect(self.success_url)
