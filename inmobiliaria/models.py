from django.contrib.auth.models import AbstractUser
from django.db import models
#from django.dispatch import receiver
import uuid
#from django.db.models.signals import pre_delete
#from django.core.exceptions import ValidationError

# Create your models here.


class Usuario(AbstractUser):
    tipo_choices = [
        ('administrador', 'Administrador'),
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]

    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=9, unique=True)
    primer_nombre = models.CharField(max_length=15, blank=False, null=False)
    segundo_nombre = models.CharField(max_length=15, blank=False, null=False)
    apellido_paterno = models.CharField(max_length=15, blank=False, null=False)
    apellido_materno = models.CharField(max_length=15, blank=False, null=False)
    fecha_nac = models.DateField()
    telefono = models.PositiveIntegerField(blank=False, null=False, unique=True)
    email = models.EmailField(max_length=30, blank=False, null=False, unique=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(auto_now=True)
    tipo_usuario = models.CharField(max_length=15, choices=tipo_choices)
    inmuebles_solicitados = models.ManyToManyField('Inmueble', through='SolicitudArriendo', related_name='solicitantes')

    # Define related_name personalizados para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='custom_user_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='custom_user_permissions',
        blank=True,
    )

    def __str__(self) -> str:
        return f"RUT: {self.rut}, {self.primer_nombre} {self.apellido_paterno} {self.apellido_materno}, {self.tipo_usuario}, teléfono: {self.telefono}, email: {self.email}"
    

class Inmueble(models.Model):
    tipo_choices = [
        ('Casa', 'Casa'),
        ('Departamento', 'Departamento'),
        ('Parcela', 'Parcela'),
    ]

    nombre = models.CharField(max_length=40, blank=False, null=False)
    descripcion = models.TextField(blank=False, null=False)
    m2_construidos = models.PositiveIntegerField(blank=False, null=False)
    m2_totales = models.PositiveIntegerField(blank=False, null=False)
    n_habitaciones = models.PositiveBigIntegerField(blank=False, null=False)
    n_banios = models.PositiveIntegerField(blank=False, null=False)
    n_estacionamientos = models.PositiveIntegerField(blank=False, null=False)
    precio = models.PositiveIntegerField(blank=False, null=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(auto_now=True)
    tipo_inmueble = models.CharField(max_length=15, choices=tipo_choices)
    disponible = models.BooleanField(default=True)
    arrendador_usuario = models.ForeignKey(Usuario, related_name='arrendador_usuario', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.nombre}, m2 constr: {self.m2_construidos}, m2 totales: {self.m2_totales}, precio: {self.precio}, tipo: {self.tipo_inmueble}"


class Imagen(models.Model):
    imagen = models.ImageField(upload_to='Inmuebles/')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_modificacion = models.DateField(auto_now=True)
    inmueble = models.ForeignKey(Inmueble, related_name='imagenes', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.imagen)


class SolicitudArriendo(models.Model):
    estado_choices = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('terminada', 'Terminada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=estado_choices)

    def __str__(self) -> str:
        return f"Usuario: {self.usuario}, Inmueble: {self.inmueble}, Estado: {self.estado}"


class Region(models.Model):
   region = models.CharField(max_length=50, unique=True)

   def __str__(self) -> str:
       return self.region
       

class Comuna(models.Model):
    comuna = models.CharField(max_length=50, unique=True, blank=False, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comuna
    

class Direccion(models.Model):
    calle = models.CharField(max_length=50, blank=False, null=False)
    numero = models.CharField(max_length=10, blank=False, null=False)
    numero_departamento = models.CharField(max_length=10, blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    inmueble = models.OneToOneField(Inmueble, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.calle} {self.numero}, dpto: {self.numero_departamento}, región: {self.region}, comuna: {self.comuna}"


class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()

    def __str__(self) -> str:
        return self.customer_name


"""
# Evita el borrado de una dirección; el problema es que utilizarlo genera que no se puedan eliminar usuarios y tampoco inmuebles; menos direcciones, generando un bucle
@receiver(pre_delete, sender=Direccion)
def prevent_delete_direccion_with_inmueble(sender, instance, **kwargs):
    if instance.inmueble:
        raise ValidationError("No se puede eliminar la dirección porque está asociada a un inmueble.")
"""