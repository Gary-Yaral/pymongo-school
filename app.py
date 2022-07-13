import os
from flask import Flask, render_template
from pymongo import MongoClient
from data.docentes import docentesData 
from data.paraleloA import paraleloA 
from data.paraleloB import paraleloB 

app=Flask(__name__)
app._static_folder = os.path.abspath("templates/static/")
# Definimos la uri de conexión a mongodb local
MONGO_URI = "mongodb://localhost"
# Creamos la conexión
client = MongoClient(MONGO_URI) 
# Creamos la base de datos
db = client["escuela"]

# Primero verificamos si no la collecion estudiantes no existe
if (("estudiantes" in db.list_collection_names()) == False):
    estudiantes = db["estudiantes"] # Creamos la colección
    estudiantes.insert_many(paraleloA) # Agregamos los 10 estudiantes de paralelo A
    estudiantes.insert_many(paraleloB) # Agregamos los 10 estudiantes de paralelo B

# Primero verificamos si no la collecion docentes no existe
if (("docentes" in db.list_collection_names()) == False):
    docentes = db["docentes"] # Creamos la colección
    docentes.insert_many(docentesData) # Agregamos los docentes de ambos paralelos

@app.route("/")
def index():
    return render_template("layouts/index.html")

@app.route("/docente")
def teacher():
    return render_template("layouts/login_docente.html")

@app.route("/estudiante")
def student():
    return render_template("layouts/login_estudiante.html")

@app.route("/colores")
def colors():
    return render_template("layouts/colores.html")

@app.route("/colores")
def test():
    return render_template("layouts/test.html")

if __name__=='__main__':
    app.run(debug=True, port=5000)
