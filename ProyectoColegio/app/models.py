from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuario"

    def __str__(self):
        return self.nombre


class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    cargo = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
        db_table = "administrador"
        
    def __str__(self):
        return self.usuario.nombre
    
class Eventos(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    creador_por = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        db_table = "evento"
        
    def __str__(self):
        return self.titulo

      class docente (models.Model):
    id =models.OneToOneField(usuario, on_delete=models.CASCADE)
    especialidad = models.TextField()
    class Meta:
        verbose_name = "docente"
        verbose_name_plural = "docentes"
        db_table = "docente"
    def __str__ (self):
        return self.id.nombre

#creacion de modelo asistencia 
class asistencia (models.Model):
    id =models.AutoField(primary_key=True)
    estudianteid = models.ForeignKey(estudiante, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)
    horaentrada = models.TimeField ()
    horasalida = models.TimeField()
    estado = models.CharField(max_length=50)
    odsevaciones = models.TextField()
    class Meta:
        verbose_name = "asistencia"
        verbose_name_plural = "asistencias"
        db_table = "asistencia"

#creacion de modelo curso
class curso (models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    jornada =models.CharField(max_length=200)
    codigo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    fechainicio = models.DateTimeField(auto_now_add=True)
    fechafin = models.DateTimeField(auto_now=True)
    docenteid = models.ForeignKey(docente, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "curso"
        verbose_name_plural = "Cursos"
        db_table = "Curso"
    def __str__ (self):
        return self.nom 
