from django.shortcuts import render, redirect, get_object_or_404
#from dal import autocomplete
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from .models import *
from .forms import *

# Create your views here.


# Vista del index, donde se mosrtarán los inmuebles disponibles
class VistaIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtén los parámetros de búsqueda
        region_id = self.request.GET.get('region') #
        comuna_id = self.request.GET.get('comuna') #

        inmuebles = Inmueble.objects.filter(disponible=True)
        #print("Inmuebles:", inmuebles)  # Mensaje de depuración
        
        if region_id:
            inmuebles = inmuebles.filter(direccion__comuna__region_id=region_id) #
        if comuna_id:
            inmuebles = inmuebles.filter(direccion__comuna_id=comuna_id) #

        context['inmuebles'] = inmuebles
        context['regiones'] = Region.objects.all() #
        context['comunas'] = Comuna.objects.all() #
        return context

# Vista que mostrará la información del inmueble a un usuario arrendatario interesado (cuando clickee en "ver detalles" de un inmueble del index)
@login_required(login_url='/login_required/')
def detalles_inmueble(request, pk):
    user = request.user
    
    if user.tipo_usuario != 'arrendatario':
        return render(request, 'login_required.html')
    
    inmueble = get_object_or_404(Inmueble, pk=pk)
    return render(request, 'property_details.html', {'inmueble': inmueble})
    

# Vista para renderizar el login required (esto cuando un usuario no registrado (o del tipo arrendador) intente ir a ver los detalles de un inmueble en el index)
class VistaLoginRequired(TemplateView):
    template_name = 'login_required.html'

"""
class VistaLogin(TemplateView):
    template_name = 'registration/login.html'
"""

# Vista para iniciar sesión en la página
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('session_on')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# Vista para renderizar session_on (al iniciar sesión)
class VistaInicioSesion(TemplateView):
    template_name = 'session_on.html'


# Vista para cerrar sesión
def user_logout(request):
    logout(request)
    return redirect('logged_out_view')


# Renderiza la vista con mensaje de cierre de sesión exitoso
def logged_out_view(request):
    return render(request, 'registration/logged_out.html')


