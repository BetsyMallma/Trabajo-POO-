from fastapi import APIRouter, HTTPException

from dao.genero_dao import (
    GeneroDAO,
    GeneroNoEncontradoError,
    GeneroDuplicadoError,
    GeneroConTitulosError,
)
from modelos.genero import Genero
from schemas.genero_schema import GeneroCrear, GeneroActualizar, GeneroRespuesta

# --- Router que maneja los endpoints de géneros ---
router = APIRouter(prefix="/generos", tags=["Generos"])
dao = GeneroDAO()  # Instancia del DAO para acceder a la BD

@router.get("/", response_model=list[GeneroRespuesta])
def listar_generos():
    # Devuelve todos los géneros como lista de diccionarios
    return [g.to_dict() for g in dao.obtener_todos()]

@router.get("/{genero_id}", response_model=GeneroRespuesta)
def obtener_genero(genero_id: int):
    # Buscamos el género, si no existe devolvemos error 404
    g = dao.buscar_por_id(genero_id)
    if not g:
        raise HTTPException(status_code=404, detail=f"Genero ID={genero_id} no encontrado")
    return g.to_dict()

@router.post("/", response_model=GeneroRespuesta, status_code=201)
def crear_genero(datos: GeneroCrear):
    # Creamos el género, si ya existe devolvemos error 400
    try:
        g = dao.insertar(Genero(datos.nombre, datos.descripcion))
        return g.to_dict()
    except GeneroDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    
@router.put("/{genero_id}", response_model=GeneroRespuesta)
def actualizar_genero(genero_id: int, datos: GeneroActualizar):
    # Actualizamos el género, si no existe devolvemos error 404
    try:
        g = dao.actualizar(genero_id, datos.nombre, datos.descripcion)
        return g.to_dict()
    except GeneroNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    
@router.delete("/{genero_id}")
def eliminar_genero(genero_id: int):
    # Eliminamos el género, si no existe es 404, si tiene títulos vinculados es 409
    try:
        dao.eliminar(genero_id)
        return {"mensaje": f"Genero ID={genero_id} eliminado"}
    except GeneroNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except GeneroConTitulosError as ex:
        raise HTTPException(status_code=409, detail=str(ex))