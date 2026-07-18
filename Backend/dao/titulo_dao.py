import pyodbc
import datetime
from config.logger import Logger
from config.base_datos import obtener_conexion, ErrorOperacionBD
from modelos.titulo import Titulo
from modelos.enums import TipoContenido, EstadoVisu
from dao.genero_dao import GeneroNoEncontradoError
from dao.director_dao import DirectorNoEncontradoError

#==========================================================================================================
#  CREANDO MIS EXCEPCIONES
#==========================================================================================================

class TituloNoEncontradoError(Exception):
    def __init__(self, titulo_id):
        super().__init__(f"Titulo ID={titulo_id} no encontrado")

class TituloDuplicadoError(Exception):
    def __init__(self, titulo, anio):
        super().__init__(f"Titulo '{titulo}' ({anio}) ya registrado con ese mismo director")

class AnioInvalidoError(Exception):
    ANIO_MINIMO = 1888

    def __init__(self, anio):
        anio_maximo = datetime.datetime.now().year + 5
        super().__init__(
            f"Anio invalido ({anio}): debe estar entre {AnioInvalidoError.ANIO_MINIMO} y {anio_maximo}"
        )

class CalificacionInvalidaError(Exception):
    def __init__(self, nota):
        super().__init__(f"Calificacion invalida ({nota}): debe estar entre 1 y 10")


#==========================================================================================================
#  CREANDO LA CLASE TituloDAO CON LOS METODOS QUE SE USA EN UN CRUD 
#==========================================================================================================
class TituloDAO:
    def __init__(self, genero_dao, director_dao):
        self.__log = Logger()
        self.__genero_dao = genero_dao
        self.__director_dao = director_dao

    def insertar(self, titulo):
        if not self.__genero_dao.buscar_por_id(titulo.id_genero):
            self.__log.warning(f"Genero inexistente al crear titulo: ID={titulo.id_genero}")
            raise GeneroNoEncontradoError(titulo.id_genero)
        if not self.__director_dao.buscar_por_id(titulo.id_director):
            self.__log.warning(f"Director inexistente al crear titulo: ID={titulo.id_director}")
            raise DirectorNoEncontradoError(titulo.id_director)

        self.__validar_anio(titulo.anio)

        if self.__buscar_duplicado(titulo.titulo, titulo.id_director, titulo.anio):
            self.__log.warning(f"Titulo duplicado: {titulo.titulo} ({titulo.anio})")
            raise TituloDuplicadoError(titulo.titulo, titulo.anio)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT ISNULL(MAX(ID_TITULO), 0) + 1 FROM TITULO")
            nuevo_id = cursor.fetchone()[0]

            cursor.execute(
                """INSERT INTO TITULO
                   (ID_TITULO, TITULO, TIPO, ANIO, CALIFICACION, ESTADO, ID_GENERO, ID_DIRECTOR)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (nuevo_id, titulo.titulo, titulo.tipo.value, titulo.anio,
                 titulo.calificacion, titulo.estado.value,
                 titulo.id_genero, titulo.id_director)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al insertar titulo '{titulo.titulo}': {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        titulo.id = nuevo_id
        self.__log.info(f"Titulo agregado: {titulo.titulo} (ID={titulo.id})")
        return titulo

    def buscar_por_id(self, titulo_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TITULO WHERE ID_TITULO = ?", (titulo_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_titulo(fila) if fila else None

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TITULO ORDER BY TITULO")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_titulo(f) for f in filas]

    def actualizar(self, titulo_id, titulo=None, anio=None):
        t = self.buscar_por_id(titulo_id)
        if not t:
            self.__log.error(f"Actualizar fallido: Titulo ID={titulo_id} no existe")
            raise TituloNoEncontradoError(titulo_id)

        nuevo_titulo = titulo if titulo is not None else t.titulo
        nuevo_anio = anio if anio is not None else t.anio

        if anio is not None:
            self.__validar_anio(anio)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE TITULO SET TITULO = ?, ANIO = ? WHERE ID_TITULO = ?",
                (nuevo_titulo, nuevo_anio, titulo_id)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al actualizar titulo ID={titulo_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        t.titulo = nuevo_titulo
        t.anio = nuevo_anio
        self.__log.info(f"Titulo actualizado: ID={titulo_id}")
        return t

    def eliminar(self, titulo_id):
        t = self.buscar_por_id(titulo_id)
        if not t:
            self.__log.error(f"Eliminar fallido: Titulo ID={titulo_id} no existe")
            raise TituloNoEncontradoError(titulo_id)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM TITULO WHERE ID_TITULO = ?", (titulo_id,))
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al eliminar titulo ID={titulo_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        self.__log.info(f"Titulo eliminado: {t.titulo} (ID={titulo_id})")
        return True

    def marcar_visto(self, titulo_id):
        return self.__cambiar_estado(titulo_id, EstadoVisu.VISTO)

    def marcar_pendiente(self, titulo_id):
        return self.__cambiar_estado(titulo_id, EstadoVisu.PENDIENTE)

    def __cambiar_estado(self, titulo_id, nuevo_estado):
        t = self.buscar_por_id(titulo_id)
        if not t:
            raise TituloNoEncontradoError(titulo_id)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE TITULO SET ESTADO = ? WHERE ID_TITULO = ?",
                (nuevo_estado.value, titulo_id)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al cambiar estado de titulo ID={titulo_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        t.estado = nuevo_estado
        self.__log.info(f"Titulo marcado {nuevo_estado.value}: ID={titulo_id}")
        return t

    def calificar(self, titulo_id, nota):
        t = self.buscar_por_id(titulo_id)
        if not t:
            raise TituloNoEncontradoError(titulo_id)
        if not (1 <= nota <= 10):
            # Aca valido que la CALIFICACION sea entre 1 y 10).
            self.__log.warning(f"Calificar fallido: nota {nota} fuera de rango (titulo ID={titulo_id})")
            raise CalificacionInvalidaError(nota)

        conn = obtener_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE TITULO SET CALIFICACION = ? WHERE ID_TITULO = ?",
                (nota, titulo_id)
            )
            conn.commit()
        except pyodbc.Error as ex:
            self.__log.error(f"Error al calificar titulo ID={titulo_id}: {ex}")
            raise ErrorOperacionBD(ex)
        finally:
            conn.close()

        t.calificacion = nota
        self.__log.info(f"Titulo calificado: ID={titulo_id} Nota={nota}")
        return t

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM TITULO")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def __fila_a_titulo(self, fila):
        t = Titulo(
            fila.TITULO,
            TipoContenido(fila.TIPO),
            fila.ANIO,
            fila.ID_GENERO,
            fila.ID_DIRECTOR,
            float(fila.CALIFICACION) if fila.CALIFICACION is not None else None
        )
        t.id = fila.ID_TITULO
        t.estado = EstadoVisu(fila.ESTADO)
        return t

    def __validar_anio(self, anio):
        anio_maximo = datetime.datetime.now().year + 5
        if not (AnioInvalidoError.ANIO_MINIMO <= anio <= anio_maximo):
            self.__log.warning(f"Anio invalido: {anio}")
            raise AnioInvalidoError(anio)

    def __buscar_duplicado(self, titulo_txt, id_director, anio):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM TITULO WHERE TITULO = ? AND ID_DIRECTOR = ? AND ANIO = ?",
            (titulo_txt, id_director, anio)
        )
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_titulo(fila) if fila else None
