import os
import psycopg2
from psycopg2.extras import RealDictCursor

#Esto permite que el archivo .env se ejecute
from dotenv import load_dotenv
load_dotenv()

#================================================
# Creo la clase obtener_conexion
#================================================
def obtener_conexion():
    #Credenciales
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "bd_sps"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )
    conn.cursor_factory = RealDictCursor
    return conn

#================================================
# Creo la clase inicializar
#================================================
def inicializar():
    # Crea las tablas si aún no existen. Se llama UNA vez al iniciar el sistema.
    # "IF NOT EXISTS" evita un error si la tabla ya fue creada en una ejecución anterior.
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genero (
            id          SERIAL PRIMARY KEY,
            nombre      VARCHAR(80)  NOT NULL,
            descripcion VARCHAR(200)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS director (
            id           SERIAL PRIMARY KEY,
            nombre       VARCHAR(60) NOT NULL,
            apellido     VARCHAR(60) NOT NULL,
            nacionalidad VARCHAR(60)
        )
    """)
    # Tabla de titulo: tiene FOREIGN KEY que enlaza con genero y director.
    # FOREIGN KEY garantiza integridad referencial: no se puede registrar un
    # titulo con un id_genero o id_director que no exista en sus tablas respectivas.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS titulo (
            id           SERIAL PRIMARY KEY,
            titulo       VARCHAR(150) NOT NULL,
            tipo         VARCHAR(10)  NOT NULL CHECK (tipo IN ('PELICULA','SERIE')),
            anio         INT          NOT NULL,
            calificacion NUMERIC(3,1) CHECK (calificacion >= 1 AND calificacion <= 10),
            estado       VARCHAR(10)  NOT NULL CHECK (estado IN ('VISTO','PENDIENTE')),
            id_genero    INTEGER      NOT NULL,
            id_director  INTEGER      NOT NULL,
            FOREIGN KEY (id_genero)   REFERENCES genero(id),
            FOREIGN KEY (id_director) REFERENCES director(id)
        )
    """)
    # conn.commit() confirma todos los cambios (equivale a "guardar" en la BD).
    # Sin commit(), los cambios se pierden al cerrar la conexión.
    conn.commit()
    conn.close()