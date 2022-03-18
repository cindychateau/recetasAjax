from flask import render_template, redirect, session, request, flash, jsonify
from flask_app import app

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['POST'])
def register():
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario)

    session['user_id'] = id

    return redirect('/dashboard')

@app.route("/login", methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    #user = User -> first_name, last_name, password, email ....

    if not user:
        #flash("E-mail no encontrado", "login")
        #return redirect('/')
        return jsonify(message="E-mail no encontrado")
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        #flash("Password incorrecto", "login")
        #return redirect('/')
        return jsonify(message="Password incorrecto")
    
    session['user_id'] = user.id
    #return redirect('/dashboard')
    return jsonify(message="correcto")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }
    
    user = User.get_by_id(data)
    #Recetas
    recipes = Recipe.get_all()
    
    return render_template('dashboard.html', user=user, recipes=recipes)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')