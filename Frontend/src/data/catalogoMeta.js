// catalogoMeta.js
// El backend todavía no guarda póster ni sinopsis, así que los
// completamos acá en el frontend hasta que esas columnas existan.
//
// La clave DEBE coincidir exactamente con el campo `titulo` de la API.
// Cuando el backend los incluya, solo hay que eliminar el merge en
// catalogo.jsx y listo — este archivo ya no sería necesario.

const BASE_PELICULAS = "/imagenes/PELICULAS/";
const BASE_SERIES = "/imagenes/SERIES/";

const catalogoMeta = {
  "Interstellar": {
    imagen: BASE_PELICULAS + "_Interstellar.webp",
    sinopsis: "Un grupo de astronautas atraviesa un agujero de gusano en busca de un nuevo hogar para la humanidad, mientras el tiempo se convierte en su peor enemigo.",
  },
  "The Dark Knight": {
    imagen: BASE_PELICULAS + "the dark nigth.jpg",
    sinopsis: "Batman se enfrenta al Joker, un criminal que sumerge a Gotham en el caos y pone a prueba los límites morales del héroe.",
  },
  "Oppenheimer": {
    imagen: BASE_PELICULAS + "openhimer.webp",
    sinopsis: "La historia del físico que lideró el desarrollo de la bomba atómica y cargó con el peso moral de su creación.",
  },
  "Barbie": {
    imagen: BASE_PELICULAS + "Poster - BARBIE.webp",
    sinopsis: "Barbie es expulsada del mundo perfecto de Barbieland y emprende un viaje al mundo real que cambiará su forma de ver la vida.",
  },
  "Parasite": {
    imagen: BASE_PELICULAS + "parasite.webp",
    sinopsis: "Una familia humilde se infiltra en la vida de una familia adinerada, desatando una espiral de tensión y conflicto de clases.",
  },
  "Dune": {
    imagen: BASE_PELICULAS + "Dune.jpg",
    sinopsis: "El joven Paul Atreides debe sobrevivir en el desértico planeta Arrakis mientras se cumple un destino que podría cambiar el universo.",
  },
  "The Batman": {
    imagen: BASE_PELICULAS + "The Batman .webp",
    sinopsis: "Un Batman novato investiga una serie de asesinatos que exponen la corrupción oculta de Gotham City.",
  },
  "Tenet": {
    imagen: BASE_PELICULAS + "tenet.webp",
    sinopsis: "Un agente debe manipular el flujo del tiempo para evitar la Tercera Guerra Mundial en una misión que desafía la lógica.",
  },
  "Avatar": {
    imagen: BASE_PELICULAS + "Avatar .webp",
    sinopsis: "Un ex-marine se infiltra en Pandora a través de un avatar Na'vi y termina luchando por proteger el mundo que lo acogió.",
  },
  "Titanic": {
    imagen: BASE_PELICULAS + "titanic.webp",
    sinopsis: "Un romance prohibido florece entre dos pasajeros de distintas clases a bordo del trasatlántico condenado a hundirse.",
  },
  "Avatar 2": {
    imagen: BASE_PELICULAS + "avatar 2.webp",
    sinopsis: "Jake y Neytiri deben proteger a su familia y huir de una nueva amenaza que pone en peligro a Pandora.",
  },
  "Pulp Fiction": {
    imagen: BASE_PELICULAS + "Pulp Fiction .webp",
    sinopsis: "Las vidas de dos sicarios, un boxeador y una pareja de ladrones se entrelazan en historias violentas y absurdas.",
  },
  "Jurassic Park": {
    imagen: BASE_PELICULAS + "jurasic park.webp",
    sinopsis: "Un parque temático con dinosaurios clonados se convierte en una trampa mortal cuando los sistemas de seguridad fallan.",
  },
  "Schindlers List": {
    imagen: BASE_PELICULAS + "Schindler's List.webp",
    sinopsis: "Un empresario alemán salva la vida de más de mil judíos durante el Holocausto empleándolos en sus fábricas.",
  },
  "Little Women": {
    imagen: BASE_PELICULAS + "little women.webp",
    sinopsis: "Las hermanas March enfrentan el amor, la ambición y la pérdida mientras buscan su lugar en el mundo.",
  },
  "The Wolf of Wall Street": {
    imagen: BASE_PELICULAS + "The Wolf of Wall Street .webp",
    sinopsis: "Un corredor de bolsa construye un imperio basado en fraude, excesos y fiestas desenfrenadas hasta que todo se derrumba.",
  },
  "Goodfellas": {
    imagen: BASE_PELICULAS + "goodfellas.webp",
    sinopsis: "La ascensión y caída de un joven que se une al crimen organizado y vive los excesos de la mafia neoyorquina.",
  },
  "Inception": {
    imagen: BASE_PELICULAS + "inception.jpg",
    sinopsis: "Un ladrón que roba secretos corporativos infiltrándose en los sueños recibe la misión inversa: plantar una idea en la mente de un objetivo.",
  },
  "Breaking Bad": {
    imagen: BASE_SERIES + "breaking badf.webp",
    sinopsis: "Un profesor de química con cáncer terminal se convierte en fabricante de metanfetamina para asegurar el futuro de su familia.",
  },
  "Stranger Things": {
    imagen: BASE_SERIES + "Stranger things.webp",
    sinopsis: "La desaparición de un niño desata fuerzas sobrenaturales y un misterio gubernamental en un pequeño pueblo de los años 80.",
  },
  "Dark": {
    imagen: BASE_SERIES + "dark.webp",
    sinopsis: "La desaparición de niños en un pueblo alemán revela un misterio que involucra viajes en el tiempo y secretos familiares.",
  },
  "La Casa de Papel": {
    imagen: BASE_SERIES + "La Casa de Papel.jpg",
    sinopsis: "Un grupo de atracadores planea el robo perfecto a la Fábrica Nacional de Moneda y Timbre de España.",
  },
  "Squid Game": {
    imagen: BASE_SERIES + "Squid game.webp",
    sinopsis: "Cientos de personas endeudadas compiten en juegos infantiles mortales por un premio millonario que podría cambiarles la vida.",
  },
  "The Last of Us": {
    imagen: BASE_SERIES + "The Last of Us.webp",
    sinopsis: "Un contrabandista debe escoltar a una adolescente inmune a través de un Estados Unidos devastado por una infección fúngica.",
  },
  "House of the Dragon": {
    imagen: BASE_SERIES + "House of the Dragon .webp",
    sinopsis: "Las luchas internas de la Casa Targaryen desatan una guerra civil por el trono de hierro de Westeros.",
  },
};

