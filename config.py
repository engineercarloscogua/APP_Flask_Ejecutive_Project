'''
# confguracón para la producción y el desarrollo y conexiones a base de datos
class Config:
    # Configuración para el modo de depuración (debug) y pruebas (testing)
    DEBUG = True
    TESTING =True
    
    # Configuración para SQLAlchemy para evitar el seguimiento de modificaciones
    SQLALCHEMY_TRACK_MODIFICATIONS = False   
    #debe estar credala base de datos ejemplo blog_db
    # Configuración de la URI de la base de datos
    # Aquí se especifica la URI para conectarse a la base de datos MySQL
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Villadavid20@localhost:3306/blog_db"   
    # El formato de la URI de la base de datos debe ser: 
    # mysql+pymysql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_de_datos>
    # En este caso, se conecta a MySQL, usando el usuario 'root' y contraseña 'Villadavid20',
    # en el host 'localhost', en el puerto '3308', a la base de datos 'blog_db'.
    
    #Clase para modo de producción y desarrollo 27:59 https://www.youtube.com/watch?v=JTAY5_LO0Ug

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    
    # Clave secreta para el entorno de desarrollo
    SECRET_KEY = 'dev'
    # Activa el modo de depuración (debug) y pruebas (testing)
    DEBUG = True
    TESTING =True
    
'''