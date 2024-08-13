import os
import django
import sys

# Agrega el directorio del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoinmobiliaria.settings')
django.setup()

from inmobiliaria.models import Inmueble

def consultar_inmuebles_por_comuna():
    inmuebles_por_comuna = {}

    # Consulta los inmuebles y agrúpalos por comuna
    inmuebles = Inmueble.objects.select_related('direccion__comuna').values(
        'direccion__comuna__comuna', 'nombre', 'descripcion'
    )

    for inmueble in inmuebles:
        comuna = inmueble['direccion__comuna__comuna']
        if comuna not in inmuebles_por_comuna:
            inmuebles_por_comuna[comuna] = []
        inmuebles_por_comuna[comuna].append({
            'nombre': inmueble['nombre'],
            'descripcion': inmueble['descripcion']
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
    inmuebles_por_comuna = consultar_inmuebles_por_comuna()
    guardar_resultados_en_archivo(inmuebles_por_comuna, 'scripts/consultas_txt/inmuebles_por_comuna.txt')
    print("Consulta completada. Resultados guardados en 'scripts/consultas_txt/inmuebles_por_comuna.txt'.")


"""
Explicación del código:

- En la línea de código:
    inmuebles = Inmueble.objects.select_related('direccion__comuna').values('direccion__comuna__comuna', 'nombre', 'descripcion')

    - select_related(): realiza un join siguiendo las relaciones ForeignKey y OneToOneField "hacia adelante". 
            Su objetivo principal es reducir el número de consultas realizadas a la base de datos al usar un único JOIN 
            para recuperar datos relacionados en una sola consulta.

            En los modelos, el modelo Inmueble que tiene una relación ForeignKey con Direccion, y Direccion a su vez tiene una relación
            ForeignKey con Comuna, el uso de select_related permite obtener los datos de Comuna directamente al consultar Inmueble.

            El equivalente de esta consulta a una consulta SQL es la siguiente:

            SELECT
                c.comuna AS comuna,
                i.nombre AS nombre,
                i.descripcion AS descripcion
            FROM
                inmobiliaria_inmueble AS i
            INNER JOIN
                inmobiliaria_direccion AS d ON i.id = d.inmueble_id
            INNER JOIN
                inmobiliaria_comuna AS c ON d.comuna_id = c.id
            ORDER BY
                c.comuna, i.nombre;

    - 'direccion__comuna__comuna': 
            direccion: campo del modelo Inmueble que apunta a Direccion a través del OneToOneField. Es como hacer Inmueble.direccion.
            comuna: campo del modelo Direccion que apunta a Comuna a través del FK. Es como hacer Direccion.comuna.
            comuna (segundo): campo del modelo Comuna. En este caso accedemos al propio campo de Comuna.

            Por lo tanto, lo que obtenemos con las dobles barras bajas es acceder, escalonadamente, al propio campo "comuna" del modelo
            Comuna, pero pasando por las relaciones que se dan entre: Inmueble - Direccion - Comuna. Con esto, obtenemos el valor de
            comuna mientras comenzamos la consulta con las instancias de Inmueble.

    - if comuna not in inmuebles_por_comuna: Verifica si la comuna actual ya está registrada en el diccioario ('inmuebles_por_comuna').
            Si no está en el diccionario, crea una nueva entrada en el diccionario con la clave comuna y le asigna una lista vacía como valor
            'inmuebles_por_comuna[comuna] = []'.

            Luego, a la lista vacía de la comuna le agrega los valores 'nombre' y 'descripción' correspondientes a través de:
                 inmuebles_por_comuna[comuna].append({'nombre': inmueble['nombre'],'descripcion': inmueble['descripcion']})

                Si la comuna ya existe, agrega a la lista solo los valores 'nombre' y 'descripción'
"""