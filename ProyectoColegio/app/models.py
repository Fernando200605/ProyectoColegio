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