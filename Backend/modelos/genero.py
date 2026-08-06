# ──────────────────────────────────────────────────────────────────────────────
# MODELO — Genero
# ──────────────────────────────────────────────────────────────────────────────
class Genero:
    def __init__(self, nombre, descripcion=None):
        self.id = None  # La BD asigna el ID al insertar
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        # Muestra el género en formato legible, con guión si no tiene descripción
        return f"[{self.id}] {self.nombre} | {self.descripcion or '-'}"

    # to_dict() convierte el objeto en un diccionario simple para que los
    # routers de FastAPI puedan devolverlo como JSON (validado por el
    # schema GeneroRespuesta antes de salir).
    def to_dict(self):
        # Convierte el objeto a diccionario para devolverlo como JSON en FastAPI
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }

    @classmethod
    def from_dict(cls, datos):
        # Reconstruye un objeto Genero desde un diccionario
        g = cls(datos["nombre"], datos["descripcion"])
        g.id = datos["id"]
        return g