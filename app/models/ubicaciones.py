from winreg import QueryInfoKey
from app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template,request,redirect,session, flash

class Ubicaciones:
    def __init__(self, data):
        self.idubicaciones = data ['idubicaciones']
        self.longitud = data ['longitud']
        self.latitud = data ['latitud']
        self.fecha = data ['fecha']
        self.idusuarios_y_desafios = data ['idusuarios_y_desafios']


    @classmethod
    def guardar (cls, data):
        query = 'INSERT INTO hacela.ubicaciones (longitud, latitud, fecha, idusuarios_y_desafios ) VALUES (%(longitud)s, %(latitud)s, now(), %(idusuarios_y_desafios)s);'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        return results

    @classmethod
    def get_one_usuarios_y_desafios(cls, data):
        query = 'SELECT * FROM hacela.usuarios_y_desafios WHERE idusuarios = %(idusuarios)s AND idusuarios_y_desafios = (SELECT MAX(idusuarios_y_desafios) from hacela.usuarios_y_desafios);'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        print (results)
        return results

    @classmethod
    def get_ubicaciones_desafio(cls, data):
        query = 'SELECT (latitud), (longitud) FROM hacela.ubicaciones WHERE idusuarios_y_desafios = %(idusuarios_y_desafios)s;'
        mysql= connectToMySQL('hacela')
        results = mysql.query_db(query, data)
        print (results)
        return results