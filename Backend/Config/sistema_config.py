from Backend.config.logger import Logger

class SistemaConfig:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre  = "SPS - Sistema de Peliculas y Series"
            cls._inst.version = "1.0"
            cls._inst.empresa = "Proyecto Academico SPS"
            cls._inst.autor   = "Betsy"
            Logger().info(
                f"Sistema Iniciado: {cls._inst.nombre} "
                f"Version: {cls._inst.version} "
                f"Empresa: {cls._inst.empresa} "
                f"Autor: {cls._inst.autor}"
            )
        return cls._inst
