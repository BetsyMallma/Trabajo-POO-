from Backend.Config.looger import Logger

class SistemaConfig:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre  = "SPS - Sistema de Peliculas y Series"
            cls._inst.version = "1.0"
            cls._inst.empresa = "Proyecto Academico SPS"
            cls._inst.autor   = "Betsy"
