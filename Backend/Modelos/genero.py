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
