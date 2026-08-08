from pydantic import BaseModel
from typing import Optional

#=================================================================
#  Schemas que validan los datos que entran y salen por la API
#=================================================================

# Lo que se recibe al crear un director (nombre y apellido obligatorios)
class DirectorCrear(BaseModel):
    nombre: str
    apellido: str
    nacionalidad: Optional[str] = None  # Es opcional, puede no venir
    
# Lo que se recibe al actualizar (todos los campos son opcionales)
class DirectorActualizar(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    nacionalidad: Optional[str] = None
    
# Lo que se devuelve como respuesta (incluye el ID que generó la BD)
class DirectorRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    nacionalidad: Optional[str] = None