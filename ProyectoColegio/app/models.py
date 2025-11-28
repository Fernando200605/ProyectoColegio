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
  #creacion de modelo curso
class Curso (models.Model):
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
class categoria(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = "categoria"

    def __str__(self):
        return self.nombre
    
class tipoelemento(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "tipoelemento"
        verbose_name_plural = "tipoelementos"
        db_table = "tipoelemento"

    def __str__(self):
        return self.nombre
    
class marca(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"
        db_table = "marca"
    def __str__(self):
        return self.nombre
 
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
        db_table = "unidadmedida"

    def __str__(self):
        return self.nombre
class Elemento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    stockActual = models.IntegerField()
    stockMinimo = models.IntegerField()
    tipoElementoId = models.ForeignKey(tipoelemento, on_delete=models.CASCADE)
    categoriaId = models.ForeignKey(categoria, on_delete=models.CASCADE)
    marcaId = models.ForeignKey(marca, on_delete=models.CASCADE)
    unidadMedidaId = models.ForeignKey(Unidadmedida, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaActualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Elemento"
        verbose_name_plural = "Elementos"
        db_table = "elemento"


class Movimiento(models.Model):
    tipo = models.CharField(max_length=50)
    fecha = models.DateTimeField()
    cantidad = models.IntegerField()
    elementoId = models.ForeignKey(Elemento, on_delete=models.CASCADE)
    usuarioId = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cursoId = models.ForeignKey(Curso, on_delete=models.CASCADE)
    motivo = models.TextField()
    
    class Meta:
        verbose_name= 'Movimiento'
        verbose_name_plural= 'Movimiento'
        db_table= 'movimiento'

    def __str__(self):
        return self.tipo
class notificacion(models.Model):
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50)
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        db_table = "notificacion"

    def __str__(self):
        return self.titulo

