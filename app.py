import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json

app = Flask(__name__)

app._static_folder = os.path.abspath("templates/static/")
app.config["MONGO_URI"] = "mongodb://localhost/escuela"
mongo = PyMongo(app)

@app.route('/login')
def teacher():
    return render_template('layouts/docente.html')

@app.route('/inicio')
def inicio():
    return render_template('layouts/login_estudiantes.html')

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

@app.route('/notas')
def notas():
    return render_template('layouts/notas.html')

@app.route('/processTeacher', methods=["POST", "GET"])
def processTeacher():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        data = {"Cedula": username, "Contraseña": password}
        if mongo.db.docentes.find_one(data):
            return jsonify({"result": True}) 
        else:
            return jsonify({"result": False}) 
    else:
        return f"<h1>No ha enviado datos</h1>"

@app.route('/getEstudiantes', methods=["POST", "GET"])
def getEstudiantes():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        data = {"Cedula": username, "Contraseña": password}
        if mongo.db.docentes.find_one(data):
            return jsonify({"result": True}) 
        else:
            return jsonify({"result": False}) 
    else:
        return f"<h1>No ha enviado datos</h1>"

@app.route('/saveData', methods=["POST", "GET"])
def saveData():
    if request.method == "POST":
        cedula = request.form["cedula"]
        tiempo = request.form["tiempo"]
      
        return jsonify({"result": True}) 
    else:
        return f"<h1>No ha enviado datos</h1>"

@app.route('/getParalelo', methods=["POST", "GET"])
def paralelo():
    if request.method == "POST":
        paralelo = request.form["paralelo"]
        res = list(mongo.db.estudiantes.find({"Paralelo":paralelo}))

        if res:
            return jsonify(json.dumps(res, default=str))
        else:
            return jsonify({"result": False}) 
            

    else:
        return f"<h1>No ha enviado datos</h1>"

if '__main__' == __name__:
    app.run(debug=True, port=5000)

