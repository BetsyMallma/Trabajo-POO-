-- ============================================================
-- SCRIPT DDL + DML — SPS: Sistema de Películas y Series
-- Motor: SQL Server / PostgreSQL compatible
-- Integrantes: Mallma Vito Betsy Jazmín
--              Tantavilca Razzo Aldo David
-- Ciclo: 2025-I
-- ============================================================
 
-- ============================================================
-- PASO 1: CREAR Y USAR LA BASE DE DATOS
-- ============================================================
CREATE DATABASE BD_SPS;
USE BD_SPS;
 
-- ============================================================
-- PASO 2: CREAR TABLAS (DDL)
-- ============================================================
 
-- Tabla: GENERO
CREATE TABLE GENERO (
    ID_GENERO   INT          NOT NULL,
    NOMBRE      VARCHAR(80)  NOT NULL,
    DESCRIPCION VARCHAR(200),
    PRIMARY KEY (ID_GENERO)
);
 
-- Tabla: DIRECTOR
CREATE TABLE DIRECTOR (
    ID_DIRECTOR  INT         NOT NULL,
    NOMBRE       VARCHAR(60) NOT NULL,
    APELLIDO     VARCHAR(60) NOT NULL,
    NACIONALIDAD VARCHAR(60),
    PRIMARY KEY (ID_DIRECTOR)
);
 
-- Tabla: TITULO
CREATE TABLE TITULO (
    ID_TITULO    INT          NOT NULL,
    TITULO       VARCHAR(150) NOT NULL,
    TIPO         VARCHAR(10)  NOT NULL CHECK (TIPO IN ('PELICULA','SERIE')),
    ANIO         INT          NOT NULL,
    CALIFICACION DECIMAL(3,1) CHECK (CALIFICACION >= 1 AND CALIFICACION <= 10),
    ESTADO       VARCHAR(10)  NOT NULL CHECK (ESTADO IN ('VISTO','PENDIENTE')),
    ID_GENERO    INT          NOT NULL,
    ID_DIRECTOR  INT          NOT NULL,
    PRIMARY KEY (ID_TITULO),
    FOREIGN KEY (ID_GENERO)   REFERENCES GENERO(ID_GENERO),
    FOREIGN KEY (ID_DIRECTOR) REFERENCES DIRECTOR(ID_DIRECTOR)
);
 
-- ============================================================
-- PASO 3: INSERTAR DATOS (DML)
-- ============================================================
 
-- Datos: GENERO
INSERT INTO GENERO (ID_GENERO, NOMBRE, DESCRIPCION) VALUES
(1, 'Accion',       'Peliculas con escenas de pelea, explosiones y persecuciones'),
(2, 'Drama',        'Historias emocionales y personajes con conflictos profundos'),
(3, 'Comedia',      'Contenido humoristico con situaciones divertidas'),
(4, 'Terror',       'Contenido que genera miedo o suspenso en el espectador'),
(5, 'Ciencia Ficcion', 'Historias futuristas con tecnologia avanzada o espacio'),
(6, 'Animacion',    'Contenido animado para todo publico'),
(7, 'Thriller',     'Historias de suspenso con giros inesperados'),
(8, 'Romance',      'Historias centradas en relaciones amorosas');
 
-- Datos: DIRECTOR
INSERT INTO DIRECTOR (ID_DIRECTOR, NOMBRE, APELLIDO, NACIONALIDAD) VALUES
(1, 'Christopher', 'Nolan',      'Britanico'),
(2, 'Steven',      'Spielberg',  'Estadounidense'),
(3, 'James',       'Cameron',    'Canadiense'),
(4, 'Quentin',     'Tarantino',  'Estadounidense'),
(5, 'Greta',       'Gerwig',     'Estadounidense'),
(6, 'Martin',      'Scorsese',   'Estadounidense'),
(7, 'Pedro',       'Almodovar',  'Espanol'),
(8, 'Bong',        'Joon-ho',    'Surcoreano');
 
