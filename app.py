# ====================== Importaciones necesarias ======================
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy  # ORM para la base de datos
from werkzeug.utils import secure_filename  # Para manejo seguro de archivos
import json  # Para manejo de datos JSON
import os.path  # Para operaciones con rutas de archivos

# ====================== Configuración de la aplicación ======================
# Crear instancia de Flask
app = Flask(__name__)

# Configuración de la base de datos y seguridad
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database', 'base.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones
app.config['SECRET_KEY'] = '2025'  # Clave secreta para sesiones y CSRF

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# ====================== Modelo de Usuario ======================
class User(db.Model):
    """
    Modelo de base de datos para la tabla de usuarios.
    Define la estructura y restricciones de los datos de usuario.
    """
    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Identificador único
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(80), unique=True, nullable=False)  # Email único
    password = db.Column(db.String(80))  # Contraseña (en producción debería estar hasheada)

    def __repr__(self):
        """Método para representación string del objeto"""
        return f'{self.id, self.username, self.email}'

# ====================== Formularios ======================
from flask_wtf import FlaskForm  # Base para formularios seguros
from wtforms import StringField, PasswordField, SubmitField  # Campos de formulario
from wtforms.validators import DataRequired, Email  # Validadores

class LoginForm(FlaskForm):
    """
    Formulario para el inicio de sesión.
    Incluye campos para nombre de usuario y contraseña.
    """
    username = StringField('Username', validators=[DataRequired()])  # Campo obligatorio
    password = PasswordField('Password', validators=[DataRequired()])  # Campo obligatorio
    submit = SubmitField('Login')  # Botón de envío

class CreateUserForm(FlaskForm):
    """
    Formulario para el registro de nuevos usuarios.
    Incluye validación de email y campos obligatorios.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])  # Validación de formato de email
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# ====================== Rutas ======================

@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Ruta principal y de login.
    Maneja tanto la visualización del formulario como el proceso de login.
    """
    login = LoginForm()
    if login.validate_on_submit():  # Si el formulario es válido y fue enviado
        # Aquí deberías agregar la lógica de verificación de credenciales
        return '<h1>' + login.username.data + '  ' + login.password.data + '</h1>'
    return render_template('form2.html', formi=login)

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    """
    Ruta para el registro de nuevos usuarios.
    Incluye validaciones y manejo de errores.
    """
    registro_form = CreateUserForm()
    if registro_form.validate_on_submit():
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=registro_form.username.data).first()
        if existing_user:
            flash('El nombre de usuario ya existe')
            return redirect(url_for('registro'))
        
        # Verificar si el email ya existe
        existing_email = User.query.filter_by(email=registro_form.email.data).first()
        if existing_email:
            flash('El email ya está registrado')
            return redirect(url_for('registro'))
        
        # Crear nuevo usuario con los datos del formulario
        new_user = User(
            username=registro_form.username.data,
            email=registro_form.email.data,
            password=registro_form.password.data  # NOTA: En producción, usar hash para la contraseña
        )
        
        # Intentar guardar el nuevo usuario en la base de datos
        try:
            db.session.add(new_user)  # Agregar a la sesión de la base de datos
            db.session.commit()  # Confirmar los cambios
            flash('Usuario registrado exitosamente')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()  # Revertir cambios en caso de error
            flash('Error al registrar usuario')
            return redirect(url_for('registro'))
            
    return render_template('register.html', regis=registro_form)

# ====================== Inicialización de la Base de Datos ======================
# Crear todas las tablas definidas en los modelos
with app.app_context():
    db.create_all()

# ====================== Ejecución de la Aplicación ======================
if __name__ == '__main__':
    app.run(debug=True)  # Modo debug para desarrollo