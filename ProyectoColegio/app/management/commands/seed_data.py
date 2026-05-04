from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import Group
rol_admin = Group.objects.get(name="Administrador")
rol_docente = Group.objects.get(name="Docente")
rol_estudiante = Group.objects.get(name="Estudiante")
rol_acudiente = Group.objects.get(name="Acudiente")
from app.models import (
    Usuario, Administrador, docente, Estudiante,
    Curso, Evento, Asistencia, Acudiente,
    Estudianteacudiente, categoria, tipoelemento,
    marca, UnidadMedida, Elemento, Movimiento, Notificacion
)

fake = Faker('es_ES')


class Command(BaseCommand):
    help = 'Generar datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generando datos de prueba...")

        # =========================
        # 1. USUARIOS
        # =========================
        usuarios = []
        for _ in range(30):
            user = Usuario.objects.create(
                email=fake.unique.email(),
                nombre=fake.name(),
                estado=True
            )
            user.set_password("123456")
            user.save()
            usuarios.append(user)

        # =========================
        # 2. ADMINISTRADORES
        # =========================
        admins = []
        for user in usuarios[:5]:
            admin = Administrador.objects.create(
                usuario=user,
                cargo=fake.job()
            )
            user.groups.add(rol_admin)
            admins.append(admin)

        # =========================
        # 3. DOCENTES
        # =========================
        docentes = []
        for user in usuarios[5:15]:
            doc = docente.objects.create(
                usuario=user,
                especialidad=fake.job()
            )
            user.groups.add(rol_docente)
            docentes.append(doc)
            
        # =========================
        # 4. CURSOS
        # =========================
        cursos = []
        grados = ['1','2','3','4','5','6','7','8','9','10','11']

        for i in range(10):
            curso = Curso.objects.create(
                grado=random.choice(grados),
                codigo=f"CUR-{i}",
                capacidad=random.randint(20, 40),
                docenteid=random.choice(docentes)
            )
            cursos.append(curso)

        # =========================
        # 5. ESTUDIANTES
        # =========================
        estudiantes = []
        for user in usuarios[15:30]:
            est = Estudiante.objects.create(
                usuario=user,
                fechaNacimiento=fake.date_of_birth(minimum_age=6, maximum_age=18),
                estadoMatricula="Matriculado",
                fechaIngreso=fake.date_this_decade(),
                cursoId=random.choice(cursos)
            )
            user.groups.add(rol_estudiante)
            estudiantes.append(est)

        # =========================
        # 6. EVENTOS
        # =========================
        eventos = []
        for _ in range(5):
            inicio = fake.date_time_this_year()
            fin = inicio + timedelta(hours=2)

            evento = Evento.objects.create(
                titulo=fake.sentence(),
                descripcion=fake.text(),
                fecha_inicio=inicio,
                fecha_fin=fin,
                creador_por=random.choice(admins)
            )
            eventos.append(evento)

        # =========================
        # 7. ASISTENCIAS
        # =========================
        for est in estudiantes:
            for _ in range(5):
                Asistencia.objects.create(
                    estudianteid=est,
                    horaentrada=fake.time(),
                    horasalida=fake.time(),
                    estado=random.choice(["A tiempo", "Tarde", "Inasistencia"]),
                    observaciones=fake.text()
                )

        # =========================
        # 8. ACUDIENTES
        # =========================
        acudientes = []
        for i in range(10):
            user = Usuario.objects.create(
                email=fake.unique.email(),
                nombre=fake.name(),
                estado=True
            )
            user.set_password("123456")
            user.save()
            user.groups.add(rol_acudiente)

            acu = Acudiente.objects.create(
                usuario=user,
                telefono=fake.phone_number(),
                direccion=fake.address()
            )
            acudientes.append(acu)

        # RELACIÓN
        for est in estudiantes:
            Estudianteacudiente.objects.create(
                estudianteId=est,
                acudienteId=random.choice(acudientes)
            )

        # =========================
        # 9. INVENTARIO
        # =========================
        categorias = [categoria.objects.create(nombre=fake.word()) for _ in range(5)]
        tipos = [tipoelemento.objects.create(nombre=fake.word()) for _ in range(5)]
        marcas = [marca.objects.create(nombre=fake.company()) for _ in range(5)]
        unidades = [UnidadMedida.objects.create(nombre=fake.word()) for _ in range(5)]

        elementos = []
        for _ in range(20):
            elem = Elemento.objects.create(
                nombre=fake.word(),
                descripcion=fake.text(),
                stockActual=random.randint(10, 100),
                stockMinimo=random.randint(1, 10),
                tipoElementoId=random.choice(tipos),
                categoriaId=random.choice(categorias),
                marcaId=random.choice(marcas),
                unidadMedidaId=random.choice(unidades),
                ubicacion=fake.city()
            )
            elementos.append(elem)

        # =========================
        # 10. MOVIMIENTOS
        # =========================
        for _ in range(30):
            Movimiento.objects.create(
                tipo=random.choice(["Absoluto", "Parcial", "Indefinido"]),
                cantidad=random.randint(1, 20),
                elementoId=random.choice(elementos),
                usuarioId=random.choice(usuarios),
                cursoId=random.choice(cursos),
                motivo=fake.text()
            )

        # =========================
        # 11. NOTIFICACIONES
        # =========================
        for _ in range(20):
            Notificacion.objects.create(
                titulo=fake.sentence(),
                mensaje=fake.text(),
                estado=random.choice(["Activo", "Inactivo"]),
                tipo=random.choice(["Aviso", "Actualización", "Otro"]),
                receptor=random.choice(usuarios),
                evento=random.choice(eventos)
            )

        self.stdout.write(self.style.SUCCESS("Datos generados correctamente"))