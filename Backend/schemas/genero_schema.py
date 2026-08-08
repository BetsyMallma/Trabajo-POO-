from pydantic import BaseModel
from typing import Optional

# Lo que el cliente HTTP envía al CREAR un genero (POST /generos)
class GeneroCrear(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

# Lo que el cliente HTTP envía al ACTUALIZAR (PUT /generos/{id})
# Todos opcionales: se puede mandar solo el campo que se quiere cambiar.
class GeneroActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

# Lo que la API devuelve (incluye siempre el id, generado por la BD)
class GeneroRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
