#Importo con el import las rutas
import pyodbc
from config.logger import Logger
from config.base_datos import obtener_conexion, ErrorOperacionBD
from modelos.director import Director

#==========================================================================================================
#  CREANDO MIS EXCEPCIONES
#==========================================================================================================
class DirectorNoEncontradoError(Exception):
    def __init__(self, director_id):
        super().__init__(f"Director ID={director_id} no encontrado")

class DirectorDuplicadoError(Exception):
    def __init__(self, nombre, apellido):
        super().__init__(f"Director '{nombre} {apellido}' ya registrado")

class DirectorConTitulosError(Exception):
    def __init__(self, director_id):
        super().__init__(f"Director ID={director_id} no se puede eliminar: tiene titulos asociados")