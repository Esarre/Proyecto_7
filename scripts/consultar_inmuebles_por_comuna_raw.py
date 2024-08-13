import os
import django
import sys
from django.db import connection

# Agrega el directorio del proyecto al sys.path (explicación abajo del todo)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoinmobiliaria.settings')
django.setup()

def consultar_inmuebles_por_comuna_raw():
    inmuebles_por_comuna = {}

    # Consulta SQL para obtener inmuebles agrupados por comuna
    query = """
    SELECT c.comuna AS comuna, i.nombre AS nombre, i.descripcion AS descripcion
    FROM inmobiliaria_inmueble i
    JOIN inmobiliaria_direccion d ON i.id = d.inmueble_id
    JOIN inmobiliaria_comuna c ON d.comuna_id = c.id
    """
    
    # Explicación del siguiente código abajo del todo:
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    for row in rows:
        comuna, nombre, descripcion = row
        if comuna not in inmuebles_por_comuna:
            inmuebles_por_comuna[comuna] = []
        inmuebles_por_comuna[comuna].append({
            'nombre': nombre,
            'descripcion': descripcion
        })

    return inmuebles_por_comuna

def guardar_resultados_en_archivo(inmuebles_por_comuna, archivo):
    with open(archivo, 'w', encoding='utf-8') as f:
        for comuna, inmuebles in inmuebles_por_comuna.items():
            f.write(f"Comuna: {comuna}\n")
            for inmueble in inmuebles:
                f.write(f"Nombre: {inmueble['nombre']}\n")
                f.write(f"Descripción: {inmueble['descripcion']}\n")
                f.write("-" * 40 + "\n")
            f.write("=" * 40 + "\n")

if __name__ == '__main__':
    inmuebles_por_comuna = consultar_inmuebles_por_comuna_raw()
    guardar_resultados_en_archivo(inmuebles_por_comuna, 'scripts/consultas_txt/inmuebles_por_comuna_raw.txt')
    print("Consulta RAW completada. Resultados guardados en 'scripts/consultas_txt/inmuebles_por_comuna_raw.txt'.")


"""
#################################################
    Explicación código de conexión y los row:
#################################################

    - 'with connection.cursor() as cursor:' : Abre un 'cursor' de la conexión a la base de datos. Un 'cursor' es un objeto que permite ejecutar consultas y recuperar datos.
        - 'with' : La palabra clave (o 'estamento'), 'with', se utiliza para simplificar la gestión de recursos, asegurando que los recursos sean correctamente liberados 
                cuando ya no se necesitan.
        - 'connection' : es un objeto proporcionado por Django que representa la conexión actual a la base de datos.
        - 'cursor()' : es un método del objeto 'connection' que devuelve un cursor de base de datos.
    
    - 'cursor.execute(query)' : 'cursor' ejecuta la query almacenada en la variable del mismo nombre.
    
    - 'rows = cursor.fetchall()' : 'fetchall()' devuelve todas las filas de la consulta en forma de lista de tuplas, así cada tupla representa una fila de la BD. Almacena esa
        lista de tuplas en la variable 'rows'.
    
    - Luego, ocurre la lógica para traer la información de la lista de tuplas y trabajarla como se requiere, en este caso imprimirlas en un archivo de texto.

    
########################################################################
    Explicación sobre agregar el directorio del proyecto a sys.path:
########################################################################

- Esto se utiliza para poder ejecutar el script cuando el archivo .py que contiene el código no está a la misma altura de manage.py 
(en tal caso, no necesitamos escribir el código que se explicará a continuación). El código es el siguiente:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

- Explicación de las partes:
    - 'os.path.dirname(__file__)' : Obtenemos el directorio donde se encuentra el script actual. '__file__' es una variable especial que contiene la ruta del archivo actual.
    
    - 'os.path.join(os.path.dirname(__file__), '..')' : Se construye una nueva ruta que sitúa al archivo un nivel por encima del directorio actual (sería "sacar el archivo"
        de la carpeta scripts, o sea: en vez de estar en "proyectoinmobiliaria/scripts/archivo.py", lo deja como "proyectoinmobiliaria/archivo.py").
    
    - 'os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))' : Hasta este punto, la ruta del archivo era "relativa", con esto la conviertre en una ruta "absoluta"
        para que Python no tenga problemas al momento de resolverla.
    
    - 'sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))' : Agrega la ruta absoluta al principio de la lista sys.path. 
        sys.path es una lista de directorios que Python utiliza para buscar módulos. Al añadir la ruta de tu proyecto a sys.path, le estás diciendo a Python que también 
        busque módulos en esa ubicación.
"""