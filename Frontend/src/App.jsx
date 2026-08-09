// Aca estoy haciendo importaciones
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import "./App.css";

import Menu from "./componentes/menu/menu";
import Catalogo from "./componentes/catalogo/catalogo";
import Login from "./componentes/login/login";
import Registrar from "./componentes/registrar/registrar";

import { listarTitulos, eliminarTitulo } from "./api/titulosApi";
import { listarGeneros } from "./api/generosApi";
import { listarDirectores } from "./api/directoresApi";
import { slugGenero, nombreCortoDirector, etiquetaTipo } from "./data/catalogoHelpers";

//================================================
// Aca estoy mapeando la ruta actual al "tipo" de la BD que le corresponde.
// null = sin filtrar por tipo (catálogo completo).
//================================================
function tipoSegunRuta(pathname) {
  if (pathname === "/peliculas") return "PELICULA";
  if (pathname === "/series") return "SERIE";
  return null;
}

function App() {
  const location = useLocation();
  const tipoScope = tipoSegunRuta(location.pathname);

  // ---------- datos crudos de la API ----------
  const [titulos, setTitulos] = useState([]);
  const [generos, setGeneros] = useState([]);
  const [directores, setDirectores] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  // ---------- estado de filtros / orden (vive aquí porque tanto el
  // Menu -sidebar de filtros- como el Catalogo -grid- lo necesitan) ----------
  const [estado, setEstado] = useState("todos");
  const [genero, setGenero] = useState("todos");
  const [minRating, setMinRating] = useState(1);
  const [busqueda, setBusqueda] = useState("");
  const [orden, setOrden] = useState("recientes");

  function cargarDatos() {
    setCargando(true);
    setError(null);
    Promise.all([listarTitulos(), listarGeneros(), listarDirectores()])
      .then(([t, g, d]) => {
        setTitulos(t);
        setGeneros(g);
        setDirectores(d);
      })
      .catch((err) => {
        setError(err?.message || "Error de conexión con la API");
      })
      .finally(() => setCargando(false));
  }

  useEffect(() => {
    cargarDatos();
  }, []);

  // combinar titulo + genero + director + metadata visual
  const titulosEnriquecidos = useMemo(() => {
    const mapaGeneros = Object.fromEntries(generos.map((g) => [g.id, g]));
    const mapaDirectores = Object.fromEntries(directores.map((d) => [d.id, d]));

    return titulos.map((t) => {
      const g = mapaGeneros[t.id_genero];
      const d = mapaDirectores[t.id_director];
      return {
        ...t,
        generoNombre: g?.nombre || "—",
        generoSlug: g ? slugGenero(g.nombre) : "otro",
        directorCorto: nombreCortoDirector(d),
        tipoEtiqueta: etiquetaTipo(t.tipo),
        // OJO: meta (imagen/sinopsis) NO se calcula aquí a propósito.
        // Vive en localStorage y puede cambiar sin que la API cambie
        // (por ejemplo al editar solo la imagen), así que Catalogo la
        // lee directo con obtenerMeta() en cada render en vez de
        // quedar guardada en este useMemo — si no, se queda "vieja".
      };
    });
  }, [titulos, generos, directores]);

  // Subconjunto de la página actual: todo (/catalogo) o solo
  // PELICULA/SERIE (/peliculas, /series) — igual que index.html vs
  // peliculas.html/series.html en el diseño original.
  const titulosDelScope = useMemo(() => {
    if (!tipoScope) return titulosEnriquecidos;
    return titulosEnriquecidos.filter((t) => t.tipo === tipoScope);
  }, [titulosEnriquecidos, tipoScope]);

  // géneros realmente usados en ESTE subconjunto, para los chips del sidebar
  const generosDisponibles = useMemo(() => {
    const vistos = new Map();
    titulosDelScope.forEach((t) => {
      if (!vistos.has(t.generoSlug)) vistos.set(t.generoSlug, t.generoNombre);
    });
    return Array.from(vistos, ([slug, nombre]) => ({ slug, nombre }));
  }, [titulosDelScope]);

  // ---------- filtrar + ordenar (misma lógica que applyFilters() del script.js original) ----------
  const titulosFiltrados = useMemo(() => {
    let lista = titulosDelScope.filter((t) => {
      const okEstado = estado === "todos" || t.estado.toLowerCase() === estado;
      const okGenero = genero === "todos" || t.generoSlug === genero;
      const okRating = t.calificacion == null ? true : t.calificacion >= minRating;
      const okBusqueda =
        busqueda.trim() === "" || t.titulo.toLowerCase().includes(busqueda.toLowerCase());
      return okEstado && okGenero && okRating && okBusqueda;
    });

    if (orden === "az") {
      lista = [...lista].sort((a, b) => a.titulo.localeCompare(b.titulo));
    } else if (orden === "top") {
      lista = [...lista].sort((a, b) => (b.calificacion ?? -1) - (a.calificacion ?? -1));
    }
    // "recientes" conserva el orden que entrega la API (por id)

    return lista;
  }, [titulosDelScope, estado, genero, minRating, busqueda, orden]);

  // ---------- stats para el stat-strip ----------
  // Nota: igual que en el diseño original, el stat-strip refleja el
  // subconjunto de la página (todos/películas/series) pero NO se ve
  // afectado por los chips de filtro (estado/género/rating) — solo
  // por búsqueda/orden que no cambian totales, y por altas/bajas reales.
  const stats = useMemo(() => {
    const total = titulosDelScope.length;
    const vistos = titulosDelScope.filter((t) => t.estado === "VISTO").length;
    const conCalificacion = titulosDelScope.filter((t) => t.calificacion != null);
    const promedio = conCalificacion.length
      ? (conCalificacion.reduce((s, t) => s + t.calificacion, 0) / conCalificacion.length).toFixed(1)
      : "—";
    return {
      total,
      vistos,
      pendientes: total - vistos,
      promedio,
      generos: generos.length,
      directores: directores.length,
    };
  }, [titulosDelScope, generos, directores]);

  const conteos = useMemo(
    () => ({
      total: titulosEnriquecidos.length,
      peliculas: titulosEnriquecidos.filter((t) => t.tipo === "PELICULA").length,
      series: titulosEnriquecidos.filter((t) => t.tipo === "SERIE").length,
    }),
    [titulosEnriquecidos]
  );

  // ---------- acciones ----------
  function handleEliminar(t) {
    const ok = window.confirm(`¿Eliminar "${t.titulo}" del catálogo? Esta acción no se puede deshacer.`);
    if (!ok) return;
    eliminarTitulo(t.id)
      .then(() => cargarDatos())
      .catch((err) => alert("No se pudo eliminar: " + (err?.response?.data?.detail || err.message)));
  }

  const filtros = { estado, setEstado, genero, setGenero, minRating, setMinRating, busqueda, setBusqueda };

  return (
    <>
      <input type="checkbox" id="sidebar-toggle" />
      <div className="shell">
        <Menu conteos={conteos} filtros={filtros} generosDisponibles={generosDisponibles} />

        <main className="main">
          <Routes>
            <Route path="/" element={<Navigate to="/catalogo" replace />} />
            <Route
              path="/catalogo"
              element={
                <Catalogo
                  modo="todos"
                  titulos={titulosFiltrados}
                  stats={stats}
                  orden={orden}
                  setOrden={setOrden}
                  onEliminar={handleEliminar}
                  cargando={cargando}
                  error={error}
                />
              }
            />
            <Route
              path="/peliculas"
              element={
                <Catalogo
                  modo="peliculas"
                  titulos={titulosFiltrados}
                  stats={stats}
                  orden={orden}
                  setOrden={setOrden}
                  onEliminar={handleEliminar}
                  cargando={cargando}
                  error={error}
                />
              }
            />
            <Route
              path="/series"
              element={
                <Catalogo
                  modo="series"
                  titulos={titulosFiltrados}
                  stats={stats}
                  orden={orden}
                  setOrden={setOrden}
                  onEliminar={handleEliminar}
                  cargando={cargando}
                  error={error}
                />
              }
            />
            <Route path="/login" element={<Login />} />
            <Route path="/registrar" element={<Registrar />} />
          </Routes>
        </main>
      </div>
    </>
  );
}
export default App;