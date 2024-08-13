import json
import os
import sys
import django
from django.conf import settings
from datetime import datetime

# Agrega el directorio del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ejecución del script en el contexto del proyecto:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoinmobiliaria.settings')  # Reemplaza 'proyectoinmoviliaria' con el nombre de tu proyecto
django.setup()

# Cargar los datos del archivo JSON existente
with open('inmobiliaria/fixtures/lista-inmuebles.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lista para almacenar los datos en el formato de fixture
fixture_data = []

# Itera sobre los inmuebles y convierte cada uno al formato de fixture
for i, inmueble in enumerate(data['inmuebles'], start=1):
    fixture_item = {
        "model": "inmobiliaria.inmueble",
        "pk": i,
        "fields": {
            "nombre": inmueble['nombre'],
            "descripcion": inmueble['descripcion'],
            "m2_construidos": inmueble['m2_construidos'],
            "m2_totales": inmueble['m2_totales'],
            "n_habitaciones": inmueble['n_habitaciones'],
            "n_banios": inmueble['n_banios'],
            "n_estacionamientos": inmueble['n_estacionamientos'],
            "precio": inmueble['precio'],
            "tipo_inmueble": inmueble['tipo_inmueble'],
            "fecha_creacion": datetime.now().strftime('%Y-%m-%d'),
            "fecha_modificacion": datetime.now().strftime('%Y-%m-%d'),
            "arrendador_usuario": inmueble['arrendador_usuario']
        }
    }
    fixture_data.append(fixture_item)

# Guarda los nuevos datos en un archivo JSON de fixture
with open('inmobiliaria/fixtures/inmuebles_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(fixture_data, f, ensure_ascii=False, indent=4)

print("Conversión completada. Archivo 'inmuebles_fixture.json' creado.")


"""
Pasos a seguir (consola, con el entorno activado):
    1. Ejecutar este script: 
        python scripts/convert_inmuebles_to_fixture.py

    2. Cargar la información a la BD utilizando el nuevo documento, que entiende Django:
        python manage.py loaddata inmuebles_fixture.json 
"""