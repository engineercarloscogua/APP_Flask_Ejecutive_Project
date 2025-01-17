#se ejecuta ditectamente para cargar las tablas de la BD
from app import app, db  # Importa la instancia de la aplicación y la base de datos
from database import User  # Importa el modelo User

# Establece el contexto de la aplicación
with app.app_context():
    # Crea las tablas definidas en los modelos (en este caso, solo User)
    db.create_all()

print("Tablas creadas correctamente.")


'''
en consola sqlite 3 se puede verificar la creación de las tablas
sqlite3 database/base.db
.table
'''