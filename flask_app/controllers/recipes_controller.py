from flask import render_template, redirect, session, request, flash
from flask_app import app

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

#Para subir imágenes
from werkzeug.utils import secure_filename
import os

@app.route("/new/recipe")
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    return render_template('new_recipe.html', user=user)

@app.route("/create/recipe", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')

    # formulario = {
    #     "name": request.form['name'],
    #     "description": request.form['description'],
    #     "instructions": request.form['instructions'],
    #     "data_made": request.form['data_made'],
    #     "user_id": request.form['user_id'],
    #     "under30": int(request.form['under30']),
    # }
    
    if not Recipe.valida_receta(request.form):
        return redirect("/new/recipe")
    
    if 'image' not in request.files:
        flash('Imagen no encontrada', 'receta')
        return redirect("/new/recipe")

    image = request.files['image']

    if image.filename == '':
        flash('Nombre de imagen vacío', 'receta')
        return redirect("/new/recipe")

    nombre_imagen = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))

    formulario = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "instructions" : request.form['instructions'],
        "date_made" : request.form['date_made'],
        "user_id" : request.form['user_id'],
        "under30" : request.form['under30'],
        "image": nombre_imagen
    }

    Recipe.save(formulario)
    return redirect("/dashboard")

@app.route("/edit/recipe/<int:id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    user = User.get_by_id(data)

    #Necesitamos los datos de la receta
    data_receta = {
        "id": id
    }
    recipe = Recipe.get_by_id(data_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route("/update/recipe", methods=["POST"])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.valida_receta(request.form):
        return redirect("/edit/recipe/"+request.form['id'])
    
    Recipe.update(request.form)

    return redirect("/dashboard")

@app.route("/show/recipe/<int:id>")
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data_receta = {
        "id": id
    }
    recipe = Recipe.get_by_id(data_receta)

    return render_template("show_recipe.html", recipe=recipe)

@app.route("/delete/recipe/<int:id>")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id":id
    }

    Recipe.delete(data)
    return redirect("/dashboard")