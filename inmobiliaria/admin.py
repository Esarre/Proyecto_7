from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioCreationForm
from .models import *
from .forms import *

# Register your models here.


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'rut', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nac', 'telefono', 'email', 'tipo_usuario', 'password1', 'password2'),
        }),
    )
    
    list_display = ('username', 'rut', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nac', 'telefono', 'email', 'fecha_creacion', 'fecha_modificacion', 'tipo_usuario')
    search_fields = ('username', 'rut', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nac', 'telefono', 'email', 'fecha_creacion', 'fecha_modificacion', 'tipo_usuario', 'tipo_usuario__tipo',)

    def get_inmuebles_solicitados(self, obj):
        return ", ".join([str(inmueble) for inmueble in obj.inmuebles_solicitados.all()])

    get_inmuebles_solicitados.short_description = 'Inmuebles Solicitados'


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'n_habitaciones', 'n_banios', 'n_estacionamientos', 'precio', 'fecha_creacion', 'fecha_modificacion', 'tipo_inmueble', 'arrendador_usuario')
    search_fields = ('nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'n_habitaciones', 'n_banios', 'n_estacionamientos', 'precio', 'fecha_creacion', 'fecha_modificacion', 'tipo_inmueble', 'arrendador_usuario', 'tipo_inmueble__tipo', 'arrendador_usuario__rut', 'arrendador_usuario__primer_nombre', 'arrendador_usuario__segundo_nombre', 'arrendador_usuario__apellido_paterno', 'arrendador_usuario__apellido_materno', 'arrendador_usuario__fecha_nac', 'arrendador_usuario__telefono', 'arrendador_usuario__email', 'arrendador_usuario__fecha_creacion', 'arrendador_usuario__fecha_modificacion', 'arrendador_usuario__tipo_usuario__tipo',)


@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'inmueble_id', 'fecha_solicitud', 'estado')
    search_fields = ('usuario', 'inmueble', 'fecha_solicitud', 'estado', 'usuario__rut', 'inmueble__nombre')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region',)
    search_fields = ('region',)


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('comuna', 'region')
    search_fields = ('comuna', 'region', 'region__region',)


@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('imagen_thumbnail', 'inmueble_nombre', 'fecha_creacion', 'fecha_modificacion')
    search_fields = ('inmueble__nombre', 'fecha_creacion', 'fecha_modificacion')

    def imagen_thumbnail(self, obj):
        return '<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.imagen.url)

    imagen_thumbnail.allow_tags = True
    imagen_thumbnail.short_description = 'Thumbnail'

    def inmueble_nombre(self, obj):
        return obj.inmueble.nombre

    inmueble_nombre.short_description = 'Inmueble'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('inmueble')


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    form = DireccionForm
    list_display = ('calle', 'numero', 'numero_departamento', 'fecha_creacion', 'inmueble', 'region', 'comuna')
    search_fields = ('calle', 'numero', 'numero_departamento', 'fecha_creacion', 'inmueble', 'region', 'comuna', 'region__regiones', 'comuna__comuna',)

    class Media:
        js = ('assets/js/admin_custom.js',)  # Buscamos el archivo js que contiene el código para listar las comunas en base a la región seleccionada

