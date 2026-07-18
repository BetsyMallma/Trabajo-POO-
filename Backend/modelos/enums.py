import enum

class TipoContenido(str, enum.Enum):
    PELICULA = "PELICULA"
    SERIE = "SERIE"

class EstadoVisu(str, enum.Enum):
    VISTO = "VISTO"
    PENDIENTE = "PENDIENTE"
