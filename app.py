# Controlador
from flask import ( # Importación de las funcionalidades principales de Flask
    Flask,  # Flask es el framework principal para crear la aplicación web
    render_template,  # Funcionalidad de Flask para renderizar plantillas HTML
    request,  # Permite extraer datos de los formularios enviados (GET/POST)
    redirect,  # Redirige al usuario a otra ruta
    url_for,  # Genera URLs de rutas en la aplicación
    flash  # Permite mostrar mensajes emergentes de tipo alerta
)

from flask_sqlalchemy import SQLAlchemy  # Importa la funcionalidad de SQLAlchemy para manejar bases de datos
import json  # El módulo json se utiliza para trabajar con datos en formato JSON
import os.path  # El módulo os permite interactuar con el sistema de archivos
from werkzeug.utils import secure_filename  # Función que asegura que el nombre del archivo es seguro

# Importación de los formularios de la carpeta forms
from forms import Loginform, CreateUserForm  # Importando los formularios definidos en form.py

# ========================== Creación de la aplicación ============================
app = Flask(__name__)  # Crea una instancia de la aplicación Flask

# ========================== Configuración de la base de datos ===================
basedir = os.path.abspath(os.path.dirname(__file__))  # Obtiene la ruta absoluta del directorio actual
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'database', 'base.db')}"  # Configura la URI de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva la notificación de modificaciones en la base de datos
app.secret_key = '2025'  # Clave secreta para usar sesiones y mensajes emergentes (flash)
db = SQLAlchemy(app)  # Crea una instancia de SQLAlchemy para manejar la base de datos

# ========================== Rutas ==========================

# Ruta principal, disponible tanto para GET como para POST
@app.route("/home", methods = ['GET', 'POST'])  
@app.route("/", methods = ['GET', 'POST'])  # Esta ruta también es la raíz de la aplicación

def home():
    login = Loginform()  # Crea el formulario de login
    if login.validate_on_submit():  # Si el formulario se envía y es válido
        return '<h1>' + login.username.data + '  ' + login.password.data + '</h1>'  # Muestra los datos enviados como ejemplo
    return render_template('form2.html', formi= login)  # Renderiza la plantilla 'form2.html' pasando el formulario 'login'

# Ruta para registrar un nuevo usuario
@app.route("/registro", methods = ['GET', 'POST'])
def login():
    registro = CreateUserForm()  # Crea el formulario de registro de usuario
    if registro.validate_on_submit():  # Si el formulario se envía y es válido
        new_user = User(username=registro.username.data, email=registro.email.data, password=registro.password.data)  # Crea un nuevo objeto usuario
        db.session.add(new_user)  # Agrega el nuevo usuario a la sesión de la base de datos
        db.session.commit()  # Confirma la transacción en la base de datos
        return '<h1> Nuevo Usuario Registrado</h1>'  # Muestra mensaje de éxito
    return render_template('register.html', regis=registro)  # Renderiza el formulario de registro en 'register.html'

# Ruta para el formulario de ejemplo
@app.route("/form")
def form():
    return render_template('form.html')  # Renderiza la plantilla 'form.html'

# Ruta dinámica para manejar peticiones GET y POST
@app.route("/dinamic", methods = ['GET', 'POST'])
def dinamic():
    if request.method == 'POST':  # Si se realiza una petición POST (envío de formulario)
        urls = {}  # Diccionario para almacenar las URLs ingresadas
        if os.path.exists('urls.json'):  # Si el archivo 'urls.json' existe
            try:
                with open('urls.json') as url_file:  # Abre el archivo 'urls.json'
                    urls = json.load(url_file)  # Carga el contenido del archivo JSON en el diccionario 'urls'
            except json.JSONDecodeError:  # Si hay un error de formato en el JSON
                urls = {}  # Reinicia el diccionario a vacío
        else:
            urls = {}  # Si el archivo no existe, inicia un diccionario vacío

        # Si el 'code' enviado en el formulario ya está en el diccionario
        if request.form['code'] in urls.keys():
            flash('Esa clave o nombre ya está ocupada')  # Muestra un mensaje de alerta
            return redirect(url_for('form'))  # Redirige al formulario
        # Si se proporciona una URL en el formulario
        if 'url' in request.form.keys():
            urls[request.form['code']] = request.form['url']  # Guarda la URL en el diccionario
        else:
            f = request.files['file']  # Si se sube un archivo
            full_name = request.form['code'] + secure_filename(f.filename)  # Asegura un nombre único para el archivo
            f.save('static/uploads/' + full_name)  # Guarda el archivo en la carpeta 'static/uploads'
            urls[request.form['code']] = {'file': full_name}  # Guarda la información del archivo en el diccionario
        
        # Guarda el diccionario actualizado en el archivo 'urls.json'
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            flash("Se ha creado el registro correctamente", "success")  # Muestra mensaje de éxito
        return render_template('dinamic.html', nombre=request.form['code'])  # Muestra la plantilla 'dinamic.html' pasando el código como parámetro
    else:
        return redirect(url_for('form'))  # Si no es un POST, redirige al formulario

# Ruta para redirigir a imágenes o archivos
@app.route('/<string:code>')
def redirect_to(code):
    if os.path.exists('urls.json'):  # Si el archivo 'urls.json' existe
        with open('urls.json') as url_file:
            urls = json.load(url_file)  # Carga las URLs del archivo
            if code in urls.keys():  # Si el código existe en las URLs
                return redirect(url_for('static', filename='uploads/' + urls[code]['file']))  # Redirige a la URL asociada
    return "Código no encontrado"  # Si el código no se encuentra, muestra un mensaje de error

# ========================== Ejecución de la aplicación ===========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Ejecuta la aplicación en modo de depuración en el puerto 5000
