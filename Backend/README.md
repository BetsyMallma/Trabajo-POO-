# SPS - Backend (FastAPI + PostgreSQL)

API REST para gestión de géneros, directores y títulos (películas/series).

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL 18 (o compatible)
- pip

## Estructura del proyecto

```
Backend/
├── config/       # Configuración y conexión a la base de datos
├── dao/          # Data Access Objects (acceso a la base de datos)
├── modelos/      # Modelos de datos
├── routers/      # Endpoints agrupados por recurso (generos, directores, titulos)
├── schemas/      # Validación de datos de entrada/salida (Pydantic)
├── .env          # Variables de entorno (no compartir públicamente)
├── main.py       # Punto de entrada de la aplicación
└── SPS_postgres.sql  # Script de creación de la base de datos
```

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/BetsyMallma/Trabajo-POO-.git
   cd Trabajo-POO-/Backend
   ```

2. Instalar dependencias:
   ```bash
   pip install fastapi uvicorn psycopg2-binary python-multipart
   ```

## Configuración de la base de datos

1. Crear la base de datos en PostgreSQL con el mismo nombre configurado en `.env`.
2. Ejecutar el script `SPS_postgres.sql` para crear las tablas necesarias.

## Variables de entorno

El archivo `.env` debe contener:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nombre_de_tu_bd
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
LC_MESSAGES=C
```

En PowerShell (Windows), estas variables se cargan manualmente antes de correr el servidor:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="nombre_de_tu_bd"
$env:DB_USER="tu_usuario"
$env:DB_PASSWORD="tu_contraseña"
$env:LC_MESSAGES="C"
```

## Cómo levantar el servidor

```powershell
python -m uvicorn main:app --reload
```

El servidor corre por defecto en:

```
http://localhost:8000
```

## Documentación de la API (Swagger)

Una vez levantado el servidor, la documentación interactiva está disponible en:

```
http://localhost:8000/docs
```

## Endpoints disponibles

15 endpoints distribuidos en 3 routers:

- **Generos** (`/generos/`) — GET, POST, GET por ID, PUT, DELETE
- **Directores** (`/directores/`) — GET, POST, GET por ID, PUT, DELETE
- **Titulos** (`/titulos/`) — GET, POST, GET por ID, PUT, DELETE, PUT visto, PUT pendiente, PUT calificación
