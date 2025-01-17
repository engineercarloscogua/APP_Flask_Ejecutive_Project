#Hacer formularios con WT forms de flask  -Modelo de formularios
# Importamos las bibliotecas necesarias
#from flask import Flask  # Importamos la clase Flask del módulo flask, usada para crear nuestra app.
from flask_wtf import FlaskForm  # Importamos la clase FlaskForm de flask_wtf, que nos permite crear formularios en Flask.
from wtforms import (  # Importamos los campos que vamos a usar en el formulario.
    StringField,  # Campo para ingresar texto (usado para el nombre de usuario, email, etc.).
    PasswordField,  # Campo para ingresar contraseñas.
    BooleanField  # Campo para valores booleanos (Ej. 'Recordarme').
)
from wtforms.validators import (  # Importamos los validadores para asegurarnos de que los datos sean correctos.
    DataRequired,  # Validador para asegurarnos de que el campo no quede vacío.
    InputRequired,  # Validador para asegurarnos de que se ingrese un dato.
    Email,  # Validador para asegurarnos de que el email sea válido.
    Length  # Validador para verificar la longitud del valor ingresado.
)

# ---------------------- Formulario de Inicio de Sesión (Login) ---------------------------
class Loginform(FlaskForm):
    """
    Esta clase define el formulario de inicio de sesión para los usuarios.
    Hereda de FlaskForm y se usará para crear el formulario en una plantilla HTML con Jinja2.
    """
    # Definimos el campo para el nombre de usuario (texto) y sus validadores.
    username = StringField('username', 
                           validators=[InputRequired(message='Este campo requiere completarse'),
                                       Length(min=4, max=16, message='El Nombre de Usuario debe tener entre %(min)d y %(max)d Caracteres')])

    # Definimos el campo para la contraseña (texto oculto) y sus validadores.
    password = PasswordField('password', 
                             validators=[InputRequired(message='Este campo requiere completarse'),
                                         Length(min=8, max=16, message='La contraseña debe tener entre %(min)d y %(max)d Caracteres')])

    # Campo para recordar al usuario (booleano).
    remember = BooleanField('Recuerda me')

# ---------------------- Formulario de Registro de Usuario ---------------------------
class CreateUserForm(FlaskForm):
    """
    Esta clase define el formulario para crear un nuevo usuario.
    Hereda de FlaskForm y se usará para crear el formulario en una plantilla HTML con Jinja2.
    """
    # Definimos el campo para el correo electrónico (texto) con validación de correo electrónico.
    email = StringField('Escribe el Correo Electrónico', 
                        validators=[InputRequired(message='Este campo requiere completarse'),
                                    Email(message="Este no es un correo electrónico válido"), 
                                    Length(max=60, message='El Correo Electrónico debe tener %(max)d caracteres máximo')])

    # Definimos el campo para el nombre de usuario con validadores para longitud.
    username = StringField('Escribe el Nombre de Usuario', 
                           validators=[InputRequired(message='Este campo requiere completarse'),
                                       Length(min=4, max=16, message='El Nombre de Usuario debe tener entre %(min)d y %(max)d caracteres')])

    # Definimos el campo para la contraseña con validadores para longitud.
    password = PasswordField('Agrega una Contraseña', 
                             validators=[InputRequired(message='Este campo requiere completarse'), 
                                         Length(min=8, max=16, message='La contraseña debe tener entre %(min)d y %(max)d caracteres')])
