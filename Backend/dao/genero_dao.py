import pyodbc
from config.logger import Logger
from config.base_datos import obtener_conexion, ErrorOperacionBD
from modelos.genero import Genero

#==========================================================================================================
#  CREANDO MIS EXCEPCIONES
#==========================================================================================================
class GeneroNoEncontradoError(Exception):
    def __init__(self, genero_id):
        super().__init__(f"Genero ID={genero_id} no encontrado")


class GeneroDuplicadoError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Genero '{nombre}' ya registrado")


class GeneroConTitulosError(Exception):
    def __init__(self, genero_id):
        super().__init__(f"Genero ID={genero_id} no se puede eliminar: tiene titulos asociados")

#==========================================================================================================
#  CREANDO la clase Genero_dao
#==========================================================================================================
class GeneroDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, genero):
        if self.buscar_por_nombre(genero.nombre):
            # Validamos que no haiga un genero duplicado
            self.__log.warning(f"Genero duplicado: {genero.nombre}")
            raise GeneroDuplicadoError(genero.nombre)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(ID_GENERO), 0) + 1 FROM GENERO")
            nuevo_id = cursor.fetchone()[0]

            # Insertamos el registro
            cursor.execute(
                "INSERT INTO GENERO (ID_GENERO, NOMBRE, DESCRIPCION) VALUES (?, ?, ?)",
                (nuevo_id, genero.nombre, genero.descripcion)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al insertar genero '{genero.nombre}': {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        genero.id = nuevo_id
        self.__log.info(f"Genero agregado: {genero.nombre} (ID={genero.id})")
        return genero

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GENERO WHERE NOMBRE = ?", (nombre,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_genero(fila) if fila else None

    def buscar_por_id(self, genero_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GENERO WHERE ID_GENERO = ?", (genero_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_genero(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GENERO ORDER BY NOMBRE")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_genero(f) for f in filas]

    def actualizar(self, genero_id, nombre=None, descripcion=None):
        g = self.buscar_por_id(genero_id)
        if not g:
            #No me deja actualizar si no encuentra el genero por su id
            self.__log.error(f"Actualizar fallido: Genero ID={genero_id} no existe")
            raise GeneroNoEncontradoError(genero_id)

        nuevo_nombre = nombre if nombre is not None else g.nombre
        nueva_descripcion = descripcion if descripcion is not None else g.descripcion

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE GENERO SET NOMBRE = ?, DESCRIPCION = ? WHERE ID_GENERO = ?",
                (nuevo_nombre, nueva_descripcion, genero_id)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al actualizar genero ID={genero_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        g.nombre = nuevo_nombre
        g.descripcion = nueva_descripcion
        self.__log.info(f"Genero actualizado: ID={genero_id}")
        return g

    def eliminar(self, genero_id):
        g = self.buscar_por_id(genero_id)
        if not g:
            #Aca tampoco me deja eliminar si no encuentra el genero por su id y muestra este mensaje
            self.__log.error(f"Eliminar fallido: Genero ID={genero_id} no existe")
            raise GeneroNoEncontradoError(genero_id)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM GENERO WHERE ID_GENERO = ?", (genero_id,))
            conn.commit()
        except pyodbc.IntegrityError:
            #Aca te sale un mensaje que no puedes eliminar este genero ya q hay un titulo de serie o pelicula que ya esta usando ese genero
            self.__log.warning(f"Eliminar fallido: Genero ID={genero_id} tiene titulos asociados")
            raise GeneroConTitulosError(genero_id)
        except pyodbc.Error as ex:
            self.__log.error(f"Error al eliminar genero ID={genero_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        self.__log.info(f"Genero eliminado: {g.nombre} (ID={genero_id})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM GENERO")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def __fila_a_genero(self, fila):
        g = Genero(fila.NOMBRE, fila.DESCRIPCION)
        g.id = fila.ID_GENERO
        return g