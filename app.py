import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json

app = Flask(__name__)

app._static_folder = os.path.abspath("templates/static/")
app.config["MONGO_URI"] = "mongodb://localhost/escuela"
# Envolvemos la app en pymongo para tener acceso desde cualquier lugar
mongo = PyMongo(app)

@app.route('/docente')
def teacher():
    return render_template('layouts/docente.html')

@app.route('/')
def inicio():
    return render_template('layouts/inicio.html')

@app.route('/estudiante')
def estudiante():
    return render_template('layouts/estudiante.html')

@app.route('/rojo')
def rojo():
    return render_template('layouts/rojo.html')

@app.route('/azul')
def azul():
    return render_template('layouts/azul.html')

@app.route('/amarillo')
def amarillo():
    return render_template('layouts/amarillo.html')

@app.route('/test')
def test():
    return render_template('layouts/test.html')

@app.route('/stars')
def stars():
    return render_template('layouts/stars.html')

@app.route('/notas')
def notas():
    return render_template('layouts/notas.html')

# Procesamos los datos que envia el docente al loguearse
@app.route('/processTeacher', methods=["POST", "GET"])
def processTeacher():
    if request.method == "POST":
        # Obtenemos los datos enviamos y los almacenamos
        username = request.form["username"]
        password = request.form["password"]
        # Creamos el objeto con los datos que buscaremos
        data = {"Cedula": username, "Contraseña": password}
        # Ejecutamos la consulta
        res = mongo.db.docentes.find_one(data)
        # Verfiicamos si la consulta obtuvo resultados
        if res:
            # Retornamos un json
            return jsonify(json.dumps(res, default=str))
        else:
            return jsonify({"result": False}) 
    else:
        # En caso de querer acceder a la ruta sin enviar nada
        return f"<h1>No ha enviado datos</h1>"

@app.route('/setStars', methods=["POST", "GET"])
def setStars():
    if request.method == "POST":
        # Obtenemos los datos
        cedula = request.form["cedula"]
        stars = request.form["stars"]
        # hacemos la actualización
        result = mongo.db.estudiantes.update_one({"Id_Estudiante": cedula}, {
            "$set":{
                "Test.Estrellas": int(stars)
                }
            }
        )

        # Si la actualización salió bien retornamos un true
        if result :
            return jsonify({"result": True}) 
        else:
            return jsonify({"result": False}) 
    else:
        return f"<h1>No ha enviado datos</h1>"

# Guarda los datos del test
@app.route('/saveData', methods=["POST", "GET"])
def saveData():
    if request.method == "POST":
        cedula = request.form["cedula"]
        tiempo = request.form["tiempo"]
        resuelto = request.form["resuelto"]

        #Cambiar a booleano que viene en la request
        if resuelto == "true":
            resuelto = True
        else:
            resuelto = False

        # Hacemos el guardado de los datos
        result = mongo.db.estudiantes.update_one({"Id_Estudiante": cedula}, {
            "$set":{
                "Test.Tiempo": int(tiempo),
                "Test.Resuelto": resuelto,
                }
            }
        )

        # Si todo va bien retornamos un true
        if result :
            return jsonify({"result": True}) 
        else:
            return jsonify({"result": False}) 
    else:
        return f"<h1>No ha enviado datos</h1>"

# Obtener todos los estudiantes
@app.route('/getParalelo', methods=["POST", "GET"])
def paralelo():
    if request.method == "POST":
        # REcibimos el paralelo a buscar
        paralelo = request.form["paralelo"]
        # Hacemos la consulta
        res = list(mongo.db.estudiantes.find({"Paralelo":paralelo}))
        # Si la consulta trae resultados los retornamos
        if res:
            # Retormos un json
            return jsonify(json.dumps(res, default=str))
        else:
            return jsonify({"result": False}) 
    else:
        return f"<h1>No ha enviado datos</h1>"

if '__main__' == __name__:
    app.run(debug=True, port=5000)

