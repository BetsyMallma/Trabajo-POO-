import axiosClient from "./axiosClient";

export function listarGeneros() {
  return axiosClient.get("/generos/").then((res) => res.data);
}

export function crearGenero(datos) {
  return axiosClient.post("/generos/", datos).then((res) => res.data);
}
