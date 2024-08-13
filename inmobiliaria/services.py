from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .models import *

def crear_usuario(username, rut, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, fecha_nac, telefono, email, tipo_usuario):
    try:
        if len(rut) < 8 or len(rut) > 9:
            raise IntegrityError("El rut del profesor debe tener 8 o 9 dígitos. No incorpore puntos ni guión")
        usuario = Usuario.objects.create(username=username, rut=rut, primer_nombre=primer_nombre, segundo_nombre=segundo_nombre, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, fecha_nac=fecha_nac, telefono=telefono, email=email, tipo_usuario=tipo_usuario)
        return usuario
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except IntegrityError as e:
        print(f"\nError: {str(e)}.\n")
    except ValidationError:
        print('\nError: El formato de la fecha debe ser "AA-MM-DD".\n')
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el usuario: {str(e)}\n")


def obtener_usuario(rut):
    try:
        usuario = Usuario.objects.get(rut=rut)
        return usuario
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except Exception as e:
        print(f"\nHa ocurrido un error al obtener el usuario: {str(e)}\n")


def borrar_usuario(rut):
    try:
        usuario = Usuario.objects.get(rut=rut)
        usuario.delete()
        return f"Usuario eliminado de la base de datos"
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al borrar el usuario: {str(e)}\n")


def listar_usuarios_arrendador():
    try:
        arrendadores = Usuario.objects.filter(tipo_usuario='arrendador')
        return list(arrendadores)
    except Exception as e:
        print(f"\nHa ocurrido un error al listar usuarios tipo arrendador: {str(e)}\n")


def listar_usuarios_arrendatario():
    try:
        arrendatarios = Usuario.objects.filter(tipo_usuario='arrendatario')
        return list(arrendatarios)
    except Exception as e:
        print(f"\nHa ocurrido un error al listar usuarios tipo arrendatario: {str(e)}\n")


def crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, n_habitaciones, n_banios, n_estacionamientos, precio, tipo_inmueble, rut):
    try:
        usuario = Usuario.objects.get(rut=rut)
        inmueble = Inmueble.objects.create(nombre=nombre, descripcion=descripcion, m2_construidos=m2_construidos, m2_totales=m2_totales, n_habitaciones=n_habitaciones, n_banios=n_banios, n_estacionamientos=n_estacionamientos, precio=precio, tipo_inmueble=tipo_inmueble, arrendador_usuario=usuario)
        return inmueble
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")
    

def obtener_inmuebles_arrendador(rut):
    try:
        usuario = Usuario.objects.get(rut=rut)
        inmuebles = Inmueble.objects.filter(arrendador_usuario=usuario)
        lista_inmuebles = [str(inmueble) for inmueble in inmuebles]
        return lista_inmuebles
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut}' no se encuentra en la base de datos o no pertenece a un usuario arrendador\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")


def borrar_inmueble(id):
    try:
        inmueble = Inmueble.objects.get(id=id)
        inmueble.delete()
        return f"El inmueble ha sido eliminado de la base de datos"
    except Inmueble.DoesNotExist:
        print(f"\nError: El id de inmueble ingresado: '{id}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")


def obtener_inmueble(id):
    try:
        inmueble = Inmueble.objects.get(id=id)
        return inmueble
    except Inmueble.DoesNotExist:
        print(f"\nError: El id de inmueble ingresado: '{id}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")


def crear_direccion_inmueble(calle, numero, numero_departamento, inmueble_id, region_nombre, comuna_nombre):
    try:
        inmueble = Inmueble.objects.get(id=inmueble_id)
        region = Region.objects.get(region=region_nombre)
        comuna = Comuna.objects.get(comuna=comuna_nombre)
        direccion = Direccion.objects.create(calle=calle, numero=numero, numero_departamento=numero_departamento, inmueble=inmueble, region=region, comuna=comuna)
        return direccion
    except ValidationError as e:
        print(f'\nError: Debes ingresar el nombre de una región y/o comuna\n')
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")


def obtener_direccion_inmueble(id_direccion):
    try:
        direccion = Direccion.objects.get(id=id_direccion)
        inmueble = direccion.inmueble
        return f"{direccion}, inmueble asociado: {inmueble}"
    except Direccion.DoesNotExist:
        print(f"\nError: El id de dirección ingresado: '{id_direccion}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")


def crear_solicitud_arriendo(rut_solicitante, inmueble_id, estado):
    try:
        usuario = Usuario.objects.get(rut=rut_solicitante)
        if usuario.tipo_usuario == 'arrendatario':
            inmueble = Inmueble.objects.get(id=inmueble_id)
            solicitud = SolicitudArriendo.objects.create(usuario=usuario, inmueble=inmueble, estado=estado)
            return solicitud
        else:
            print("Error: Se aceptan solo usuarios del tipo Arrendatario")
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut_solicitante}' no se encuentra en la base de datos.\n")
    except Inmueble.DoesNotExist:
        print(f"\nError: El id de inmueble ingresado: '{inmueble_id}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al crear el inmueble: {str(e)}\n")


