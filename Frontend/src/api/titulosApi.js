import axiosClient from "./axiosClient";

export function listarTitulos() {
  return axiosClient.get("/titulos/").then((res) => res.data);
}

export function obtenerTitulo(id) {
  return axiosClient.get(`/titulos/${id}`).then((res) => res.data);
}

export function crearTitulo(datos) {
  return axiosClient.post("/titulos/", datos).then((res) => res.data);
}

export function actualizarTitulo(id, datos) {
  return axiosClient.put(`/titulos/${id}`, datos).then((res) => res.data);
}

export function eliminarTitulo(id) {
  return axiosClient.delete(`/titulos/${id}`).then((res) => res.data);
}

export function marcarVisto(id) {
  return axiosClient.put(`/titulos/${id}/visto`).then((res) => res.data);
}

export function marcarPendiente(id) {
  return axiosClient.put(`/titulos/${id}/pendiente`).then((res) => res.data);
}

export function calificarTitulo(id, nota) {
  return axiosClient
    .put(`/titulos/${id}/calificacion`, { nota })
    .then((res) => res.data);
}
