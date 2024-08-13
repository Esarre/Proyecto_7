import os
import django
import sys

# Agrega el directorio del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoinmobiliaria.settings')
django.setup()

from inmobiliaria.models import Inmueble

def consultar_inmuebles_por_region():
    inmuebles_por_region = {}

    # Consulta los inmuebles y agrúpalos por región
    inmuebles = Inmueble.objects.select_related('direccion__region').values(
        'direccion__region__region', 'nombre', 'descripcion'
    )

    for inmueble in inmuebles:
        region = inmueble['direccion__region__region']
        if region not in inmuebles_por_region:
            inmuebles_por_region[region] = []
        inmuebles_por_region[region].append({
            'nombre': inmueble['nombre'],
            'descripcion': inmueble['descripcion']
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
    inmuebles_por_region = consultar_inmuebles_por_region()
    guardar_resultados_en_archivo(inmuebles_por_region, 'scripts/consultas_txt/inmuebles_por_region.txt')
    print("Consulta completada. Resultados guardados en 'scripts/consultas_txt/inmuebles_por_region.txt'.")
