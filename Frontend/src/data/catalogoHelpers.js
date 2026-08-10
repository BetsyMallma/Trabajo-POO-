//===========================================================
// catalogoHelpers.js
//===========================================================

// Funciones puras para transformar los datos de la API al formato
// que espera el diseño visual de SPS.

// Mapa de género (BD) → slug para las clases CSS g-* y chips del sidebar
const SLUGS_GENERO = {
  "Accion": "accion",
  "Drama": "drama",
  "Comedia": "comedia",
  "Terror": "terror",
  "Ciencia Ficcion": "ciencia",
  "Animacion": "animacion",
  "Thriller": "thriller",
  "Romance": "romance",
};

export function slugGenero(nombreGenero) {
  return SLUGS_GENERO[nombreGenero] || nombreGenero.toLowerCase();
}

// "Christopher Nolan" → "C. Nolan"
export function nombreCortoDirector(director) {
  if (!director) return "—";
  const inicial = director.nombre ? director.nombre.charAt(0) + ". " : "";
  return inicial + director.apellido;
}

// "PELICULA" → "PELÍCULA" / "SERIE" → "SERIE"
export function etiquetaTipo(tipo) {
  return tipo === "PELICULA" ? "PELÍCULA" : "SERIE";
}