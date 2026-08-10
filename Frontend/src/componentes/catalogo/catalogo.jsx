// Catálogo — muestra todos los títulos, películas o series según el modo.
// Recibe los datos desde App.jsx y solo se encarga de pintarlos.
import { Link } from "react-router-dom";
import { obtenerMeta } from "../../data/catalogoMeta";

// Opciones de orden que aparecen arriba del grid
const ETIQUETAS_ORDEN = [
  { valor: "recientes", texto: "Recientes" },
  { valor: "az", texto: "A–Z" },
  { valor: "top", texto: "Mejor calificados" },
];

// Cada modo tiene su propio título, subtítulo y etiquetas de stats
const TEXTOS_POR_MODO = {
  todos: {
    h1: "Catálogo de Títulos",
    sub: (s) => `${s.total} títulos registrados · ${s.generos} géneros · ${s.directores} directores`,
    labelTotal: "Total de títulos",
    labelVistos: "Vistos",
  },
  peliculas: {
    h1: "Películas",
    sub: (s) => `${s.total} películas registradas en el catálogo`,
    labelTotal: "Total de películas",
    labelVistos: "Vistas",
  },
  series: {
    h1: "Series",
    sub: (s) => `${s.total} series registradas en el catálogo`,
    labelTotal: "Total de series",
    labelVistos: "Vistas",
  },
};

function Catalogo({ modo = "todos", titulos, stats, orden, setOrden, onEliminar, cargando, error }) {
  const textos = TEXTOS_POR_MODO[modo] || TEXTOS_POR_MODO.todos;
  
  // Mientras la API responde
  if (cargando) {
    return (
      <div className="page-head">
        <div>
          <div className="eyebrow">Panel del administrador</div>
          <h1>Cargando catálogo…</h1>
          <div className="sub">Conectando con la API en {import.meta.env.VITE_API_URL || "http://localhost:8000"}</div>
        </div>
      </div>
    );
  }
  
  // Si el fetch falló, muestra qué salió mal
  if (error) {
    return (
      <div className="page-head">
        <div>
          <div className="eyebrow">Panel del administrador</div>
          <h1>No se pudo cargar el catálogo</h1>
          <div className="sub">
            {error} — revisa que el backend FastAPI esté corriendo (uvicorn main:app --reload) y que
            CORS permita este origen.
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Encabezado con título, subtítulo y botón para agregar */}
      <div className="page-head">
        <div>
          <div className="eyebrow">Panel del administrador</div>
          <h1>{textos.h1}</h1>
          <div className="sub">{textos.sub(stats)}</div>
        </div>
        <Link to="/registrar" className="btn btn-primary">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
            <path d="M12 5v14M5 12h14" />
          </svg>
          Registrar título
        </Link>
      </div>

      {/* Números rápidos: total, vistos, pendientes y promedio */}
      <div className="stat-strip">
        <div className="stat-cell">
          <div className="num">{stats.total}</div>
          <div className="lbl">{textos.labelTotal}</div>
        </div>
        <div className="stat-cell">
          <div className="num ok">{stats.vistos}</div>
          <div className="lbl">{textos.labelVistos}</div>
        </div>
        <div className="stat-cell">
          <div className="num accent">{stats.pendientes}</div>
          <div className="lbl">Pendientes</div>
        </div>
        <div className="stat-cell">
          <div className="num">{stats.promedio}</div>
          <div className="lbl">Calificación promedio</div>
        </div>
      </div>

      {/* Cantidad de resultados y botones para cambiar el orden */}
      <div className="grid-head">
        <div className="count">
          <b>{titulos.length}</b> resultados
        </div>
        <div className="sort-row">
          {ETIQUETAS_ORDEN.map((op) => (
            <span
              key={op.valor}
              className={orden === op.valor ? "on" : ""}
              onClick={() => setOrden(op.valor)}
            >
              {op.texto}
            </span>
          ))}
        </div>
      </div>

      {/* Grid de pósters — una card por título */}
      <div className="poster-grid">
        {titulos.map((t) => {
          const meta = obtenerMeta(t.titulo); // imagen y sinopsis del catálogo local
          return (
          <div className={`card g-${t.generoSlug}`} key={t.id} data-estado={t.estado.toLowerCase()}>
            <div className="poster-art">
              {meta.imagen ? (
                <img src={meta.imagen} alt={t.titulo} />
                      ) : null}
                      
              {/* Botones de editar y eliminar, aparecen al hacer hover */}
              <div className="card-actions">
                <Link
                  to={`/registrar?edit=1&id=${t.id}`}
                  className="action-btn edit"
                  title="Actualizar título"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 20h9" />
                    <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
                  </svg>
                </Link>
                <button
                  type="button"
                  className="action-btn delete"
                  title="Eliminar título"
                  onClick={() => onEliminar(t)}
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M3 6h18" />
                    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                    <line x1="10" y1="11" x2="10" y2="17" />
                    <line x1="14" y1="11" x2="14" y2="17" />
                  </svg>
                </button>
              </div>
              
              {/* Sinopsis que aparece al hacer hover sobre el póster */}
              <div className="sinopsis-overlay">
                <p>{meta.sinopsis}</p>
              </div>
              <span className="type-tag">{t.tipoEtiqueta}</span>
              
              {/* Etiqueta de visto/pendiente */}
              <div className={"status-tab " + t.estado.toLowerCase()}>
                {t.estado === "VISTO" ? "Visto" : "Pendiente"}
              </div>
              <div>
                <div className="ttitle">{t.titulo}</div>
                <div className="year">{t.anio}</div>
              </div>
            </div>
            
            {/* Pie de card: director y calificación */}
            <div className="card-foot">
              <span className="director">{t.directorCorto}</span>
              <span className={"rating" + (t.calificacion == null ? " empty" : "")}>
                <svg viewBox="0 0 24 24">
                  <path d="M12 2l3.1 6.5 7.1 1-5.1 5 1.2 7-6.3-3.5-6.3 3.5 1.2-7-5.1-5 7.1-1z" />
                </svg>
                {t.calificacion != null ? t.calificacion : "—"}
              </span>
            </div>
          </div>
          );
        })}
      </div>

      {/* Mensaje si ningún título pasa los filtros */}
      {titulos.length === 0 && (
        <p style={{ color: "var(--text-dim)", marginTop: "20px" }}>
          Ningún título coincide con los filtros seleccionados.
        </p>
      )}
    </>
  );
}

export default Catalogo;