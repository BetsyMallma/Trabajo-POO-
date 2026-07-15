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
