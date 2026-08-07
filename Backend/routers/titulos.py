from fastapi import APIRouter, HTTPException

from dao.genero_dao import GeneroDAO, GeneroNoEncontradoError
from dao.director_dao import DirectorDAO, DirectorNoEncontradoError
from dao.titulo_dao import (
    TituloDAO,
    TituloNoEncontradoError,
    TituloDuplicadoError,
    AnioInvalidoError,
    CalificacionInvalidaError,
)
from modelos.titulo import Titulo
from schemas.titulo_schema import (
    TituloCrear,
    TituloActualizar,
    TituloRespuesta,
    CalificacionAsignar,
)

# Creo el router para agrupar todas las rutas de "titulos" bajo el mismo prefijo
router = APIRouter(prefix="/titulos", tags=["Titulos"])

# TituloDAO necesita GeneroDAO y DirectorDAO para validar las FK antes de
# insertar/actualizar (misma composicion que en main.py del menu de terminal).
gdao = GeneroDAO()
ddao = DirectorDAO()
dao = TituloDAO(gdao, ddao)


# GET /titulos/ -> devuelve la lista completa de titulos
@router.get("/", response_model=list[TituloRespuesta])
def listar_titulos():
    return [t.to_dict() for t in dao.obtener_todos()]


# GET /titulos/{id} -> busca un titulo puntual por su id
@router.get("/{titulo_id}", response_model=TituloRespuesta)
def obtener_titulo(titulo_id: int):
    t = dao.buscar_por_id(titulo_id)
    if not t:
        # si no existe, respondo con error 404 (no encontrado)
        raise HTTPException(status_code=404, detail=f"Titulo ID={titulo_id} no encontrado")
    return t.to_dict()


# POST /titulos/ -> crea un titulo nuevo
@router.post("/", response_model=TituloRespuesta, status_code=201)
def crear_titulo(datos: TituloCrear):
    try:
        t = dao.insertar(Titulo(
            datos.titulo,
            datos.tipo,
            datos.anio,
            datos.id_genero,
            datos.id_director,
            datos.calificacion,
        ))
        return t.to_dict()
    # atrapo cada error posible del DAO y lo transformo en un HTTPException
    # con el codigo de estado que corresponda
    except GeneroNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except DirectorNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except AnioInvalidoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except TituloDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


# PUT /titulos/{id} -> actualiza titulo y/o anio de un titulo existente
@router.put("/{titulo_id}", response_model=TituloRespuesta)
def actualizar_titulo(titulo_id: int, datos: TituloActualizar):
    try:
        t = dao.actualizar(titulo_id, datos.titulo, datos.anio)
        return t.to_dict()
    except TituloNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except AnioInvalidoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


# DELETE /titulos/{id} -> elimina un titulo
@router.delete("/{titulo_id}")
def eliminar_titulo(titulo_id: int):
    try:
        dao.eliminar(titulo_id)
        return {"mensaje": f"Titulo ID={titulo_id} eliminado"}
    except TituloNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


# PUT /titulos/{id}/visto — marca un titulo como VISTO.
@router.put("/{titulo_id}/visto", response_model=TituloRespuesta)
def marcar_visto(titulo_id: int):
    try:
        t = dao.marcar_visto(titulo_id)
        return t.to_dict()
    except TituloNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


# PUT /titulos/{id}/pendiente -> vuelve a marcar el titulo como PENDIENTE
@router.put("/{titulo_id}/pendiente", response_model=TituloRespuesta)
def marcar_pendiente(titulo_id: int):
    try:
        t = dao.marcar_pendiente(titulo_id)
        return t.to_dict()
    except TituloNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


# PUT /titulos/{id}/calificacion -> asigna una nota/calificacion al titulo
@router.put("/{titulo_id}/calificacion", response_model=TituloRespuesta)
def calificar_titulo(titulo_id: int, datos: CalificacionAsignar):
    try:
        t = dao.calificar(titulo_id, datos.nota)
        return t.to_dict()
    except TituloNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except CalificacionInvalidaError as ex:
        raise HTTPException(status_code=400, detail=str(ex))