import enum

class TipoContenido(str, enum.Enum):
    PELICULA = "PELICULA"
    SERIE = "SERIE"
    
class EstadoVisu(str, enum.Enum):
    VISTO = "VISTO"
    PENDIENTE = "PENDIENTE"
    
# ──────────────────────────────────────────────────────────────────────────────
# MODELO — Titulo
# ──────────────────────────────────────────────────────────────────────────────
class Titulo:
    def __init__(self, titulo, tipo, anio, id_genero, id_director, calificacion=None):
        self.id = None    # La BD asigna el ID al insertar
        self.titulo = titulo
        self.tipo = tipo  # PELICULA o SERIE
        self.anio = anio
        self.calificacion = calificacion  # Es opcional, puede quedar vacío
        self.estado = EstadoVisu.PENDIENTE  # Por defecto arranca como pendiente
        self.id_genero = id_genero
        self.id_director = id_director

    def marcar_visto(self):
        # Cambia el estado del título a VISTO
        self.estado = EstadoVisu.VISTO

    def marcar_pendiente(self):
        # Cambia el estado del título a PENDIENTE
        self.estado = EstadoVisu.PENDIENTE

    def asignar_calificacion(self, nota):
        # Solo guarda la nota si está entre 1 y 10
        if 1 <= nota <= 10:
            self.calificacion = nota

    def __str__(self):
        # Muestra el título en formato legible, con guión si no tiene calificación
        cal = self.calificacion if self.calificacion is not None else "-"
        return (f"[{self.id}] {self.titulo} ({self.anio}) | {self.tipo.value} | "
                f"Genero:{self.id_genero} Director:{self.id_director} | "
                f"Cal:{cal} | {self.estado.value}")

    def to_dict(self):
        # Convierte el objeto a diccionario para devolverlo como JSON en FastAPI
        # Los enums se exportan como texto plano con .value
        return {
            "id": self.id,
            "titulo": self.titulo,
            "tipo": self.tipo.value,
            "anio": self.anio,
            "calificacion": self.calificacion,
            "estado": self.estado.value,
            "id_genero": self.id_genero,
            "id_director": self.id_director
        }

    @classmethod
    def from_dict(cls, datos):
        # Reconstruye un objeto Titulo desde un diccionario
        # Los textos de tipo y estado se convierten de vuelta a enums
        t = cls(
            datos["titulo"],
            TipoContenido(datos["tipo"]),
            datos["anio"],
            datos["id_genero"],
            datos["id_director"],
            datos["calificacion"]
        )
        t.id = datos["id"]
        t.estado = EstadoVisu(datos["estado"])
        return t

