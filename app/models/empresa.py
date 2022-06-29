from app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re

class Empresa: 
    def __init__(self, data): 
        self.idempresas = data["idempresas"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.password = data["password"]

    @staticmethod
    def validate_empresa(empresa):
        is_valid = True 
        if len(empresa['nombre']) < 2:
            flash("Nombre con al menos 2 letras")
            is_valid = False
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(empresa['email']): 
            flash("Inserta un email valido")
            is_valid = False
        if len(empresa['password']) < 3:
            flash("Tu clave debe tener más de 3 caracteres.")
            is_valid = False
        if empresa['password'] != empresa ['confirm_password']:
                flash('Tu clave debe coincidir')
                is_valid = False
        return is_valid

    @staticmethod
    def validate_login(empresa):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(empresa['email']): 
            flash("Inserta un email valido")
            is_valid = False
        if len(empresa['password']) < 3:
            flash("Tu clave debe tener más de 3 caracteres.")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO hacela.empresas (nombre, email, password) VALUES (%(nombre)s, %(email)s, %(password)s);'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        empresas = {'idempresa' : results}
        print('guardando')
        print(empresas)
        return cls.get_one(empresas)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM hacela.empresas WHERE idempresas = %(idempresas)s;'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        print ('resultados de get_one empresa se ven aqui')
        print(results)
        #if len (results) > 0:
        #    return cls(results[0])
        #else:
        #    return None
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM hacela.empresas WHERE email = %(email)s;"
        result = connectToMySQL("hacela").query_db(query,data)
        return cls(result[0])
        #if len(result) > 0:
        #    return cls(result[0])
        #else:
        #    return None