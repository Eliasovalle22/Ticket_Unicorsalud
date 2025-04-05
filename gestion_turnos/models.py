from django.db import models
from django.contrib.auth.models import User

# Modelo para Estudiantes
class Estudiante(models.Model):
    codigo = models.CharField(max_length=20, unique=True)  # Código de estudiante
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    class Meta:
        db_table = 'estudiantes'  # Nombre de la tabla en la base de datos
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.codigo})"
    
    

# Modelo para Personal de Soporte
class PersonalSoporte(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Vinculado a usuario de Django
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    class Meta:
        db_table = 'soporte'  # Nombre de la tabla en la base de datos
        verbose_name = "Soporte"
        verbose_name_plural = "Soportes"

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"



# Modelo para Turnos
class Turno(models.Model):
    ESTADOS = (
        ('en_espera', 'En espera'),
        ('atendido', 'Atendido'),
        ('finalizado', 'Finalizado'),
    )
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tipo_turno = models.CharField(max_length=50)  # Ejemplo: "Inscripción", "Consulta"
    motivo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_espera')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_atencion = models.DateTimeField(null=True, blank=True)
    atendido_por = models.ForeignKey(PersonalSoporte, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'turnos'
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return f"Turno {self.id} - {self.estudiante} ({self.estado})"

# Modelo para Notificaciones
class Notificacion(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    class Meta:
        db_table = 'notificaciones'
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
    
    def __str__(self):
        return f"Notificación para {self.turno.estudiante} - {self.fecha}"