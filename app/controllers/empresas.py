from app import app
from flask import Flask, render_template,request,redirect,session
from app.models.empresa import Empresa
from flask import flash
from flask_bcrypt import Bcrypt
from app.models.desafio import Desafio

bcrypt = Bcrypt(app)

@app.route('/indexempresa')
def indexempresa():
    return render_template('indexempresa.html')

@app.route('/registroempresa', methods=['POST'])
def register():
    print(request.form)
    
    if not Empresa.validate_empresa(request.form):
        return redirect ('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    
    data = {
        "nombre": request.form['nombre'],
        'email': request.form ['email'],
        "password" : pw_hash
    }
    empresa_id = Empresa.save(data)
    print('esto es el ID de la ruta registra empresa')
    print (empresa_id)
    return redirect ('/indexempresa')

@app.route('/loginempresa', methods=['POST'])
def login():
    
    data = { "email" : request.form["email"] }
    empresa_en_db = Empresa.get_by_email(data)
    
    if not empresa_en_db:
        flash("Invalid Email/Password")
        return redirect("/")
    
    if not bcrypt.check_password_hash(empresa_en_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    
    session['empresa_id'] = empresa_en_db.idempresas
    session['nombre'] = empresa_en_db.nombre #este es solo para ponerle el nombre en el encabezado de html
    
    return redirect("/creatusdesafios")

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect ('/')

@app.route('/creatusdesafios', methods = ['GET', 'POST'])
def crea_tusdesafios():
    
    if not 'empresa_id' in session:
        print('Crea un perfil empresa')
        return redirect('/')

    #con el siguiente validaremos el metodo
    if request.method == 'GET':
        data = { 'idempresas' : session['empresa_id']}
        desafios = Desafio.get_desafios_by_empresa(data)
        return render_template('creatusdesafios.html', desafios = desafios)
    
    elif request.method == 'POST':
        print('CREANDO DESAFIO')

    #hay que pasarle los datos de lo que crearemos
    data = {
        'nombre': request.form['nombre'], #la variable en el parentesis debe ser igual al nombre que tiene el name en tu html en ese input
        'descuento' : request.form['descuento'],
        'condiciones' : request.form ['condiciones'],
        'creado' : request.form ['creado'],
        'finaliza' : request.form['finaliza'],
        'idempresas' : session['empresa_id']
    }

    Desafio.save(data)#aqui recien guardamos la receta 
    
    return redirect('/creatusdesafios')
    
