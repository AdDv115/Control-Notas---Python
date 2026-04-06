-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 16-03-2026 a las 15:43:09
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `web`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Estudiantes`
--

CREATE TABLE `Estudiantes` (
  `idestudiante` int(11) NOT NULL,
  `Nombre` varchar(40) DEFAULT NULL,
  `Edad` int(11) DEFAULT NULL,
  `Carrera` varchar(40) DEFAULT NULL,
  `nota1` decimal(1,0) DEFAULT NULL,
  `nota2` decimal(1,0) DEFAULT NULL,
  `nota3` decimal(1,0) DEFAULT NULL,
  `Promedio` decimal(10,0) DEFAULT NULL,
  `Desempeño` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Estudiantes`
--

INSERT INTO `Estudiantes` (`idestudiante`, `Nombre`, `Edad`, `Carrera`, `nota1`, `nota2`, `nota3`, `Promedio`, `Desempeño`) VALUES
(91, 'Maria Lopez', 35, 'Administracion Empresas', 4, 1, 3, 3, 'Bajo'),
(92, 'Valentina Mora', 28, 'Derecho', 1, 1, 3, 2, 'Bajo'),
(93, 'Andres Torres', 27, 'Derecho', 5, 1, 5, 4, 'Regular'),
(94, 'Valentina Mora', 24, 'Contaduria', 3, 3, 1, 3, 'Bajo'),
(95, 'Juan Perez', 24, 'Psicologia', 0, 3, 1, 1, 'Bajo'),
(96, 'Andres Torres', 30, 'Arquitectura', 0, 4, 2, 2, 'Bajo'),
(97, 'Sofia Herrera', 22, 'Medicina', 3, 1, 3, 3, 'Bajo'),
(98, 'Felipe Vargas', 23, 'Arquitectura', 1, 4, 0, 2, 'Bajo'),
(99, 'Felipe Vargas', 15, 'Administracion Empresas', 3, 1, 2, 2, 'Bajo'),
(100, 'Daniela Cruz', 13, 'Derecho', 1, 1, 4, 2, 'Bajo'),
(101, 'Jose Castro', 17, 'Medicina', 5, 1, 4, 3, 'Regular'),
(102, 'Ana Rodriguez', 17, 'Ingenieria Sistemas', 4, 3, 4, 4, 'Regular'),
(103, 'Laura Gutierrez', 21, 'Ingenieria Industrial', 2, 2, 1, 2, 'Bajo'),
(104, 'Daniela Cruz', 25, 'Administracion Empresas', 4, 5, 3, 4, 'Bueno'),
(105, 'Felipe Vargas', 27, 'Contaduria', 1, 3, 5, 3, 'Regular'),
(106, 'Valentina Mora', 0, 'Ingenieria Industrial', 4, 3, 5, 4, 'Bueno'),
(107, 'Maria Lopez', 17, 'Ingenieria Industrial', 4, 0, 2, 2, 'Bajo'),
(108, 'Luis Martinez', 15, 'Arquitectura', 1, 1, 3, 2, 'Bajo'),
(109, 'Laura Gutierrez', 24, 'Ingenieria Sistemas', 2, 3, 3, 3, 'Bajo'),
(110, 'Laura Gutierrez', 6, 'Psicologia', 4, 3, 0, 2, 'Bajo'),
(111, 'Sebastian Ruiz', 29, 'Ingenieria Industrial', 5, 2, 2, 3, 'Bajo'),
(112, 'Paul', 89, 'Adso', 5, 4, 3, 4, 'Bueno');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuarios`
--

CREATE TABLE `Usuarios` (
  `idusuario` int(11) NOT NULL,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `rolusu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Usuarios`
--

INSERT INTO `Usuarios` (`idusuario`, `username`, `password`, `rolusu`) VALUES
(1, 'admin', '1234', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Estudiantes`
--
ALTER TABLE `Estudiantes`
  ADD PRIMARY KEY (`idestudiante`);

--
-- Indices de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  ADD PRIMARY KEY (`idusuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Estudiantes`
--
ALTER TABLE `Estudiantes`
  MODIFY `idestudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT de la tabla `Usuarios`
--
ALTER TABLE `Usuarios`
  MODIFY `idusuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
