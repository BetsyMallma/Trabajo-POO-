# ──────────────────────────────────────────────────────────────────────────────
# MODELO — Titulo
# ──────────────────────────────────────────────────────────────────────────────
from modelos.enums import TipoContenido, EstadoVisu


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

    def to_dict(self):
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

