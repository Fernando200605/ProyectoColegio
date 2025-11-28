from django.db import models



# Create your models here.

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE,primary_key=True)
    codigo = models.TextField(max_length=50, null=True, blank=True, verbose_name="Codigo")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    estadoMatricula = models.TextField(max_length=20, null=True, blank=True, verbose_name="Estado de Matricula")
    fechaIngreso = models.DateField(verbose_name="Fecha de Ingreso")
    cursoId = models.ForeignKey(Curso,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.usuario.nombre
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes" 
        db_table = "Estudiante"

class Acudiente(models.Model):
    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE,primary_key=True)
    telefono = models.TextField(max_length=10, null=True, blank=True, verbose_name="Telefono")
    direccion = models.TextField(max_length=150, null=True, blank=True, verbose_name="Direccion")

    def __str__(self):
        return self.usuario.nombre
    
    class Meta:
        verbose_name = "Acudiente"
        verbose_name_plural = "Acudientes" 
        db_table = "Acudiente"

class Estudianteacudiente(models.Model):
    estudianteId = models.ForeignKey(Estudiante,on_delete=models.CASCADE)
    acudienteId = models.ForeignKey(Acudiente,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.estudianteId.usuario.nombre, self.acudienteId.usuario.nombre
    
    class Meta:
        verbose_name = "Estudianteacudiente"
        verbose_name_plural = "Estudianteacudientes" 
        db_table = "Estudianteacudiente"