# ──────────────────────────────────────────────────────────────────────────────
# MODELO — Genero
# ──────────────────────────────────────────────────────────────────────────────
class Genero:
    def __init__(self, nombre, descripcion=None):
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return f"[{self.id}] {self.nombre} | {self.descripcion or '-'}"

    # Convierte el objeto a diccionario / lo reconstruye desde un diccionario.
    # to_dict() convierte el objeto en un diccionario simple para que los
    # routers de FastAPI puedan devolverlo como JSON (validado por el
    # schema GeneroRespuesta antes de salir).
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    @classmethod
    def from_dict(cls, datos):
        g = cls(datos["nombre"], datos["descripcion"])
        g.id = datos["id"]
        return g