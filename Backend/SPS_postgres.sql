-- ============================================================
-- SCRIPT DDL + DML — SPS: Sistema de Peliculas y Series
-- Motor: PostgreSQL (migrado desde SQL Server)
-- Integrantes: Mallma Vito Betsy Jazmin
--              Tantavilca Razzo Aldo David
-- ============================================================

-- ============================================================
-- PASO 1: CREAR LA BASE DE DATOS
-- (ejecutar esta linea sola, conectado a la BD "postgres" por defecto)
-- ============================================================
-- CREATE DATABASE bd_sps;

-- ============================================================
-- PASO 2: CREAR TABLAS (DDL)
-- ============================================================

-- Tabla: genero
CREATE TABLE genero
(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(200)
);

-- Tabla: director
CREATE TABLE director
(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    nacionalidad VARCHAR(60)
);

-- Tabla: titulo
CREATE TABLE titulo
(
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('PELICULA','SERIE')),
    anio INT NOT NULL,
    calificacion NUMERIC(3,1) CHECK (calificacion >= 1 AND calificacion <= 10),
    estado VARCHAR(10) NOT NULL CHECK (estado IN ('VISTO','PENDIENTE')),
    id_genero INT NOT NULL REFERENCES genero(id),
    id_director INT NOT NULL REFERENCES director(id)
);

-- ============================================================
-- PASO 3: INSERTAR DATOS (DML)
-- ============================================================

-- Datos: genero
INSERT INTO genero
    (id, nombre, descripcion)
VALUES
    (1, 'Accion', 'Peliculas con escenas de pelea, explosiones y persecuciones'),
    (2, 'Drama', 'Historias emocionales y personajes con conflictos profundos'),
    (3, 'Comedia', 'Contenido humoristico con situaciones divertidas'),
    (4, 'Terror', 'Contenido que genera miedo o suspenso en el espectador'),
    (5, 'Ciencia Ficcion', 'Historias futuristas con tecnologia avanzada o espacio'),
    (6, 'Animacion', 'Contenido animado para todo publico'),
    (7, 'Thriller', 'Historias de suspenso con giros inesperados'),
    (8, 'Romance', 'Historias centradas en relaciones amorosas');

-- Datos: director
INSERT INTO director
    (id, nombre, apellido, nacionalidad)
VALUES
    (1, 'Christopher', 'Nolan', 'Britanico'),
    (2, 'Steven', 'Spielberg', 'Estadounidense'),
    (3, 'James', 'Cameron', 'Canadiense'),
    (4, 'Quentin', 'Tarantino', 'Estadounidense'),
    (5, 'Greta', 'Gerwig', 'Estadounidense'),
    (6, 'Martin', 'Scorsese', 'Estadounidense'),
    (7, 'Pedro', 'Almodovar', 'Espanol'),
    (8, 'Bong', 'Joon-ho', 'Surcoreano');

-- Datos: titulo (mezcla de peliculas y series, vistas y pendientes)
-- Los que tienen calificacion NULL son los que estan PENDIENTE, porque
-- todavia no se vieron y por lo tanto no se pueden calificar.
INSERT INTO titulo
    (id, titulo, tipo, anio, calificacion, estado, id_genero, id_director)
VALUES
    (1, 'Inception', 'PELICULA', 2010, 9.0, 'VISTO', 5, 1),
    (2, 'Interstellar', 'PELICULA', 2014, 9.5, 'VISTO', 5, 1),
    (3, 'The Dark Knight', 'PELICULA', 2008, 9.8, 'VISTO', 1, 1),
    (4, 'Jurassic Park', 'PELICULA', 1993, 8.5, 'VISTO', 5, 2),
    (5, 'Schindlers List', 'PELICULA', 1993, 9.2, 'VISTO', 2, 2),
    (6, 'Avatar', 'PELICULA', 2009, 7.8, 'VISTO', 5, 3),
    (7, 'Titanic', 'PELICULA', 1997, 8.0, 'VISTO', 8, 3),
    (8, 'Pulp Fiction', 'PELICULA', 1994, 9.0, 'VISTO', 7, 4),
    (9, 'Barbie', 'PELICULA', 2023, 7.5, 'VISTO', 3, 5),
    (10, 'Little Women', 'PELICULA', 2019, 8.0, 'VISTO', 2, 5),
    (11, 'The Wolf of Wall Street', 'PELICULA', 2013, 8.7, 'VISTO', 2, 6),
    (12, 'Goodfellas', 'PELICULA', 1990, 9.1, 'VISTO', 2, 6),
    (13, 'Parasite', 'PELICULA', 2019, 9.3, 'VISTO', 7, 8),
    (14, 'The Batman', 'PELICULA', 2022, NULL, 'PENDIENTE', 7, 1),
    (15, 'Oppenheimer', 'PELICULA', 2023, NULL, 'PENDIENTE', 2, 1),
    (16, 'Tenet', 'PELICULA', 2020, NULL, 'PENDIENTE', 1, 1),
    (17, 'Dune', 'PELICULA', 2021, NULL, 'PENDIENTE', 5, 2),
    (18, 'Avatar 2', 'PELICULA', 2022, NULL, 'PENDIENTE', 5, 3),
    (19, 'Breaking Bad', 'SERIE', 2008, 9.9, 'VISTO', 7, 4),
    (20, 'Stranger Things', 'SERIE', 2016, 8.8, 'VISTO', 5, 2),
    (21, 'Dark', 'SERIE', 2017, 9.2, 'VISTO', 5, 1),
    (22, 'La Casa de Papel', 'SERIE', 2017, 8.5, 'VISTO', 7, 7),
    (23, 'Squid Game', 'SERIE', 2021, 8.0, 'VISTO', 7, 8),
    (24, 'The Last of Us', 'SERIE', 2023, NULL, 'PENDIENTE', 7, 2),
    (25, 'House of the Dragon', 'SERIE', 2022, NULL, 'PENDIENTE', 1, 3);

-- ============================================================
-- PASO 4: SINCRONIZAR LAS SECUENCIAS (SERIAL)
-- ============================================================
SELECT setval('genero_id_seq',   (SELECT MAX(id)
    FROM genero));
SELECT setval('director_id_seq', (SELECT MAX(id)
    FROM director));
SELECT setval('titulo_id_seq',   (SELECT MAX(id)
    FROM titulo));

-- ============================================================
-- PASO 5: CONSULTAS DE VERIFICACION
-- ============================================================

-- Ver todos los titulos con genero y director
SELECT
    t.id,
    t.titulo,
    t.tipo,
    t.anio,
    t.calificacion,
    t.estado,
    g.nombre               AS genero,
    d.nombre || ' ' || d.apellido AS director
FROM titulo t
    JOIN genero   g ON t.id_genero   = g.id
    JOIN director d ON t.id_director = d.id
ORDER BY t.id;

-- Ver solo los titulos vistos
SELECT titulo, tipo, calificacion
FROM titulo
WHERE estado = 'VISTO'
ORDER BY calificacion DESC;

-- Ver solo los titulos pendientes
SELECT titulo, tipo, anio
FROM titulo
WHERE estado = 'PENDIENTE';

-- Contar titulos por genero
SELECT g.nombre AS genero, COUNT(t.id) AS total
FROM genero g
    LEFT JOIN titulo t ON g.id = t.id_genero
GROUP BY g.nombre
ORDER BY total DESC;

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================