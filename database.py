# Crea un modelo de base de datos utilizando SQLAlchemy
from app import db  # Importa el objeto db, que es utilizado para interactuar con la base de datos.

# La siguiente línea está comentada porque no se está utilizando en el código actual, pero es una importación necesaria si deseas usar SQLAlchemy directamente.
# from flask_sqlalchemy import SQLAlchemy  #? Importa SQLAlchemy para trabajar con bases de datos en Flask.

# Definimos un modelo de base de datos utilizando SQLAlchemy. Este modelo representará una tabla en la base de datos.
class User(db.Model): #? La clase 'User' hereda de 'db.Model', lo que indica que es un modelo de base de datos.
    # Definición de los campos (columnas) que tendrá la tabla 'User' en la base de datos.
    id = db.Column(db.Integer, primary_key=True)  # 'id' es una columna de tipo entero. Es la clave primaria de la tabla.
    username = db.Column(db.String(80), unique=True, nullable=False)  # 'username' es una columna única y no nula.
    email = db.Column(db.String(80), unique=True, nullable=False)  # 'email' es una columna única y no nula.
    password = db.Column(db.String(80))  # 'password' es una columna de tipo cadena. Puede ser nula.

    # Método especial que permite mostrar los registros de una manera más legible en la consola de Python, ver notas.txt.
    def __repr__(self):  #? __repr__ es un método especial que define cómo se mostrará el objeto cuando se imprima o se convierta en cadena.
        return f'{self.id, self.username, self.email}'  # Devuelve una representación del objeto mostrando id, username y email en consola python.