// Si el título no está en catalogoMeta, devuelve valores vacíos por defecto.
// También mezcla con los overrides guardados en localStorage.
export function obtenerMeta(tituloTexto) {
  const overrides = leerOverrides();
  if (overrides[tituloTexto]) {
    return { ...(catalogoMeta[tituloTexto] || {}), ...overrides[tituloTexto] };
  }
  return (
    catalogoMeta[tituloTexto] || {
      imagen: null,
      sinopsis: "Sinopsis no disponible todavía para este título.",
    }
  );
}

// Overrides en localStorage — sirven para guardar sinopsis/imagen de
// títulos nuevos registrados desde el formulario. Solo persisten en
// este navegador, no se comparten entre computadoras.
const CLAVE_OVERRIDES = "sps_meta_overrides";

function leerOverrides() {
  try {
    return JSON.parse(localStorage.getItem(CLAVE_OVERRIDES)) || {};
  } catch {
    return {};
  }
}

export function guardarMetaOverride(tituloTexto, { sinopsis, imagen }) {
  const overrides = leerOverrides();
  overrides[tituloTexto] = {
    sinopsis: sinopsis || overrides[tituloTexto]?.sinopsis || "",
    imagen: imagen !== undefined ? imagen : overrides[tituloTexto]?.imagen ?? null,
  };
  localStorage.setItem(CLAVE_OVERRIDES, JSON.stringify(overrides));
}

export default catalogoMeta;