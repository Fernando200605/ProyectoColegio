from django.db import models

# Create your models here.
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

