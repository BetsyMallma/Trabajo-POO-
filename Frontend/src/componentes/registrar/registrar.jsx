// Registrar: sirve para crear una película o serie nueva, o para editar una que ya existe.
//el formulario permite registrar películas/series y editar algunos de sus datos,
// pero no todos los campos se pueden modificar.

import { useEffect, useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";

import {
  crearTitulo,
  actualizarTitulo,
  obtenerTitulo,
  marcarVisto,
  marcarPendiente,
  calificarTitulo,
} from "../../api/titulosApi";
import { listarGeneros } from "../../api/generosApi";
import { listarDirectores, crearDirector } from "../../api/directoresApi";
import { obtenerMeta, guardarMetaOverride } from "../../data/catalogoMeta";

const FORM_VACIO = {
  titulo: "",
  tipo: "",
  id_genero: "",
  id_director: "",
  anio: "",
  calificacion: "",
  estado: "PENDIENTE",
  sinopsis: "",
  imagen: null,
};

function Registrar() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const esEdicion = params.get("edit") === "1";
  const idEditado = params.get("id");

  const [generos, setGeneros] = useState([]);
  const [directores, setDirectores] = useState([]);
  const [cargandoListas, setCargandoListas] = useState(true);
  const [cargandoTitulo, setCargandoTitulo] = useState(esEdicion);
  const [guardando, setGuardando] = useState(false);
  const [errorCarga, setErrorCarga] = useState(null);

  const [form, setForm] = useState(FORM_VACIO);
  const [original, setOriginal] = useState(null); // para saber qué cambió, en edición

  const [mostrarNuevoDirector, setMostrarNuevoDirector] = useState(false);
  const [nuevoDirector, setNuevoDirector] = useState({ nombre: "", apellido: "", nacionalidad: "" });

  // ---------- cargar listas de géneros/directores ----------
  useEffect(() => {
    Promise.all([listarGeneros(), listarDirectores()])
      .then(([g, d]) => {
        setGeneros(g);
        setDirectores(d);
      })
      .catch((err) => setErrorCarga(err?.message || "No se pudo conectar con la API"))
      .finally(() => setCargandoListas(false));
  }, []);

  // ---------- si es edición, cargar el título a editar ----------
  useEffect(() => {
    if (!esEdicion || !idEditado) return;
    obtenerTitulo(idEditado)
      .then((t) => {
        const meta = obtenerMeta(t.titulo);
        const datos = {
          titulo: t.titulo,
          tipo: t.tipo,
          id_genero: String(t.id_genero),
          id_director: String(t.id_director),
          anio: String(t.anio),
          calificacion: t.calificacion != null ? String(t.calificacion) : "",
          estado: t.estado,
          sinopsis: meta.sinopsis === "Sinopsis no disponible todavía para este título." ? "" : meta.sinopsis,
          imagen: meta.imagen,
        };
        setForm(datos);
        setOriginal({ ...datos, id: t.id });
      })
      .catch((err) => setErrorCarga(err?.response?.data?.detail || err.message))
      .finally(() => setCargandoTitulo(false));
  }, [esEdicion, idEditado]);

  function actualizarCampo(campo, valor) {
    setForm((f) => ({ ...f, [campo]: valor }));
  }

  function manejarImagen(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => actualizarCampo("imagen", ev.target.result);
    reader.readAsDataURL(file);
  }

  function crearDirectorInline() {
    if (!nuevoDirector.nombre.trim() || !nuevoDirector.apellido.trim()) {
      alert("Completa al menos nombre y apellido del director.");
      return;
    }
    crearDirector(nuevoDirector)
      .then((d) => {
        setDirectores((lista) => [...lista, d]);
        actualizarCampo("id_director", String(d.id));
        setMostrarNuevoDirector(false);
        setNuevoDirector({ nombre: "", apellido: "", nacionalidad: "" });
      })
      .catch((err) => alert("No se pudo crear el director: " + (err?.response?.data?.detail || err.message)));
  }

  async function manejarSubmit(e) {
    e.preventDefault();
    if (!form.titulo.trim() || !form.tipo || !form.id_genero || !form.id_director || !form.anio) {
      alert("Completa título, tipo, género, director y año — son obligatorios.");
      return;
    }

    setGuardando(true);
    try {
      if (esEdicion) {
        // 1) título / año (único PUT que soporta el backend)
        if (form.titulo !== original.titulo || form.anio !== original.anio) {
          await actualizarTitulo(idEditado, { titulo: form.titulo, anio: Number(form.anio) });
        }
        // 2) estado, si cambió
        if (form.estado !== original.estado) {
          if (form.estado === "VISTO") await marcarVisto(idEditado);
          else await marcarPendiente(idEditado);
        }
        // 3) calificación, si cambió
        if (form.calificacion !== original.calificacion && form.calificacion !== "") {
          await calificarTitulo(idEditado, Number(form.calificacion));
        }
        // 4) sinopsis / imagen (solo local, el backend no las guarda)
        guardarMetaOverride(form.titulo, { sinopsis: form.sinopsis, imagen: form.imagen });
      } else {
        const creado = await crearTitulo({
          titulo: form.titulo,
          tipo: form.tipo,
          anio: Number(form.anio),
          id_genero: Number(form.id_genero),
          id_director: Number(form.id_director),
          calificacion: form.calificacion !== "" ? Number(form.calificacion) : null,
        });
        if (form.estado === "VISTO") {
          await marcarVisto(creado.id);
        }
        guardarMetaOverride(form.titulo, { sinopsis: form.sinopsis, imagen: form.imagen });
      }
      navigate("/catalogo");
    } catch (err) {
      alert("No se pudo guardar: " + (err?.response?.data?.detail || err.message));
    } finally {
      setGuardando(false);
    }
  }

  if (cargandoListas || cargandoTitulo) {
    return (
      <div className="auth-shell">
        <div className="auth-card">
          <div className="auth-head">
            <span className="mark">SPS</span>
            <h1>Cargando…</h1>
          </div>
        </div>
      </div>
    );
  }

  if (errorCarga) {
    return (
      <div className="auth-shell">
        <div className="auth-card">
          <div className="auth-head">
            <span className="mark">SPS</span>
            <h1>No se pudo cargar</h1>
            <p>{errorCarga}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-shell">
      <Link to="/catalogo" className="auth-back">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M19 12H5" />
          <path d="M12 19l-7-7 7-7" />
        </svg>
        Volver al catálogo
      </Link>

      <div className="auth-card">
        <div className="auth-head">
          <span className="mark">SPS</span>
          <h1>{esEdicion ? "Actualizar título" : "Registrar título"}</h1>
          <p>
            {esEdicion
              ? `Modifica los datos de "${original?.titulo}" y guarda los cambios`
              : "Completa los datos para añadir una película o serie al catálogo"}
          </p>
        </div>

        <form onSubmit={manejarSubmit}>
          <div className="field">
            <label htmlFor="titulo">Título</label>
            <input
              type="text"
              id="titulo"
              placeholder="Ej. Interstellar"
              value={form.titulo}
              onChange={(e) => actualizarCampo("titulo", e.target.value)}
              required
            />
          </div>

          <div className="field-row">
            <div className="field">
              <label htmlFor="tipo">Tipo</label>
              <select
                id="tipo"
                value={form.tipo}
                onChange={(e) => actualizarCampo("tipo", e.target.value)}
                disabled={esEdicion}
                required
              >
                <option value="" disabled>
                  Selecciona…
                </option>
                <option value="PELICULA">Película</option>
                <option value="SERIE">Serie</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="genero">Género</label>
              <select
                id="genero"
                value={form.id_genero}
                onChange={(e) => actualizarCampo("id_genero", e.target.value)}
                disabled={esEdicion}
                required
              >
                <option value="" disabled>
                  Selecciona…
                </option>
                {generos.map((g) => (
                  <option key={g.id} value={g.id}>
                    {g.nombre}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="field-row">
            <div className="field">
              <label htmlFor="director">Director</label>
              <select
                id="director"
                value={form.id_director}
                onChange={(e) => actualizarCampo("id_director", e.target.value)}
                disabled={esEdicion}
                required
              >
                <option value="" disabled>
                  Selecciona…
                </option>
                {directores.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.nombre} {d.apellido}
                  </option>
                ))}
              </select>
              {!esEdicion && !mostrarNuevoDirector && (
                <span
                  onClick={() => setMostrarNuevoDirector(true)}
                  style={{ fontSize: "12px", color: "var(--amber)", cursor: "pointer", marginTop: "6px", display: "inline-block" }}
                >
                  + Nuevo director
                </span>
              )}
              {mostrarNuevoDirector && (
                <div style={{ marginTop: "8px", display: "grid", gap: "6px" }}>
                  <input
                    type="text"
                    placeholder="Nombre"
                    value={nuevoDirector.nombre}
                    onChange={(e) => setNuevoDirector((n) => ({ ...n, nombre: e.target.value }))}
                  />
                  <input
                    type="text"
                    placeholder="Apellido"
                    value={nuevoDirector.apellido}
                    onChange={(e) => setNuevoDirector((n) => ({ ...n, apellido: e.target.value }))}
                  />
                  <input
                    type="text"
                    placeholder="Nacionalidad (opcional)"
                    value={nuevoDirector.nacionalidad}
                    onChange={(e) => setNuevoDirector((n) => ({ ...n, nacionalidad: e.target.value }))}
                  />
                  <div style={{ display: "flex", gap: "8px" }}>
                    <button type="button" className="btn btn-primary" onClick={crearDirectorInline}>
                      Guardar director
                    </button>
                    <button type="button" className="btn btn-ghost" onClick={() => setMostrarNuevoDirector(false)}>
                      Cancelar
                    </button>
                  </div>
                </div>
              )}
            </div>
            <div className="field">
              <label htmlFor="anio">Año</label>
              <input
                type="text"
                id="anio"
                placeholder="Ej. 2014"
                inputMode="numeric"
                value={form.anio}
                onChange={(e) => actualizarCampo("anio", e.target.value.replace(/[^0-9]/g, ""))}
                required
              />
            </div>
          </div>

          <div className="field">
            <label htmlFor="calificacion">Calificación (opcional, 1–10)</label>
            <input
              type="text"
              id="calificacion"
              placeholder="Ej. 9.2"
              inputMode="decimal"
              value={form.calificacion}
              onChange={(e) => actualizarCampo("calificacion", e.target.value.replace(/[^0-9.]/g, ""))}
            />
          </div>

          <div className="field">
            <label htmlFor="sinopsis">Sinopsis</label>
            <textarea
              id="sinopsis"
              placeholder="Escribe una breve sinopsis del título…"
              value={form.sinopsis}
              onChange={(e) => actualizarCampo("sinopsis", e.target.value)}
            />
          </div>

          <div className="field">
            <label>Imagen referencial</label>
            <label className={"upload-box" + (form.imagen ? " has-image" : "")} htmlFor="imagen">
              <input type="file" id="imagen" accept="image/*" onChange={manejarImagen} />
              {form.imagen ? (
                <img className="preview" src={form.imagen} alt="Vista previa" style={{ display: "block" }} />
              ) : (
                <div className="upload-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <rect x="3" y="3" width="18" height="18" rx="2" />
                    <circle cx="8.5" cy="8.5" r="1.5" />
                    <path d="M21 15l-5-5L5 21" />
                  </svg>
                  <div className="upload-text">Haz clic para subir una imagen</div>
                  <div className="upload-hint">PNG, JPG o WEBP · vertical recomendado</div>
                </div>
              )}
            </label>
          </div>

          <div className="field field-status">
            <label>Estado</label>
            <div className="status-toggle chip-row">
              <span
                className={"chip" + (form.estado === "PENDIENTE" ? " on" : "")}
                onClick={() => actualizarCampo("estado", "PENDIENTE")}
              >
                Pendiente
              </span>
              <span
                className={"chip" + (form.estado === "VISTO" ? " on" : "")}
                onClick={() => actualizarCampo("estado", "VISTO")}
              >
                Visto
              </span>
            </div>
          </div>

          <div className="auth-actions">
            <button type="submit" className="btn btn-primary" disabled={guardando}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <path d="M12 5v14M5 12h14" />
              </svg>
              {guardando ? "Guardando…" : esEdicion ? "Guardar cambios" : "Registrar título"}
            </button>
            <Link to="/catalogo" className="btn btn-ghost" style={{ textAlign: "center" }}>
              Cancelar
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Registrar;
