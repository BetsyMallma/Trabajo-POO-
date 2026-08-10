# SPS - Frontend (React + Vite)

Interfaz web del Sistema de Películas y Series (SPS), con tema oscuro tipo cine y acentos en color ámbar.

## Requisitos previos

- Node.js LTS
- npm

## Estructura del proyecto

```
Frontend/
├── src/
│   ├── api/           # Configuración de Axios (axiosClient.js)
│   ├── componentes/    # Componentes de React
│   ├── data/           # catalogoMeta.js (sinopsis e imágenes)
│   ├── App.jsx
│   └── main.jsx
├── .env                # Variables de entorno (URL del backend)
├── package.json
└── vite.config.js
```

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/BetsyMallma/Trabajo-POO-.git
   cd Trabajo-POO-/Frontend
   ```

2. Instalar dependencias:
   ```bash
   npm install
   ```

## Variables de entorno

Crear un archivo `.env` en la raíz del Frontend con:

```dotenv
# Copia este archivo a .env y ajusta si tu API corre en otro puerto/host
VITE_API_URL=http://localhost:8000
```

**Importante:** el backend debe estar corriendo antes de iniciar el frontend, ya que la aplicación consume la API en `VITE_API_URL`.

## Cómo levantar la aplicación

```bash
npm run dev
```

La aplicación estará disponible por defecto en:

```
http://localhost:5173
```

## Tecnologías principales

- React + Vite
- react-router-dom (enrutamiento sin recarga de página)
- Axios (cliente HTTP centralizado en `axiosClient.js`)
- localStorage (para overrides de metadata del catálogo)

## Notas de diseño

- Las sinopsis e imágenes de películas/series no se obtienen de la base de datos, sino de un archivo estático (`catalogoMeta.js`), con posibilidad de ajustes guardados en `localStorage` mediante `guardarMetaOverride()`.
