import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.genero import Genero

#===============================================
#CREANDO MIS EXEPCIONES
#===============================================
class GeneroNoEncontradoError(Exception):
    def __init__(self, genero_id):
        super().__init__(f"Genero ID = {genero_id} no encontrado")

class GeneroDuplicadoError(Exception):
    def __init__(self, nombre):
        super().__init__(f"Genero '{nombre}' ya registrado")

class GeneroConTitulosError(Exception):
    def __init__(self, genero_id):
        super().__init__(f"Genero ID = {genero_id} no se puede eliminar: tiene titulos asociados")

#===============================================
#CREANDO CLASE GENERODAO
#===============================================

class GeneroDAO:
    def __init__(self):
        self.__log = Logger()

    def insertar(self, genero):
        if self.buscar_por_nombre(genero.nombre):
            self.__log.warning(f"Genero duplicado: {genero.nombre}")
            raise GeneroDuplicadoError(genero.nombre)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO genero (nombre, descripcion) VALUES (%s, %s) RETURNING id",
            (genero.nombre, genero.descripcion)
        )
        genero.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Genero agregado: {genero.nombre} (ID = {genero.id})")
        return genero

    def buscar_por_nombre(self, nombre):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM genero WHERE nombre = %s", (nombre,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_genero(fila) if fila else None

    def buscar_por_id(self, genero_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM genero WHERE id = %s", (genero_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_genero(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM genero ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_genero(f) for f in filas]

    def eliminar(self, genero_id):
        g = self.buscar_por_id(genero_id)
        if not g:
            self.__log.error(f"Eliminar fallido: Genero ID = {genero_id} no existe")
            raise GeneroNoEncontradoError(genero_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM genero WHERE id = %s", (genero_id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self.__log.warning(f"Eliminar fallido: Genero ID = {genero_id} tiene titulos asociados")
            raise GeneroConTitulosError(genero_id)
        conn.close()
        self.__log.info(f"Genero eliminado: {g.nombre} (ID = {genero_id})")
        return True

    def actualizar(self, genero_id, nombre=None, descripcion=None):
        g = self.buscar_por_id(genero_id)
        if not g:
            self.__log.error(f"Actualizar fallido: Genero ID = {genero_id} no existe")
            raise GeneroNoEncontradoError(genero_id)

        nuevo_nombre = nombre if nombre is not None else g.nombre
        nueva_descripcion = descripcion if descripcion is not None else g.descripcion

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE genero SET nombre=%s, descripcion=%s WHERE id=%s",
            (nuevo_nombre, nueva_descripcion, genero_id)
        )
        conn.commit()
        conn.close()
        g.nombre = nuevo_nombre
        g.descripcion = nueva_descripcion
        self.__log.info(f"Genero actualizado: ID = {genero_id}")
        return g

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM genero")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_genero(self, fila):
        g = Genero(fila["nombre"], fila["descripcion"])
        g.id = fila["id"]
        return g
