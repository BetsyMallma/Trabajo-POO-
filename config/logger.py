import datetime

class Logger:
    # Variable de CLASE (no de objeto): vive en la clase y la comparten todos.
    # Guarda la única instancia que existirá. Empieza en None = todavía no hay ninguna.
    _instancia = None

    def __new__(cls):
        # __new__ se ejecuta ANTES que __init__ y es quien realmente crea el objeto.
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Crear la lista de logs dentro del if para que se cree UNA sola vez.
            cls._instancia._logs = []
        # Siempre devuelve la misma instancia.
        return cls._instancia

    def _registrar(self, nivel, mensaje):
        # Método privado (guión bajo = convención "uso interno").
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        entrada = {"hora": hora, "nivel": nivel, "msg": mensaje}
        self._logs.append(entrada)

    def info(self, msg):    self._registrar("INFO",    msg)
    def warning(self, msg): self._registrar("WARNING", msg)
    def error(self, msg):   self._registrar("ERROR",   msg)

    def mostrar_logs(self):
        print(f"\n=== HISTORIAL DEL SISTEMA ({len(self._logs)} eventos) ===")
        for log in self._logs:
            print(f"  [{log['hora']}] {log['nivel']:7} | {log['msg']}")

    def limpiar(self):
        self._logs.clear()
        print("  OK Historial de logs limpiado")