def obtener_solicitudes_arrendatario(rut_solicitante):
    try:
        arrendatario = Usuario.objects.get(rut=rut_solicitante)
        solicitudes = SolicitudArriendo.objects.filter(usuario=arrendatario)
        lista_solicitudes = [str(solicitud) for solicitud in solicitudes]
        return lista_solicitudes
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut_solicitante}' no se encuentra en la base de datos\n")
    except SolicitudArriendo.DoesNotExist:
        print(f"\nNo hay solicitudes asociadas al arrendatario con rut: {rut_solicitante}.\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al obtener las solicitudes del arrendatario: {str(e)}\n")


def obtener_solicitudes_arrendador(rut_arrendador):
    try:
        arrendador = Usuario.objects.get(rut=rut_arrendador)
        inmuebles = Inmueble.objects.filter(arrendador_usuario=arrendador)
        solicitudes = SolicitudArriendo.objects.filter(inmueble__in=inmuebles)
        return list(solicitudes)
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut_arrendador}' no se encuentra en la base de datos\n")
    except Inmueble.DoesNotExist:
        print(f"\nNo hay inmuebles asociados al rut: {rut_arrendador}.\n")
    except SolicitudArriendo.DoesNotExist:
        print(f"\nNo hay solicitudes asociadas al inmueble: {inmuebles}.\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al obtener las solicitudes del arrendador: {str(e)}\n")


def modificar_datos_usuario(rut, nuevo_telefono, nuevo_email):
    try:
        usuario = Usuario.objects.get(rut=rut)
        usuario.telefono = nuevo_telefono
        usuario.email = nuevo_email
        usuario.save()
        return usuario
    except Usuario.DoesNotExist:
        print(f"\nError: El rut de usuario ingresado: '{rut}' no se encuentra en la base de datos.\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al modificar los datos del usuario: {str(e)}\n")


def modificar_datos_inmueble(id_inmueble, nueva_descripcion, nuevo_precio):
    try:
        inmueble = Inmueble.objects.get(id=id_inmueble)
        inmueble.descripcion = nueva_descripcion
        inmueble.precio = nuevo_precio
        inmueble.save()
        return inmueble
    except Inmueble.DoesNotExist:
        print(f"\nError: El id de inmueble ingresado: '{id_inmueble}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al modificar los datos del inmueble: {str(e)}\n")


def modificar_solicitud(id_solicitud, nuevo_estado):
    try:
        solicitud = SolicitudArriendo.objects.get(id=id_solicitud)
        #inmueble = solicitud.inmueble
        solicitud.estado = nuevo_estado
        return solicitud
    except SolicitudArriendo.DoesNotExist:
        print(f"\nError: El id de solicitud ingresado: '{id_solicitud}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al modificar la solicitud: {str(e)}\n")


def borrar_solicitud_arriendo(id_solicitud):
    try:
        solicitud = SolicitudArriendo.objects.get(id=id_solicitud)
        solicitud.delete()
        return f"La solicitud de arriendo ha sido eliminada de la base de datos"
    except SolicitudArriendo.DoesNotExist:
        print(f"\nError: El id de solicitud ingresado: '{id_solicitud}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al borrar la solicitud: {str(e)}\n")


def obtener_solicitud_arriendo(id_solicitud):
    try:
        solicitud = SolicitudArriendo.objects.get(id=id_solicitud)
        return solicitud
    except SolicitudArriendo.DoesNotExist:
        print(f"\nError: El id de solicitud ingresado: '{id_solicitud}' no se encuentra en la base de datos\n")
    except NameError as e:
        print(f"Error lógico: {str(e)}")
    except TypeError as e:
        print(f"\nError: No has proporcionado todos los argumentos requeridos: {str(e)}\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al modificar la solicitud: {str(e)}\n")


def listar_solicitudes_arriendo():
    try:
        solicitudes = SolicitudArriendo.objects.all()
        return list(solicitudes)
    except Exception as e:
        print(f"\nHa ocurrido un error al listar las solicitudes de arriendo: {str(e)}\n")


def listar_direcciones():
    try:
        direcciones = Direccion.objects.all()
        return list(direcciones)
    except Exception as e:
        print(f"\nHa ocurrido un error al listar las direcciones: {str(e)}\n")


# LÓGICA NO UTILIZADA (ver comentario en models.py) Debería saltar un error, ya que se definió una señal para evitar borrar una dirección mientras esté asociada a un inmueble (revisar la clase Direccion en models.py)
def borrar_direccion(id):
    try:
        direccion = Direccion.objects.get(id=id)
        direccion.delete()
        return f"La dirección ha sido eliminada de la base de datos"
    except Direccion.DoesNotExist:
        print(f"\nError: El id de dirección ingresada: '{id}' no se encuentra en la base de datos\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al borrar la dirección: {str(e)}\n")


def obtener_direccion(id_direccion):
    try:
        direccion = Direccion.objects.get(id=id_direccion)
        return direccion
    except Direccion.DoesNotExist:
        print(f"\nError: El id de dirección ingresada: '{id_direccion}' no se encuentra en la base de datos\n")
    except Exception as e:
        print(f"\nHa ocurrido un error al obtener la dirección: {str(e)}\n")