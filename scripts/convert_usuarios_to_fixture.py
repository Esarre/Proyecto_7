import json
import os
import sys
import django
from django.conf import settings
from django.contrib.auth.hashers import make_password
from datetime import datetime

# Agrega el directorio del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ejecución del script en el contexto del proyecto:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyectoinmobiliaria.settings')  # Reemplaza 'proyectoinmoviliaria' con el nombre de tu proyecto
django.setup()

# Carga el archivo JSON original
with open('inmobiliaria/fixtures/lista-usuarios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lista para almacenar los nuevos datos en formato de fixture de Django
fixture_data = []

# Agrega manualmente el administrador
admin_fixture = {
    "model": "inmobiliaria.Usuario",
    "pk": 1,
    "fields": {
        "username": "admin",
        "rut": "000000000",
        "primer_nombre": "Admin",
        "segundo_nombre": "",
        "apellido_paterno": "Admin",
        "apellido_materno": "",
        "fecha_nac": "1970-01-01",
        "telefono": "00000000",
        "email": "admin@mail.com",
        "password": make_password("admin123456789"),
        "tipo_usuario": "administrador",
        "fecha_creacion": datetime.now().strftime('%Y-%m-%d'),
        "fecha_modificacion": datetime.now().strftime('%Y-%m-%d'),
    }
}
fixture_data.append(admin_fixture)

# Itera sobre los usuarios y convierte cada uno al formato de fixture
for idx, usuario in enumerate(data['usuarios'], start=2):
    usuario_fixture = {
        "model": "inmobiliaria.Usuario",
        "pk": idx,
        "fields": {
            "username": usuario['username'],
            "rut": usuario['rut'],
            "primer_nombre": usuario['primer_nombre'],
            "segundo_nombre": usuario['segundo_nombre'],
            "apellido_paterno": usuario['apellido_paterno'],
            "apellido_materno": usuario['apellido_materno'],
            "fecha_nac": usuario['fecha_nac'],
            "telefono": usuario['telefono'],
            "email": usuario['email'],
            "password": make_password("usuario123456789"),
            "tipo_usuario": usuario['tipo_usuario'],
            "fecha_creacion": datetime.now().strftime('%Y-%m-%d'),
            "fecha_modificacion": datetime.now().strftime('%Y-%m-%d'),
        }
    }
    fixture_data.append(usuario_fixture)

# Guarda los nuevos datos en un archivo JSON de fixture
with open('inmobiliaria/fixtures/usuarios_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(fixture_data, f, ensure_ascii=False, indent=4)

print("Conversión completada. Archivo 'usuarios_fixture.json' creado.")


"""
Pasos a seguir (consola, con el entorno activado):
    1. Ejecutar este script: 
        python scripts/convert_usuarios_to_fixture.py

    2. Cargar la información a la BD utilizando el nuevo documento, que entiende Django:
        python manage.py loaddata usuarios_fixture.json 
"""