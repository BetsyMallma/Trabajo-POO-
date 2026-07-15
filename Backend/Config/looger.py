import datetime

class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._logs = []
        return cls._instancia

    def _registrar(self, nivel, mensaje):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        entrada = {"hora": hora, "nivel": nivel, "msg": mensaje}
        self._logs.append(entrada)

    def info(self, msg):    self._registrar("INFO",    msg)
    def warning(self, msg): self._registrar("WARNING", msg)
    def error(self, msg):   self._registrar("ERROR",   msg)
