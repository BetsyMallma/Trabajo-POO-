from pydantic import BaseModel, field_validator
from typing import Optional

from modelos.titulo import TipoContenido, EstadoVisu


# Lo que el cliente HTTP envía al CREAR un titulo (POST /titulos)
class TituloCrear(BaseModel):
    titulo: str
    tipo: TipoContenido
    anio: int
    id_genero: int
    id_director: int
    calificacion: Optional[float] = None  # es opcional porque un titulo puede crearse sin calificar todavia

    # valida que la calificacion, si viene, este en el rango permitido (1 a 10)
    @field_validator("calificacion")
    @classmethod
    def validar_calificacion(cls, valor):
        if valor is not None and not (1 <= valor <= 10):
            raise ValueError("La calificacion debe estar entre 1 y 10")
        return valor


# Lo que el cliente HTTP envía al ACTUALIZAR (PUT /titulos/{id})
# Solo titulo y anio son editables aquí; tipo/genero/director no cambian
# una vez creado el registro (igual que el DAO: TituloDAO.actualizar()
# solo recibe titulo y anio).
class TituloActualizar(BaseModel):
    titulo: Optional[str] = None
    anio: Optional[int] = None


# Body para PUT /titulos/{id}/calificacion
class CalificacionAsignar(BaseModel):
    nota: float

    # misma validacion que arriba, pero aca "nota" es obligatoria (no Optional)
    @field_validator("nota")
    @classmethod
    def validar_nota(cls, valor):
        if not (1 <= valor <= 10):
            raise ValueError("La calificacion debe estar entre 1 y 10")
        return valor


# Lo que la API devuelve (incluye el id y el estado, que el cliente no manda)
class TituloRespuesta(BaseModel):
    id: int
    titulo: str
    tipo: TipoContenido
    anio: int
    calificacion: Optional[float] = None
    estado: EstadoVisu
    id_genero: int
    id_director: int