from fastapi import APIRouter, HTTPException

from dao.director_dao import (
    DirectorDAO,
    DirectorNoEncontradoError,
    DirectorDuplicadoError,
    DirectorConTitulosError,
)
from modelos.director import Director
from schemas.director_schema import DirectorCrear, DirectorActualizar, DirectorRespuesta

# --- Router que maneja los endpoints de directores ---
router = APIRouter(prefix="/directores", tags=["Directores"])
dao = DirectorDAO()  # Instancia del DAO para acceder a la BD

@router.get("/", response_model=list[DirectorRespuesta])
def listar_directores():
    # Devuelve todos los directores como lista de diccionarios
    return [d.to_dict() for d in dao.obtener_todos()]

@router.get("/{director_id}", response_model=DirectorRespuesta)
def obtener_director(director_id: int):
    # Buscamos el director, si no existe devolvemos error 404
    d = dao.buscar_por_id(director_id)
    if not d:
        raise HTTPException(status_code=404, detail=f"Director ID={director_id} no encontrado")
    return d.to_dict()

@router.post("/", response_model=DirectorRespuesta, status_code=201)
def crear_director(datos: DirectorCrear):
    # Creamos el director, si ya existe devolvemos error 400
    try:
        d = dao.insertar(Director(datos.nombre, datos.apellido, datos.nacionalidad))
        return d.to_dict()
    except DirectorDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    
@router.put("/{director_id}", response_model=DirectorRespuesta)
def actualizar_director(director_id: int, datos: DirectorActualizar):
    # Actualizamos el director, si no existe devolvemos error 404
    try:
        d = dao.actualizar(director_id, datos.nombre, datos.apellido, datos.nacionalidad)
        return d.to_dict()
    except DirectorNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    
@router.delete("/{director_id}")
def eliminar_director(director_id: int):
    # Eliminamos el director, si no existe es 404, si tiene títulos vinculados es 409
    try:
        dao.eliminar(director_id)
        return {"mensaje": f"Director ID={director_id} eliminado"}
    except DirectorNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except DirectorConTitulosError as ex:
        raise HTTPException(status_code=409, detail=str(ex))