# Vista para el formulario de registro
def vista_registro(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('registro_exitoso')
    else:
            form = UsuarioCreationForm()
    return render(request, 'registration.html', {'form': form})


# Vista para renderizar mensaje de éxito al registrarse
class VistaRegistroExito(TemplateView):
    template_name = 'registration_success.html'


# Vista para mostrar y actualizar información personal del usuario registrado (datos personales y modificar contraseña)
@login_required
def user_account(request):
    if request.method == 'POST':
        if 'update_info' in request.POST:
            user_form = UsuarioUpdateForm(request.POST, instance=request.user)
            password_form = CustomPasswordChangeForm(request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Tu información personal ha sido actualizada con éxito.')
                #return redirect('mi_cuenta')
        elif 'change_password' in request.POST:
            user_form = UsuarioUpdateForm(instance=request.user)
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()  # Se guarda la nueva contraseña en la BD
                update_session_auth_hash(request, user)  # Se actualiza la sesión del usuario, pero aplicando los cambios efectuados en la constraseña. Así, la sesión del usuario se mantiene abierta
                messages.success(request, 'Contraseña actualizada con éxito.')
                #return redirect('password_success')
    else:
        user_form = UsuarioUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'account.html', {'usuario': request.user, 'user_form': user_form, 'password_form': password_form})


# Vista para renderizar mensaje de éxito al cambiar contraseña
class VistaCambioPass(TemplateView):
    template_name = 'password_success.html'


# Vista para solicitudes de arriendo (solo usuarios tipo arrendatario):
@login_required
def gestionar_solicitudes(request):
    user = request.user
    # Verifica si el usuario es del tipo 'arrendatario'
    if user.tipo_usuario != 'arrendatario':
        raise PermissionDenied
    
    # Obtener todas las solicitudes de arriendo del usuario arrendatario (sin incluír las terminadas)
    solicitudes = SolicitudArriendo.objects.filter(usuario=user, estado__in=['pendiente', 'aceptada', 'rechazada'])

    return render(request, 'request_management.html', {'solicitudes': solicitudes})


# Vista para cancelar una solicitud
@login_required
def cancelar_solicitud(request, solicitud_id):
    user = request.user
    if user.tipo_usuario != 'arrendatario':
        raise PermissionDenied
    
    solicitud = get_object_or_404(SolicitudArriendo, id=solicitud_id, usuario=user)
    
    # Cambia el estado de la solicitud a 'cancelada'
    solicitud.delete()
    
    # Redirige de vuelta a la página de gestión de solicitudes
    return redirect('request_management')



# Vista para inmuebles (solo usuarios tipo arrendador):
@login_required
def gestionar_inmuebles(request):
    user = request.user

    # Verifica si el usuario es del tipo 'arrendador'
    if user.tipo_usuario != 'arrendador':
        raise PermissionDenied
    
    limite_img = 6
    
    if request.method == 'POST':
        form_inmueble = InmuebleCreateForm(request.POST, request.FILES)
        form_direccion = DireccionForm(request.POST, request.FILES)

        if form_inmueble.is_valid() and form_direccion.is_valid():
            imagenes = request.FILES.getlist('imagenes')
            if len(imagenes) > limite_img:
                messages.error(request, f'Solo se permite subir un máximo de {limite_img} imágenes.')
            else:
                inmueble = form_inmueble.save(commit=False)
                inmueble.arrendador_usuario = request.user
                inmueble.save()

                direccion = form_direccion.save(commit=False)
                direccion.inmueble = inmueble
                direccion.save()

                # Manejar imágenes que el usuario debe subir al crear la propiedad:
                for file in request.FILES.getlist('imagenes'):
                    Imagen.objects.create(inmueble=inmueble, imagen=file)

                messages.success(request, "Inmueble agregado con éxito.")
                return redirect('property_management')
    else:
        form_inmueble = InmuebleCreateForm()
        form_direccion = DireccionForm()

    # Obtener los inmuebles que ha agregado el usuario a la BD:
    inmuebles_usuario = Inmueble.objects.filter(arrendador_usuario=user)

    return render(request, 'property_management.html', {'form_inmueble': form_inmueble, 'form_direccion': form_direccion, 'inmuebles_usuario': inmuebles_usuario})


"""
# Código de depuración para buscar el error
@login_required
def gestionar_inmuebles(request):
    user = request.user

    # Verifica si el usuario es del tipo 'arrendador'
    if user.tipo_usuario != 'arrendador':
        raise PermissionDenied

    if request.method == 'POST':
        form_inmueble = InmuebleCreateForm(request.POST, request.FILES)
        form_direccion = DireccionForm(request.POST, request.FILES)

        # Imprimir errores de formulario si no son válidos
        if not form_inmueble.is_valid():
            print("Errores en form_inmueble:", form_inmueble.errors)
        if not form_direccion.is_valid():
            print("Errores en form_direccion:", form_direccion.errors)

        if form_inmueble.is_valid() and form_direccion.is_valid():
            inmueble = form_inmueble.save(commit=False)
            inmueble.arrendador_usuario = request.user
            inmueble.save()

            # Crear la dirección usando los datos del formulario
            direccion_data = form_direccion.cleaned_data
            direccion = Direccion(
                inmueble=inmueble,
                calle=direccion_data['calle'],
                numero=direccion_data['numero'],
                numero_departamento=direccion_data.get('numero_departamento'),
                region=direccion_data['region'],
                comuna=direccion_data['comuna']
            )
            direccion.save()

            # Manejar imágenes que el usuario debe subir al crear la propiedad:
            for file in request.FILES.getlist('imagenes'):
                Imagen.objects.create(inmueble=inmueble, imagen=file)

            messages.success(request, "Inmueble agregado con éxito.")
            return redirect('index')
        else:
            # Retornar errores de validación en la respuesta para depuración
            return HttpResponse(f"Errores en formularios: {form_inmueble.errors}, {form_direccion.errors}")
    else:
        form_inmueble = InmuebleCreateForm()
        form_direccion = DireccionForm()

    return render(request, 'property_management.html', {'form_inmueble': form_inmueble, 'form_direccion': form_direccion})
"""


# Lógica para borrar una propiedad:
@login_required
def eliminar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    if request.user != inmueble.arrendador_usuario:
        raise PermissionDenied

    inmueble.delete()
    messages.success(request, "Inmueble eliminado con éxito.")
    return redirect('property_management')


# Lógica para actualizar la información de una propiedad:
@login_required
def actualizar_propiedad(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    if request.user != inmueble.arrendador_usuario:
        raise PermissionDenied
    
    limite_img = 6

    if request.method == 'POST':
        form_inmueble = InmuebleCreateForm(request.POST, request.FILES, instance=inmueble)
        form_direccion = DireccionForm(request.POST, instance=inmueble.direccion)

        if form_inmueble.is_valid() and form_direccion.is_valid():
            imagenes = request.FILES.getlist('imagenes')
            imagenes_existentes = inmueble.imagenes.count()

            # Verificar si la cantidad total de imágenes (existentes + nuevas) excede el límite
            if imagenes_existentes + len(imagenes) > limite_img:
                messages.error(request, f'No se pueden subir más de {limite_img} imágenes en total. Si deseas reemplazar alguna imagen, primero borra la imagen a reemplazar.')
            else:
                form_direccion.save()
                form_inmueble.save()

                # actualizar también las imágenes:
                    # Primero borraremos las imágenes existentes:
                #inmueble.imagenes.all().delete()

                # Subir nuevas imágenes:
                for imagen in request.FILES.getlist('imagenes'):
                    inmueble.imagenes.create(imagen=imagen)

                # Eliminar imágenes seleccionadas para borrar
                imagenes_a_eliminar = request.POST.getlist('imagenes_a_eliminar')
                Imagen.objects.filter(id__in=imagenes_a_eliminar).delete()

                messages.success(request, "Inmueble actualizado con éxito.")
                return redirect('property_management')
    else:
        form_inmueble = InmuebleCreateForm(instance=inmueble)
        form_direccion = DireccionForm(instance=inmueble.direccion)

    # Obtener imágenes asociadas al inmueble para poder mostrárselas al usuario en el template:
    imagenes = Imagen.objects.filter(inmueble=inmueble)

    return render(request, 'update_property.html', {
        'form_inmueble': form_inmueble,
        'form_direccion': form_direccion,
        'imagenes': imagenes,
        'inmueble': inmueble
    })

# Vista para borrar una imagen en actualizar_propiedad:
@login_required
def eliminar_imagen(request, inmueble_id):
    if request.method == 'POST':
        imagen_id = request.POST.get('imagen_id')
        try:
            imagen = Imagen.objects.get(id=imagen_id, inmueble_id=inmueble_id)
            if request.user != imagen.inmueble.arrendador_usuario:
                return HttpResponseForbidden()
            imagen.delete()
            messages.success(request, "Imagen eliminada con éxito.")
        except Imagen.DoesNotExist:
            messages.error(request, "Imagen no encontrada.")
    return redirect('update_property', pk=inmueble_id)


# Vista para realizar solicitud de arriendo (usuario Arrendatario):
@login_required
def enviar_solicitud(request, pk):
    user = request.user
    # Verifica si el usuario es del tipo 'arrendatario'
    if user.tipo_usuario != 'arrendatario':
        raise PermissionDenied

    inmueble = get_object_or_404(Inmueble, pk=pk)
    #arrendatario = inmueble.arrendador_usuario

    # Verifica si ya existe una solicitud pendiente para este inmueble y usuario
    solicitud_existente = SolicitudArriendo.objects.filter(usuario=user, inmueble=inmueble, estado='pendiente').exists()
    if not solicitud_existente:
        SolicitudArriendo.objects.create(usuario=user, inmueble=inmueble, estado='pendiente')

    return redirect('request_success')    #'property_details', pk=pk


# Vista que renderiza mensaje de éxito al postular a la vivienda 
class VistaRequestSuccess(TemplateView):
    template_name = 'request_success.html'


# Vista para gestionar las solicitudes de arriendo (usuario Arrendador):
@login_required
def gestionar_solicitudes_inmueble(request):
    user = request.user
    # Verifica si el usuario es del tipo 'arrendador'
    if user.tipo_usuario != 'arrendador':
        raise PermissionDenied

    # Obtener todos los inmuebles del usuario arrendador
    inmuebles = Inmueble.objects.filter(arrendador_usuario=user)

    # Obtener todas las solicitudes de arriendo para esos inmuebles
    solicitudes_activas = SolicitudArriendo.objects.filter(inmueble__in=inmuebles, estado='pendiente')   #inmueble__arrendador_usuario=user
    solicitudes_aceptadas = SolicitudArriendo.objects.filter(inmueble__in=inmuebles, estado='aceptada')

    return render(request, 'property_request_management.html', {'solicitudes_activas': solicitudes_activas, 'solicitudes_aceptadas': solicitudes_aceptadas})


# Vista para cambiar el estado de una solicitud (usuario Arrendador):
@login_required
@require_POST
def cambiar_estado_solicitud(request, solicitud_id):
    user = request.user
    solicitud = get_object_or_404(SolicitudArriendo, id=solicitud_id)

    # Verifica si el usuario es el arrendador del inmueble
    if solicitud.inmueble.arrendador_usuario != user:
        raise PermissionDenied

    # Cambiar el estado de la solicitud
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        #if nuevo_estado in dict(SolicitudArriendo.estado_choices):
        #    solicitud.estado = nuevo_estado
        #    solicitud.save()
        if nuevo_estado == 'rechazada':
            solicitud.delete()    # Eliminamos la solicitud si es rechazada por el usuario arrendador
            #messages.info(request, f"Tu solicitud para el inmueble '{solicitud.inmueble.nombre}' ha sido rechazada por el propietario del inmueble.")    # Notificar del rechazo al usuario arrendatario
        elif nuevo_estado == 'aceptada':
            solicitud.estado = nuevo_estado
            solicitud.save()
            solicitud.inmueble.disponible = False    # Con este ajuste, vamos a ocultar la oferta para otros usuarios arrendatarios del sistema
            solicitud.inmueble.save()
            #messages.info(request, f"Tu solicitud para el inmueble '{solicitud.inmueble.nombre}' ha sido aceptada.")    # Notificamos al arrendatario de que le aceptaron la solicitud
        else:
            solicitud.estado = nuevo_estado
            solicitud.save()
    return redirect('property_request_management')


# Vista para terminar relación de arriendo
@login_required
def terminar_relacion(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArriendo, id=solicitud_id)
    user = request.user

    # Verifica si el usuario es el arrendador del inmueble
    if solicitud.inmueble.arrendador_usuario != user:
        raise PermissionDenied

    # Actualiza el estado de la solicitud a 'terminada'. No la borra de la BD para que quede el registro
    solicitud.estado = 'terminada'
    solicitud.save()

    # Actualiza el estado del inmueble para que vuelva a estar disponible
    solicitud.inmueble.disponible = True
    solicitud.inmueble.save()

    return redirect('property_request_management')


# Vista para cargar las comunas en base a la región seleccionada
def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'comuna')
    return JsonResponse(list(comunas), safe=False)


# Vista para el envío de un formulario de contacto:
def contacto(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            return redirect('contact_success')
    else:
        form = ContactFormForm()
    return render(request, 'contact.html', {'form': form})

class VistaContactoExito(TemplateView):
    template_name = 'contact_success.html'

class VistaSobreNosotros(TemplateView):
    template_name = 'about.html'



