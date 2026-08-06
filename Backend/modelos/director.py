# ──────────────────────────────────────────────────────────────────────────────
# MODELO — Director
# ──────────────────────────────────────────────────────────────────────────────
class Director:
    def __init__(self, nombre, apellido, nacionalidad=None):
        self.id = None   # La BD asigna el ID al insertar
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad

    def __str__(self):
        # Muestra el director en formato legible, con guión si no tiene nacionalidad
        return f"[{self.id}] {self.nombre} {self.apellido} | {self.nacionalidad or '-'}"

    # Convierte el objeto a diccionario / lo reconstruye desde un diccionario.
    def to_dict(self):
        # Convierte el objeto a diccionario, útil para enviarlo como JSON o guardarlo
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nacionalidad": self.nacionalidad
        }

    @classmethod
    def from_dict(cls, datos):
        # Reconstruye un objeto Director desde un diccionario
        d = cls(datos["nombre"], datos["apellido"], datos["nacionalidad"])
        d.id = datos["id"]
        return d
