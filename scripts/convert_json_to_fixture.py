# Convertir el json que contiene las regiones y sus comunas a un archivo legible por Django (al guardar los cambios del código, ejecutar en la consola: 
#     python scripts/convert_json_to_fixture.py
# se creará un archivo llamado "comunas-regiones-fixture.json" en la misma carpeta donde está el json original -> en fixtures
# Si todo sale bien, ejecutar en la consola: 
#     python manage.py loaddata comunas-regiones-fixture.json

import os
import json

# Determinar la ruta del archivo JSON en relación con el script
current_dir = os.path.dirname(__file__)
json_file_path = os.path.join(current_dir, '..', 'inmobiliaria', 'fixtures', 'comunas-regiones.json')
fixture_file_path = os.path.join(current_dir, '..', 'inmobiliaria', 'fixtures', 'comunas-regiones-fixture.json')

# Cargar el archivo JSON original
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Lista para almacenar los nuevos registros
fixture_data = []

# Variables para manejar las claves primarias (pk)
region_pk = 1
comuna_pk = 1

# Convertir la estructura
for region_data in data['regiones']:
    region_entry = {
        "model": "inmobiliaria.region",
        "pk": region_pk,
        "fields": {
            "region": region_data['region']
        }
    }
    fixture_data.append(region_entry)

    for comuna_name in region_data['comunas']:
        comuna_entry = {
            "model": "inmobiliaria.comuna",
            "pk": comuna_pk,
            "fields": {
                "comuna": comuna_name,
                "region": region_pk
            }
        }
        fixture_data.append(comuna_entry)
        comuna_pk += 1

    region_pk += 1

# Guardar la nueva estructura en un archivo JSON
with open(fixture_file_path, 'w', encoding='utf-8') as file:
    json.dump(fixture_data, file, ensure_ascii=False, indent=4)

print(f"Archivo JSON convertido y guardado como 'comunas-regiones-fixture.json'.")
 