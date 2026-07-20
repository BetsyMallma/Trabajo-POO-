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

#==========================================================================================================
#  CREANDO director_dao
#==========================================================================================================
class DirectorDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, director):
        # Aca valido si hay un director duplicado y si hay sale este mensaje
        if self.buscar_por_nombre_apellido(director.nombre, director.apellido):
            self.__log.warning(f"Director duplicado: {director.nombre} {director.apellido}")
            raise DirectorDuplicadoError(director.nombre, director.apellido)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT ISNULL(MAX(ID_DIRECTOR), 0) + 1 FROM DIRECTOR")
            nuevo_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO DIRECTOR (ID_DIRECTOR, NOMBRE, APELLIDO, NACIONALIDAD) VALUES (?, ?, ?, ?)",
                (nuevo_id, director.nombre, director.apellido, director.nacionalidad)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al insertar director '{director.nombre} {director.apellido}': {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        director.id = nuevo_id
        self.__log.info(f"Director agregado: {director.nombre} {director.apellido} (ID={director.id})")
        return director

    def buscar_por_id(self, director_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DIRECTOR WHERE ID_DIRECTOR = ?", (director_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_director(fila) if fila else None

    def buscar_por_nombre_apellido(self, nombre, apellido):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM DIRECTOR WHERE NOMBRE = ? AND APELLIDO = ?",
            (nombre, apellido)
        )
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_director(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DIRECTOR ORDER BY APELLIDO")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_director(f) for f in filas]

    def actualizar(self, director_id, nombre=None, apellido=None, nacionalidad=None):
        d = self.buscar_por_id(director_id)
        # En este caso busco al director por su ID para poder actualizar, si no lo encuentra me aparece este mensaje 
        if not d:
            self.__log.error(f"Actualizar fallido: Director ID={director_id} no existe")
            raise DirectorNoEncontradoError(director_id)

        nuevo_nombre = nombre if nombre is not None else d.nombre
        nuevo_apellido = apellido if apellido is not None else d.apellido
        nueva_nacionalidad = nacionalidad if nacionalidad is not None else d.nacionalidad

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE DIRECTOR SET NOMBRE = ?, APELLIDO = ?, NACIONALIDAD = ? WHERE ID_DIRECTOR = ?",
                (nuevo_nombre, nuevo_apellido, nueva_nacionalidad, director_id)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al actualizar director ID={director_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        d.nombre = nuevo_nombre
        d.apellido = nuevo_apellido
        d.nacionalidad = nueva_nacionalidad
        self.__log.info(f"Director actualizado: ID={director_id}")
        return d

    def eliminar(self, director_id):
        d = self.buscar_por_id(director_id)
        # Aca busco el ID del director para poder eliminar, si no lo encuentra sale este mensaje
        if not d:
            self.__log.error(f"Eliminar fallido: Director ID={director_id} no existe")
            raise DirectorNoEncontradoError(director_id)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM DIRECTOR WHERE ID_DIRECTOR = ?", (director_id,))
            conn.commit()
        except pyodbc.IntegrityError:
            #Aca le estoy diciendo que no puede eliminar al director ya que hay peliculas o series q lo llevan
            self.__log.warning(f"Eliminar fallido: Director ID={director_id} tiene titulos asociados")
            raise DirectorConTitulosError(director_id)
        except pyodbc.Error as ex:
            self.__log.error(f"Error al eliminar director ID={director_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        self.__log.info(f"Director eliminado: {d.nombre} {d.apellido} (ID={director_id})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM DIRECTOR")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def __fila_a_director(self, fila):
        d = Director(fila.NOMBRE, fila.APELLIDO, fila.NACIONALIDAD)
        d.id = fila.ID_DIRECTOR
        return d
