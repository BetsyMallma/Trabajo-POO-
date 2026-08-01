# ──────────────────────────────────────────────────────────────────────────────
# MODELO — Director
# ──────────────────────────────────────────────────────────────────────────────
class Director:
    def __init__(self, nombre, apellido, nacionalidad=None):
        self.id = None
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad

    def __str__(self):
        return f"[{self.id}] {self.nombre} {self.apellido} | {self.nacionalidad or '-'}"

    # Convierte el objeto a diccionario / lo reconstruye desde un diccionario.
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nacionalidad": self.nacionalidad
        }

    @classmethod
    def from_dict(cls, datos):
        d = cls(datos["nombre"], datos["apellido"], datos["nacionalidad"])
        d.id = datos["id"]
        return d
