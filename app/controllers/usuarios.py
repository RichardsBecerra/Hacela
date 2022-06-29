from app import app
from flask import Flask, render_template,request,redirect,session, jsonify
from app.models.usuario import Usuario
from app.models.desafio import Desafio
from app.models.ubicaciones import Ubicaciones 
from flask import flash
import time
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        print('estamos dentro')
        desafios = Desafio.get_all_desafios()
        return render_template ('dashboard.html', desafios = desafios )
    else:
        print('Crea un usuario')
        return redirect('/')


@app.route('/registrate', methods=['POST'])
def registrate():
    print(request.form)
    
    if not Usuario.validate_user(request.form):
        return redirect ('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    
    data = {
        "nombre": request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form ['email'],
        "password" : pw_hash
    }
    guardar_usuario = Usuario.save(data)
    print('esto es el ID de la ruta register')
    print (guardar_usuario)
    return redirect ('/')


@app.route('/login', methods=['POST'])
def entrar():
    
    data = { "email" : request.form["email"] }
    user_in_db = Usuario.get_by_email(data)
    
    
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        
        flash("Invalid Email/Password")
        return redirect('/')
    
    session['user_id'] = user_in_db.idusuarios
    session['nombre'] =user_in_db.nombre #este es solo para ponerle el nombre en el encabezado de html
    session['email'] = user_in_db.email #este es solo para ponerlo en la cuenta
    return redirect("/dashboard")

@app.route('/logout', methods=['POST'])
def cerrar_sesion():
    session.clear()
    return redirect ('/')

@app.route('/verdesafio/<int:iddesafios>')
def verdesafio(iddesafios):
    if 'user_id' in session:
        data = {'iddesafios': iddesafios}
        ver_desafio = Desafio.get_one(data)
        return render_template ('desafio.html', ver_desafio=ver_desafio)
    else:
        return redirect('/')

@app.route('/tucuenta/<int:idusuarios>')
def cuenta(idusuarios):

    data = {'idusuarios' : idusuarios}
    Usuario.get_one(data)
    desafios_cuenta=Desafio.desafios_cuenta(data)
    
    if 'user_id' in session:

        return render_template('cuenta.html', desafios_cuenta=desafios_cuenta)

@app.route('/tomalo/<int:iddesafios>', methods = ['GET','POST'])
def tomalo(iddesafios):
    if request.method == 'POST':
        data = {
            'idusuarios' : session['user_id'],
            'iddesafios' : iddesafios,
            'estado_usuario' : 0
        }

        Desafio.agregar_usuario_desafio(data)
        return redirect (f'/tomalo/{iddesafios}')
    
    return render_template('tomalo.html' )


@app.route('/location', methods=['POST'])
def getLocation():

    data = {'idusuarios' : session['user_id']}
    Ubicaciones.get_one_usuarios_y_desafios(data)
    idusuarios_y_desafios = Ubicaciones.get_one_usuarios_y_desafios(data)
    x = request.get_json()
    data = {
        'latitud' : x['lat'],
        'longitud' : x['lng'],
        'idusuarios_y_desafios' : idusuarios_y_desafios[0]['idusuarios_y_desafios']
    }
    print (idusuarios_y_desafios)
    #print('la latitud es', x['lat'])
    #print('la longitud es', x['lng'])
    print(request.get_json())
    Ubicaciones.guardar(data)
    return render_template ('proceso.html') 
    


@app.route('/resultado/<int:iddesafio>')
def resultado(completado, fallido):
    
    if Desafio.estado_usuario == 1 :
        data = {'completado' : completado}
        Desafio.update(data)
        return True, render_template ('felicitaciones.html')
    else:
        data = {'fallido' : fallido}
        Desafio.update(data)
        return False, render_template ('fallido.html')
    

@app.route('/finalizado')
def finalizado():
    data = {'idusuarios' : session['user_id']}
    idusuarios_y_desafios = Ubicaciones.get_one_usuarios_y_desafios(data)
    data = {'idusuarios_y_desafios' : idusuarios_y_desafios[0]['idusuarios_y_desafios']}
    #print (idusuarios_y_desafios[0]['idusuarios_y_desafios'])
    Ubicaciones.get_ubicaciones_desafio(data)
    ubicaciones = Ubicaciones.get_ubicaciones_desafio(data)
    
    return render_template('finalizado.html', ubicaciones = ubicaciones)


