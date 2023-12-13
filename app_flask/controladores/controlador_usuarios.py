from flask import render_template, redirect, request, session, flash
from app_flask import app
from app_flask.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt 

bcrypt = Bcrypt(app)

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/dashboard')
def desplegar_dash():
    if "id" not in session:
        return redirect('/')
    return render_template("dashboard.html")

@app.route('/procesar/registro', methods=['POST'])
def procesar_registro():
    if Usuario.validacion_registro(request.form) == False:
        return redirect('/')
    password_encriptado = bcrypt.generate_password_hash(request.form['contraseña'])
    nuevo_usuario = {
        **request.form,
        'contraseña': password_encriptado
    }
    id = Usuario.crear_user(nuevo_usuario)
    session['id'] = id
    session['nombre'] = nuevo_usuario['nombre']
    session['apellido'] = nuevo_usuario['apellido']
    return redirect('/dashboard')

@app.route('/procesar/login', methods=['POST'])
def procesar_login():
    usuario_login = Usuario.obtener_user(request.form)
    if usuario_login == None:
        flash('Este correo no existe', 'error_login')
        return redirect('/')
    if not bcrypt.check_password_hash(usuario_login.contraseña, request.form['contraseña']):
        flash('Credenciales incorrectas', 'error_login')
        return redirect('/')
    
    session['id'] = usuario_login.id
    session['nombre'] = usuario_login.nombre
    session['apellido'] = usuario_login.apellido
    return redirect('/dashboard')

@app.route('/procesar/logout', methods=['POST'])
def procesar_logout():
    session.clear()
    return redirect('/')

