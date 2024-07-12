-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-07-2024 a las 20:31:10
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `dbmusica`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `idgenero` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `album` varchar(50) NOT NULL,
  `anio` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `precio` float(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `idgenero`, `nombre`, `album`, `anio`, `descripcion`, `imagen`, `precio`) VALUES
(2, 3, 'queen', 'NEWS OF THE WORLD', 1977, 'DVD', 'queen_1720808295.jpeg', 120.00),
(3, 5, 'Nirvana', 'Bleach', 1979, 'Formato: CD, casete, LP', 'nirvana_1720806136.png', 100.00),
(11, 5, 'aerosmith', 'get your wings', 1974, 'formato CD', 'aerosmith_1720808246.jpeg', 34.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `provincia`
--

CREATE TABLE `provincia` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `provincia`
--

INSERT INTO `provincia` (`id`, `descripcion`) VALUES
(1, 'Ciudad Autónoma de Buenos Aires'),
(2, 'Buenos Aires'),
(3, 'Catamara'),
(4, 'Córdoba'),
(5, 'Corrientes'),
(6, 'Entre Ríos'),
(7, 'Jujuy'),
(8, 'Mendoza'),
(9, 'La Rioja'),
(10, 'Salta'),
(11, 'San juan'),
(12, 'San Luis'),
(13, 'Santa Fe'),
(14, 'Santiago del Estero'),
(15, 'Tucumán'),
(16, 'Chaco'),
(17, 'Chubut'),
(18, 'Formosa'),
(19, 'Misiones'),
(20, 'Neuquén'),
(21, 'La Pampa'),
(22, 'Río Negro'),
(23, 'Santa Cruz'),
(24, 'Tierra del Fuego');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `tipo_user` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `sexo` varchar(10) DEFAULT NULL,
  `direccion` varchar(50) DEFAULT NULL,
  `provincia` varchar(50) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `create_at` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `tipo_user`, `nombre`, `apellido`, `fecha_nacimiento`, `sexo`, `direccion`, `provincia`, `telefono`, `email`, `password`, `create_at`) VALUES
(1, 1, 'cesar enrique', 'cantoral', NULL, 'Masculino', NULL, 'Jujuy', NULL, 'cecmacuario@hotmail.com', '12345', NULL),
(3, 0, 'raul', 'cerapio', NULL, NULL, NULL, 'San Luis', NULL, '', '12345', NULL),
(4, 0, 'richard cristian', 'centurion', NULL, 'Femenino', NULL, 'Santa Fe', NULL, 'centurion@hotmail.com', '12345', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `provincia`
--
ALTER TABLE `provincia`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `provincia`
--
ALTER TABLE `provincia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
