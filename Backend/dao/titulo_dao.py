import psycopg2
import datetime
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.titulo import Titulo, TipoContenido, EstadoVisu
from dao.genero_dao import GeneroNoEncontradoError
from dao.director_dao import DirectorNoEncontradoError

#===============================================
#CREANDO MIS EXEPCIONES
#===============================================

# Cuando no se encuentra el título por su ID
class TituloNoEncontradoError(Exception):
    def __init__(self, titulo_id):
        super().__init__(f"Titulo ID = {titulo_id} no encontrado")

# Duplicado si coincide título + director + año
class TituloDuplicadoError(Exception):
    # Se considera duplicado si coincide titulo + director + anio.
    def __init__(self, titulo, anio):
        super().__init__(f"Titulo '{titulo}' ({anio}) ya registrado con ese mismo director")

# Cuando el año está fuera del rango permitido (desde 1888 hasta año actual + 5)
class AnioInvalidoError(Exception):
    ANIO_MINIMO = 1888

    def __init__(self, anio):
        anio_maximo = datetime.datetime.now().year + 5
        super().__init__(
            f"Anio invalido ({anio}): debe estar entre {AnioInvalidoError.ANIO_MINIMO} y {anio_maximo}"
        )

# Cuando la calificación no está entre 1 y 10
class CalificacionInvalidaError(Exception):
    def __init__(self, nota):
        super().__init__(f"Calificacion invalida ({nota}): debe estar entre 1 y 10")

