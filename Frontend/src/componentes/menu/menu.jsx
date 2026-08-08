import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

function Menu({ conteos, filtros, generosDisponibles }) {
 const location = useLocation();
  const RUTAS_CON_FILTROS = ["/catalogo", "/peliculas", "/series"];
  const mostrarFiltros = RUTAS_CON_FILTROS.includes(location.pathname);

  // Usuario de la sesión (localStorage), igual que renderUserChip()
  // del script.js original. Se vuelve a leer cada vez que cambia de
  // ruta (por ejemplo al volver de /login hacia /catalogo), para que
  // el chip se actualice sin necesitar un refresh manual.
  const [sesion, setSesion] = useState(null);
  useEffect(() => {
    try {
      const guardado = JSON.parse(localStorage.getItem("sps_user"));
      setSesion(guardado);
    } catch {
      setSesion(null);
    }
  }, [location.pathname]);

  const inicial = sesion?.nombre ? sesion.nombre.trim().charAt(0).toUpperCase() : "?";
  const etiquetaUsuario = sesion?.nombre
    ? `${sesion.nombre} · ${sesion.rol || "Usuario"}`
    : "Iniciar sesión";

  return (
    <>
      {/* Topbar */}
      <header className="topbar">
        <label htmlFor="sidebar-toggle" className="menu-toggle">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </label>

        <Link to="/catalogo" className="brand">
          <span className="mark">SPS</span>
          <span className="full">Sistema de Películas y Series</span>
        </Link>

        {/* Buscador */}
        <div className="topbar-search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="7" />
            <path d="M21 21l-4.3-4.3" />
          </svg>
          <input
            type="text"
            placeholder="Buscar título, director, género…"
            value={filtros?.busqueda ?? ""}
            onChange={(e) => filtros?.setBusqueda(e.target.value)}
            style={{
              background: "transparent",
              border: "none",
              outline: "none",
              color: "inherit",
              font: "inherit",
              width: "100%",
            }}
          />
        </div>

        {/* Chip de usuario */}
        <div className="topbar-right">
          <Link to="/login" className="admin-chip" id="admin-chip">
            <div className="avatar">{inicial}</div>
            <span className="user-label">{etiquetaUsuario}</span>
          </Link>
        </div>
      </header>

      {/* Sidebar */}
      <aside className="sidebar">
        <div className="nav-group">
          <div className="nav-label">Catálogo</div>
          <Link
            to="/catalogo"
            className={"nav-item" + (location.pathname === "/catalogo" ? " active" : "")}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7" />
              <rect x="14" y="3" width="7" height="7" />
              <rect x="3" y="14" width="7" height="7" />
              <rect x="14" y="14" width="7" height="7" />
            </svg>
            Todos los títulos <span className="count">{conteos?.total ?? "—"}</span>
          </Link>
          <Link
            to="/peliculas"
            className={"nav-item" + (location.pathname === "/peliculas" ? " active" : "")}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13" />
              <path d="M22 2l-7 20-4-9-9-4 20-7z" />
            </svg>
            Películas <span className="count">{conteos?.peliculas ?? "—"}</span>
          </Link>
          <Link
            to="/series"
            className={"nav-item" + (location.pathname === "/series" ? " active" : "")}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="2" y="7" width="20" height="14" rx="2" />
              <path d="M17 2l-5 5-5-5" />
            </svg>
            Series <span className="count">{conteos?.series ?? "—"}</span>
          </Link>
        </div>

        {/* Filtros del catálogo */}
        {mostrarFiltros && filtros && (
          <div className="filter-block">
            <div className="nav-label">Filtros</div>

            <div className="filter-section">
              <h4>Estado</h4>
              <div className="chip-row" data-group="estado">
                {["todos", "visto", "pendiente"].map((valor) => (
                  <span
                    key={valor}
                    className={"chip" + (filtros.estado === valor ? " on" : "")}
                    onClick={() => filtros.setEstado(valor)}
                  >
                    {valor === "todos" ? "Todos" : valor === "visto" ? "Visto" : "Pendiente"}
                  </span>
                ))}
              </div>
            </div>

            <div className="filter-section">
              <h4>Género</h4>
              <div className="chip-row" data-group="genero">
                <span
                  className={"chip" + (filtros.genero === "todos" ? " on" : "")}
                  onClick={() => filtros.setGenero("todos")}
                >
                  Todos
                </span>
                {generosDisponibles?.map((g) => (
                  <span
                    key={g.slug}
                    className={"chip" + (filtros.genero === g.slug ? " on" : "")}
                    onClick={() => filtros.setGenero(g.slug)}
                  >
                    {g.nombre}
                  </span>
                ))}
              </div>
            </div>

            <div className="filter-section">
              <h4>Calificación mínima</h4>
              <div className="range-row">
                <input
                  type="range"
                  min="1"
                  max="10"
                  step="0.5"
                  value={filtros.minRating}
                  onChange={(e) => filtros.setMinRating(parseFloat(e.target.value))}
                />
                <span className="val">{filtros.minRating.toFixed(1)}</span>
              </div>
            </div>
          </div>
        )}
      </aside>

      {/* Overlay mobile */}
      <label htmlFor="sidebar-toggle" className="sidebar-overlay"></label>
    </>
  );
}

export default Menu;
