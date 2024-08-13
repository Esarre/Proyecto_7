#from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('obtener_comunas/', obtener_comunas, name='obtener_comunas'),
    path('', VistaIndex.as_view(), name='index'),
    path('registration/', vista_registro, name='registration'),
    path('registration_success/', VistaRegistroExito.as_view(), name='registro_exitoso'),
    path('login/', login_user, name='login'),
    path('logout/', user_logout, name='logout'),
    path('session_off/', logged_out_view, name='logged_out_view'),
    path('account/', user_account, name='account'),
    path('change_password_success/', VistaCambioPass.as_view(), name='password_success'),
    path('request_management/', gestionar_solicitudes, name='request_management'),
    path('property_management', gestionar_inmuebles, name='property_management'),
    path('session_on/', VistaInicioSesion.as_view(), name='session_on'),
    path('contact/', contacto, name='contact'),
    path('contact_success/', VistaContactoExito.as_view(), name='contact_success'),
    path('about/', VistaSobreNosotros.as_view(), name='about'),
    path('update_property/<int:pk>/', actualizar_propiedad, name='update_property'),
    path('delete_property/<int:pk>/', eliminar_inmueble, name='delete_property'),
    path('delete_image/<int:inmueble_id>/', eliminar_imagen, name='delete_image'),
    path('property_details/<int:pk>/', detalles_inmueble, name='property_details'),
    path('login_required/', VistaLoginRequired.as_view(), name='login_required'),
    path('send_request/<int:pk>/', enviar_solicitud, name='send_request'),
    path('request_success/', VistaRequestSuccess.as_view(), name='request_success'),
    path('property_request_management/', gestionar_solicitudes_inmueble, name='property_request_management'),
    path('change_request_status/<int:solicitud_id>/', cambiar_estado_solicitud, name='change_request_status'),
    path('end_rental/<int:solicitud_id>/', terminar_relacion, name='end_rental'),
    path('cancel_request/<int:solicitud_id>/', cancelar_solicitud, name='cancel_request'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




"""
Hay 2 formas (al menos) para expresar:

1. Primera forma (usada cuando trabajamos en DEBUG, o sea, en un entorno de desarrollo
   y no de producción. Por lo tanto, mientras 'settings.DEBUG' sea True, se incorporarán
   imágenes):

urlpatterns = [
    # tus otras rutas
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


2. Segunda forma (usada para incorporar imágenes tanto en desarrollo como producción):  

urlpatterns = [
    # tus otras rutas
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""