#===============================================
#CREANDO CLASE TITULODAO
#===============================================
# --- Clase principal que maneja los títulos en la base de datos ---
class TituloDAO:
    def __init__(self, genero_dao, director_dao):
        self.__log = Logger() # Para registrar lo que va pasando
        self.__genero_dao = genero_dao # DAO de géneros para validar
        self.__director_dao = director_dao # DAO de directores para validar

    def insertar(self, titulo):
        # Verificamos que el género exista antes de continuar
        if not self.__genero_dao.buscar_por_id(titulo.id_genero):
            self.__log.warning(f"Genero inexistente al crear titulo: ID = {titulo.id_genero}")
            raise GeneroNoEncontradoError(titulo.id_genero)
        
        # Verificamos que el director exista antes de continuar
        if not self.__director_dao.buscar_por_id(titulo.id_director):
            self.__log.warning(f"Director inexistente al crear titulo: ID = {titulo.id_director}")
            raise DirectorNoEncontradoError(titulo.id_director)
        
        # Validamos que el año esté dentro del rango permitido
        self.__validar_anio(titulo.anio)

        # Verificamos que no exista el mismo título con el mismo director y año
        if self.__buscar_duplicado(titulo.titulo, titulo.id_director, titulo.anio):
            self.__log.warning(f"Titulo duplicado: {titulo.titulo} ({titulo.anio})")
            raise TituloDuplicadoError(titulo.titulo, titulo.anio)

        # Si todo está bien, insertamos el título y guardamos el ID generado
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO titulo
            (titulo, tipo, anio, calificacion, estado, id_genero, id_director)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (titulo.titulo, titulo.tipo.value, titulo.anio,
            titulo.calificacion, titulo.estado.value,
            titulo.id_genero, titulo.id_director)
        )
        titulo.id = cursor.fetchone()["id"] # Guardamos el ID que generó la BD
        conn.commit()
        conn.close()
        self.__log.info(f"Titulo agregado: {titulo.titulo} (ID = {titulo.id})")
        return titulo

    def buscar_por_id(self, titulo_id):
        # Buscamos un título por su ID
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM titulo WHERE id = %s", (titulo_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_titulo(fila) if fila else None

    def obtener_todos(self):
        # Traemos todos los títulos ordenados alfabéticamente
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM titulo ORDER BY titulo")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_titulo(f) for f in filas]

    def eliminar(self, titulo_id):
        # Verificamos que el título exista antes de eliminarlo
        t = self.buscar_por_id(titulo_id)
        if not t:
            self.__log.error(f"Eliminar fallido: Titulo ID = {titulo_id} no existe")
            raise TituloNoEncontradoError(titulo_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM titulo WHERE id = %s", (titulo_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Titulo eliminado: {t.titulo} (ID = {titulo_id})")
        return True

    def actualizar(self, titulo_id, titulo=None, anio=None):
        # Verificamos que el título exista antes de actualizarlo
        t = self.buscar_por_id(titulo_id)
        if not t:
            self.__log.error(f"Actualizar fallido: Titulo ID = {titulo_id} no existe")
            raise TituloNoEncontradoError(titulo_id)

        # Si no se pasa un valor nuevo, se conserva el que ya tenía
        nuevo_titulo = titulo if titulo is not None else t.titulo
        nuevo_anio = anio if anio is not None else t.anio

        # Solo validamos el año si se está cambiando
        if anio is not None:
            self.__validar_anio(anio)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE titulo SET titulo=%s, anio=%s WHERE id=%s",
            (nuevo_titulo, nuevo_anio, titulo_id)
        )
        conn.commit()
        conn.close()
        t.titulo = nuevo_titulo
        t.anio = nuevo_anio
        self.__log.info(f"Titulo actualizado: ID = {titulo_id}")
        return t

    def marcar_visto(self, titulo_id):
        return self.__cambiar_estado(titulo_id, EstadoVisu.VISTO)

    def marcar_pendiente(self, titulo_id):
        return self.__cambiar_estado(titulo_id, EstadoVisu.PENDIENTE)

    def __cambiar_estado(self, titulo_id, nuevo_estado):
        # Verificamos que el título exista y actualizamos su estado
        t = self.buscar_por_id(titulo_id)
        if not t:
            raise TituloNoEncontradoError(titulo_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE titulo SET estado=%s WHERE id=%s",
            (nuevo_estado.value, titulo_id)
        )
        conn.commit()
        conn.close()
        t.estado = nuevo_estado
        self.__log.info(f"Titulo marcado {nuevo_estado.value}: ID = {titulo_id}")
        return t

    def calificar(self, titulo_id, nota):
        # Verificamos que el título exista y que la nota esté entre 1 y 10
        t = self.buscar_por_id(titulo_id)
        if not t:
            raise TituloNoEncontradoError(titulo_id)
        if not (1 <= nota <= 10):
            self.__log.warning(f"Calificar fallido: nota {nota} fuera de rango (titulo ID = {titulo_id})")
            raise CalificacionInvalidaError(nota)

        # Guardamos la calificación en la BD
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE titulo SET calificacion=%s WHERE id=%s",
            (nota, titulo_id)
        )
        conn.commit()
        conn.close()
        t.calificacion = nota
        self.__log.info(f"Titulo calificado: ID = {titulo_id} Nota = {nota}")
        return t

    def total(self):
        # Contamos cuántos títulos hay en la tabla
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM titulo")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_titulo(self, fila):
        # Convertimos una fila de la BD en un objeto Titulo
        t = Titulo(
            fila["titulo"],
            TipoContenido(fila["tipo"]),
            fila["anio"],
            fila["id_genero"],
            fila["id_director"],
            float(fila["calificacion"]) if fila["calificacion"] is not None else None
        )
        t.id = fila["id"]
        t.estado = EstadoVisu(fila["estado"])
        return t

    def __validar_anio(self, anio):
        # Verificamos que el año esté entre 1888 y el año actual + 5
        anio_maximo = datetime.datetime.now().year + 5
        if not (AnioInvalidoError.ANIO_MINIMO <= anio <= anio_maximo):
            self.__log.warning(f"Anio invalido: {anio}")
            raise AnioInvalidoError(anio)

    def __buscar_duplicado(self, titulo_txt, id_director, anio):
        # Buscamos si ya existe un título igual con el mismo director y año
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM titulo WHERE titulo = %s AND id_director = %s AND anio = %s",
            (titulo_txt, id_director, anio)
        )
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_titulo(fila) if fila else None
