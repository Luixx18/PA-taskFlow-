import sqlite3
from modelos import Tarea, Proyecto
import os


DATABASE_NAME = "tareas.db"


def get_connection():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn

def crear_tabla():
    conn   = get_connection() 
    cursor = conn.cursor()

    #tabla proyectos
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS proyectos
                   id INTERGER PRIMARY KEY AUTOINCREMENT,
                   nombre       TEXT NOT NULL,
                   descripcion  TEXT,
                   fecha_inicio TEXT,  
                   estado       TEXT                  
                    )
                   """)
    
    #tabla tareas 
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                   id INTERGER PRIMARY KEY AUTOINCREMENT,
                   titulo         TEXT,
                   descripcion    TEXT,
                   fecha_creacion TEXT, 
                   fecha_limite   TEXT,
                   prioridad      TEXT,
                   estado         TEXT,
                   proyecto_id INTEGER,
                   FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
                   )
                   """)

    try: 
        cursor.execute("INSERT INTO proyectos (id, nombre, descripcion, estado) VAULES (0, 'Tareas generales, 'Tareas sin clasificar', 'Activo')")              
    except sqlite3.IntegrityError:
        pass  # El proyecto ya existe, no hacer nada

    conn.commit()
    conn.close()



#dbm= database manager
class DBmanager:
    
    def __init__(self):
        crear_tabla()


    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id
            VALUES (?, ?, ?, ?, ?, ?, ? )) 
            """, (Tarea._titulo, Tarea._descripcion, Tarea._fecha_creacion,
                  Tarea._fecha_limite, Tarea._prioridad, Tarea._estado,
                  Tarea._proyecto_id))


        Tarea.id = cursor.lastrowid
        #funcion commit guarrda los cambios en la base de datos
        conn.commit()
        #duncion close cierra la conexion a la base de datos
        conn.close()
        return Tarea



    def obtener_proyectos(self) -> list[Proyecto]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FORM proyectos")
        filas = cursor.fetchall()
        conn.close()

        proyectos = [
            Proyecto(nombre      = fila ['nombre'],
                     descripcion = fila ['descripcion'],
                     id          = fila ['id'],
                     estado      = fila ['estado'])
        
        for fila in filas
        ]
        return proyectos
            
    
    def obtener_tareas(self, estado=None): 
        #aplicar un algoritmo de ordenamiento y filtrado
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM tareas"
        params = []

        if estado: 
            sql += " WHERE estado = ?"
            params.append(estado)

        sql += " ORDER BY fecha_limite ASC"

        cursor.execute(sql, params)
        filas = cursor.fetchall()
        conn.close()


        tareas = []
        for fila in filas:
            t = Tarea(
                titulo         = fila['titulo'],
                descripcion    = fila['descripcion'],
                fecha_limite   = fila['fecha_limite'],
                prioridad      = fila['prioridad'],
                fecha_creacion = fila['fecha_creacion'],
                proyecto_id    = fila['proyecto_id'],
                id             = fila['id'],
                estado         = fila['estado']
            )
            tareas.append(t)
        return tareas
     