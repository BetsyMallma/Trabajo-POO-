import axiosClient from "./axiosClient";

export function listarDirectores() {
  return axiosClient.get("/directores/").then((res) => res.data);
}

export function crearDirector(datos) {
  return axiosClient.post("/directores/", datos).then((res) => res.data);
}
