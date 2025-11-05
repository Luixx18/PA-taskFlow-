from flask import Flask, render_template, request, redirect, url_for
from src.database import DBmanager
from src.modelos import Proyecto, Tarea

app = Flask (__name__)
db_manager = DBmanager()         #conectar a la base de datos

@app.route('/')
def index():
    tareas_pendientes = db_manager.obtener_tareas(estado="Pendiente")
    proyectos = db_manager.obtener_proyectos()

    return render_template('index.html', 
                           tareas=tareas_pendientes,
                           proyectos=proyectos)


