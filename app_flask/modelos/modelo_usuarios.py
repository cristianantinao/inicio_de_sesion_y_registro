from app_flask.configuraciones.mysqlconnection import connectToMySQL
from flask import flash 
from app_flask import BASE_DATOS, EMAIL_REGEX

class Usuario:
    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.email = datos['email']
        self.contraseña = datos['contraseña']
        self.created_at = datos['created_at']
        self.updated_at = datos['updated_at']
    
    @classmethod
    def crear_user(cls, datos):
        query = """
                INSERT INTO usuarios (nombre, apellido, email, contraseña)
                VALUES ( %(nombre)s, %(apellido)s, %(email)s, %(contraseña)s );
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)
    
    @classmethod
    def obtener_user(cls, datos):
        query = """
                SELECT * 
                FROM usuarios
                WHERE email = %(email)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, datos)
        if len(resultado) == 0:
            return None 
        return cls(resultado[0])
    
    @staticmethod 
    def validacion_registro(datos):
        es_valido = True
        if len(datos['nombre']) < 2:
            es_valido = False 
            flash('Por favor escribe tu nombre.', 'error_nombre')
        if len(datos['apellido']) < 2:
            es_valido = False 
            flash('Por favor escribe tu apellido.', 'error_apellido') 
        if not EMAIL_REGEX.match(datos['email']):
            es_valido = False
            flash('Por favor ingresa un email valido', 'error_email')
        if datos['contraseña'] != datos['password']:
            es_valido = False
            flash('Tus contraseñas no coinciden', 'error_contraseña')
        if len(datos['contraseña']) < 1:
            es_valido = False
            flash('Por favor proporciona una contraseña', 'error_contraseña')
        return es_valido