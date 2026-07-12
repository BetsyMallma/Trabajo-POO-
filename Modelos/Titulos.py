import enum


class EstadoVisu(str, enum.Enum):
    VISTO = "VISTO"
    PENDIENTE = "PENDIENTE"


class Titulo:
    def __init__(self, titulo, tipo, anio, id_genero, id_director, calificacion=None):
        self.id = None
        self.titulo = titulo
        self.tipo = tipo
        self.anio = anio
        self.calificacion = calificacion
        self.estado = EstadoVisu.PENDIENTE
        self.id_genero = id_genero
        self.id_director = id_director

    def marcar_visto(self):
        self.estado = EstadoVisu.VISTO

    def marcar_pendiente(self):
        self.estado = EstadoVisu.PENDIENTE

    def asignar_calificacion(self, nota):
        if 1 <= nota <= 10:
            self.calificacion = nota

    def __str__(self):
        cal = self.calificacion if self.calificacion is not None else "-"
        return (f"[{self.id}] {self.titulo} ({self.anio}) | {self.tipo.value} | "
                f"Genero:{self.id_genero} Director:{self.id_director} | "
                f"Cal:{cal} | {self.estado.value}")