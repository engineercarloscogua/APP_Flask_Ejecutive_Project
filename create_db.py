# se ecuta como create_db.py 1 vez para crear o actualizar las bd 
import os  #? Importa el módulo os, que proporciona una forma de interactuar con el sistema operativo, como crear carpetas y comprobar si existen.

from app import app, db  #? Importa la aplicación Flask (app) y la base de datos (db) desde el archivo 'app.py'.

# Crear la carpeta 'database' si no existe
if not os.path.exists('database'):  #? Verifica si no existe una carpeta llamada 'database' en el directorio actual.
    os.makedirs('database')  #? Si la carpeta 'database' no existe, la crea en el sistema de archivos.

# Contexto de la aplicación Flask para realizar operaciones de base de datos
with app.app_context():  #? Abre un contexto de aplicación Flask, lo que es necesario para realizar operaciones de base de datos dentro de una aplicación Flask.
    db.create_all()  #? Crea todas las tablas definidas en los modelos de base de datos (como el modelo User) en la base de datos.
    print("📦 Base de datos creada correctamente.")  #? Imprime un mensaje indicando que la base de datos se ha creado correctamente.
