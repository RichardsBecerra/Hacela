from app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re

class Usuario: 
    def __init__(self, data): 
        self.idusuarios = data["idusuarios"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]


    @staticmethod
    def validate_user(user):
        is_valid = True 
        if len(user['nombre']) < 2:
            flash("Nombre con al menos 2 letras")
            is_valid = False
        if len(user['apellido']) < 2:
            flash("Apellido con al menos 2 letras.")
            is_valid = False
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']): 
            flash("Inserta un email valido")
            is_valid = False
        if len(user['password']) < 3:
            flash("Tu clave debe tener más de 3 caracteres.")
            is_valid = False
        if user['password'] != user ['confirm_password']:
                flash('Tu clave debe coincidir')
                is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user['email']): 
            flash("Inserta un email valido")
            is_valid = False
        if len(user['password']) < 3:
            flash("Tu clave debe tener más de 3 caracteres.")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO hacela.usuarios (nombre, apellido, email, password) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        users = {'idusuario' : results}
        print('guardando')
        print(users)
        return cls.get_one(users)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM hacela.usuarios WHERE idusuarios = %(idusuarios)s;'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        print ('resultados de get_one usuario se ven aqui')
        print(results)
        #if len (results) > 0:
        #    return cls(results[0])
        #else:
        #    return None
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM hacela.usuarios WHERE email = %(email)s;"
        result = connectToMySQL("hacela").query_db(query,data)
            
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    