-- Datos: TITULO (mezcla de peliculas y series, vistas y pendientes)
INSERT INTO TITULO (ID_TITULO, TITULO, TIPO, ANIO, CALIFICACION, ESTADO, ID_GENERO, ID_DIRECTOR) VALUES
(1,  'Inception',              'PELICULA', 2010, 9.0, 'VISTO',     5, 1),
(2,  'Interstellar',           'PELICULA', 2014, 9.5, 'VISTO',     5, 1),
(3,  'The Dark Knight',        'PELICULA', 2008, 9.8, 'VISTO',     1, 1),
(4,  'Jurassic Park',          'PELICULA', 1993, 8.5, 'VISTO',     5, 2),
(5,  'Schindlers List',        'PELICULA', 1993, 9.2, 'VISTO',     2, 2),
(6,  'Avatar',                 'PELICULA', 2009, 7.8, 'VISTO',     5, 3),
(7,  'Titanic',                'PELICULA', 1997, 8.0, 'VISTO',     8, 3),
(8,  'Pulp Fiction',           'PELICULA', 1994, 9.0, 'VISTO',     7, 4),
(9,  'Barbie',                 'PELICULA', 2023, 7.5, 'VISTO',     3, 5),
(10, 'Little Women',           'PELICULA', 2019, 8.0, 'VISTO',     2, 5),
(11, 'The Wolf of Wall Street','PELICULA', 2013, 8.7, 'VISTO',     2, 6),
(12, 'Goodfellas',             'PELICULA', 1990, 9.1, 'VISTO',     2, 6),
(13, 'Parasite',               'PELICULA', 2019, 9.3, 'VISTO',     7, 8),
(14, 'The Batman',             'PELICULA', 2022, NULL,'PENDIENTE',  7, 1),
(15, 'Oppenheimer',            'PELICULA', 2023, NULL,'PENDIENTE',  2, 1),
(16, 'Tenet',                  'PELICULA', 2020, NULL,'PENDIENTE',  1, 1),
(17, 'Dune',                   'PELICULA', 2021, NULL,'PENDIENTE',  5, 2),
(18, 'Avatar 2',               'PELICULA', 2022, NULL,'PENDIENTE',  5, 3),
(19, 'Breaking Bad',           'SERIE',    2008, 9.9, 'VISTO',     7, 4),
(20, 'Stranger Things',        'SERIE',    2016, 8.8, 'VISTO',     5, 2),
(21, 'Dark',                   'SERIE',    2017, 9.2, 'VISTO',     5, 1),
(22, 'La Casa de Papel',       'SERIE',    2017, 8.5, 'VISTO',     7, 7),
(23, 'Squid Game',             'SERIE',    2021, 8.0, 'VISTO',     7, 8),
(24, 'The Last of Us',         'SERIE',    2023, NULL,'PENDIENTE',  7, 2),
(25, 'House of the Dragon',    'SERIE',    2022, NULL,'PENDIENTE',  1, 3);
 
-- ============================================================
-- PASO 4: CONSULTAS DE VERIFICACION
-- ============================================================
 
-- Ver todos los titulos con genero y director
SELECT
    T.ID_TITULO,
    T.TITULO,
    T.TIPO,
    T.ANIO,
    T.CALIFICACION,
    T.ESTADO,
    G.NOMBRE   AS GENERO,
    D.NOMBRE + ' ' + D.APELLIDO AS DIRECTOR
FROM TITULO T
INNER JOIN GENERO   G ON T.ID_GENERO   = G.ID_GENERO
INNER JOIN DIRECTOR D ON T.ID_DIRECTOR = D.ID_DIRECTOR
ORDER BY T.ID_TITULO;
 
-- Ver solo los titulos vistos
SELECT TITULO, TIPO, CALIFICACION
FROM TITULO
WHERE ESTADO = 'VISTO'
ORDER BY CALIFICACION DESC;
 
-- Ver solo los titulos pendientes
SELECT TITULO, TIPO, ANIO
FROM TITULO
WHERE ESTADO = 'PENDIENTE';
 
-- Contar titulos por genero
SELECT G.NOMBRE AS GENERO, COUNT(T.ID_TITULO) AS TOTAL
FROM GENERO G
LEFT JOIN TITULO T ON G.ID_GENERO = T.ID_GENERO
GROUP BY G.NOMBRE
ORDER BY TOTAL DESC;
 
-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================