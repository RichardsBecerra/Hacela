from app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template,request,redirect,session, flash


class Desafio:
    def __init__(self, data):
        self.iddesafios = data ['iddesafios']
        self.nombre = data ['nombre']
        self.descuento = data ['descuento']
        self.condiciones = data['condiciones']
        self.creado = data ['creado']
        self.finaliza = data ['finaliza']
        self.idempresas = data ['idempresas']
        

    @staticmethod
    def validate_desafio(desafio):
        is_valid = True

        if len(desafio['nombre']) < 2:
            print('INCORRECTO')
            flash("El nombre del desafio debe tener más de 2 caracteres.")
            is_valid = False

        if len(desafio['descuento']) < 1:
            print('INCORRECTO')
            flash("Descuento debe tener al menos 1 caracter.")
            is_valid = False

        if len(desafio['condiciones']) < 10:
            print('INCORRECTO')
            flash("Condiciones debe tener al menos 10 caracteres.")
            is_valid = False

        if len(desafio['creado']) < 1:
            print('INCORRECTO')
            flash("Descuento debe tener una fecha de creacion.")
            is_valid = False

        if len(desafio['finaliza']) < 1:
            print('INCORRECTO')
            flash("Descuento debe tener una fecha de caducidad.")
            is_valid = False

        print('VALIDANDO EL DESAFIO ')
        return is_valid


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO hacela.desafios (nombre, descuento, condiciones, creado, finaliza, idempresas) VALUES (%(nombre)s, %(descuento)s, %(condiciones)s, %(creado)s, %(finaliza)s, %(idempresas)s);'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM hacela.desafios WHERE iddesafios = %(iddesafios)s'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        print (results)
        return cls(results[0])
        
    @classmethod
    def get_all_desafios(cls):
        query = 'SELECT * FROM hacela.desafios'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query)
        print ('resultados de get_all desafio se ven aqui')
        return results

    @classmethod
    def get_desafios_by_empresa(cls, data):
        query = 'SELECT * FROM hacela.desafios WHERE idempresas = %(idempresas)s'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        print ('resultados de get_one desafio se ven aqui')
        return results
    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM hacela.desafio WHERE iddesafios = (%(iddesafios)s);'
        results = connectToMySQL('hacela').query_db(query, data)
        
        return results

    @classmethod
    def agregar_usuario_desafio(cls, data):
        query = 'INSERT INTO hacela.usuarios_y_desafios (idusuarios, iddesafios, estado_usuario) VALUES (%(idusuarios)s, %(iddesafios)s, %(estado_usuario)s);'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)

        return results

    @classmethod
    def desafios_cuenta(cls, data):
        query = 'SELECT DISTINCT hacela.desafios.nombre, hacela.desafios.descuento, hacela.usuarios_y_desafios.estado_usuario, hacela.desafios.finaliza FROM hacela.desafios LEFT JOIN hacela.usuarios_y_desafios ON hacela.desafios.iddesafios = hacela.usuarios_y_desafios.iddesafios WHERE idusuarios = %(idusuarios)s;'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)

        return results