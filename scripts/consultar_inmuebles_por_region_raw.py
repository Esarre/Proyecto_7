import os
import django
import sys
from django.db import connection

# Agrega el directorio del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoinmobiliaria.settings')
django.setup()

def consultar_inmuebles_por_region_raw():
    inmuebles_por_region = {}

    query = """
    SELECT r.region AS region, i.nombre AS nombre, i.descripcion AS descripcion
    FROM inmobiliaria_inmueble i
    JOIN inmobiliaria_direccion d ON i.id = d.inmueble_id
    JOIN inmobiliaria_region r ON d.region_id = r.id
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    for row in rows:
        region, nombre, descripcion = row
        if region not in inmuebles_por_region:
            inmuebles_por_region[region] = []
        inmuebles_por_region[region].append({
            'nombre': nombre,
            'descripcion': descripcion
        })

    return inmuebles_por_region

def guardar_resultados_en_archivo(inmuebles_por_region, archivo):
    with open(archivo, 'w', encoding='utf-8') as f:
        for region, inmuebles in inmuebles_por_region.items():
            f.write(f"Región: {region}\n")
            for inmueble in inmuebles:
                f.write(f"Nombre: {inmueble['nombre']}\n")
                f.write(f"Descripción: {inmueble['descripcion']}\n")
                f.write("-" * 40 + "\n")
            f.write("=" * 40 + "\n")

if __name__ == '__main__':
    inmuebles_por_region = consultar_inmuebles_por_region_raw()
    guardar_resultados_en_archivo(inmuebles_por_region, 'scripts/consultas_txt/inmuebles_por_region_raw.txt')
    print("Consulta RAW completada. Resultados guardados en 'scripts/consultas_txt/inmuebles_por_region_raw.txt'.")
