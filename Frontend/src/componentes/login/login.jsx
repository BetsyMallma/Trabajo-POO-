// El inicio de sesión no es un login real todavía.
//Solo te pide tu nombre, lo guarda en el navegador y después el menú 
// usa ese nombre para mostrarlo arriba junto con tu rol.

import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function leerUsuarioGuardado() {
    try {
    return JSON.parse(localStorage.getItem("sps_user"));
    } catch {
    return null;
    }
}

function Login() {
    const navigate = useNavigate();
    const [nombre, setNombre] = useState("");
    const [rol, setRol] = useState("Administrador");
    const [yaHabiaSesion, setYaHabiaSesion] = useState(false);

    useEffect(() => {
    const guardado = leerUsuarioGuardado();
    if (guardado && guardado.nombre) {
        setNombre(guardado.nombre);
        setRol(guardado.rol || "Administrador");
        setYaHabiaSesion(true);
    }
    }, []);

    function manejarSubmit(e) {
    e.preventDefault();
    const limpio = nombre.trim();
    if (!limpio) return;
    localStorage.setItem("sps_user", JSON.stringify({ nombre: limpio, rol }));
    navigate("/catalogo");
    }

    function cerrarSesion() {
    localStorage.removeItem("sps_user");
    navigate("/catalogo");
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
            <h1>{yaHabiaSesion ? "Actualizar tu sesión" : "Iniciar sesión"}</h1>
            <p>
            {yaHabiaSesion
                ? `Ya iniciaste sesión como ${nombre}. Puedes cambiar tus datos aquí.`
                : "Ingresa tu nombre para identificarte en el panel"}
            </p>
        </div>

        <form onSubmit={manejarSubmit}>
            <div className="field">
            <label htmlFor="nombre">Nombre</label>
            <input
                type="text"
                id="nombre"
                placeholder="Ej. Betsy"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
            />
            </div>

            <div className="field">
            <label htmlFor="rol">Rol</label>
            <select id="rol" value={rol} onChange={(e) => setRol(e.target.value)} required>
                <option value="Administrador">Administrador</option>
                <option value="Usuario">Usuario</option>
            </select>
            </div>

            <div className="auth-actions">
            <button type="submit" className="btn btn-primary">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                <path d="M10 17l5-5-5-5" />
                <path d="M15 12H3" />
                </svg>
                {yaHabiaSesion ? "Guardar cambios" : "Iniciar sesión"}
            </button>
            {yaHabiaSesion && (
                <button type="button" className="btn btn-ghost" onClick={cerrarSesion}>
                Cerrar sesión
                </button>
            )}
            </div>
        </form>
        </div>
    </div>
    )   ;
}

export default Login;
