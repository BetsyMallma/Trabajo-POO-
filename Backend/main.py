from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.base_datos import inicializar
from routers import generos, directores, titulos

# Creo la app principal de FastAPI, con los datos que aparecen en /docs
app = FastAPI(
    title="SPS - Sistema de Peliculas y Series",
    version="1.0",
    description="API REST para gestion de generos, directores y titulos (peliculas/series)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea las tablas en BD_SPS 
inicializar()

# Registra los endpoints de cada router.
app.include_router(generos.router)
app.include_router(directores.router)
app.include_router(titulos.router)


# Endpoint raiz - GET / - sirve como "health check" de la API.
@app.get("/")
def inicio():
    return {
        "mensaje": "API SPS - Sistema de Peliculas y Series",
        "version": "1.0",
        "docs": "/docs"  
    }