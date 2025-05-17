CREATE SCHEMA 'traking' ;

CREATE TABLE `mitrack` (
  `idmitrack` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(15) DEFAULT NULL,
  `fechahora` datetime DEFAULT NULL,
  `direccion` varchar(10) DEFAULT NULL,
  `color` varchar(15) DEFAULT NULL,
  `marca` varchar(15) DEFAULT NULL,
  `modelo` varchar(15) DEFAULT NULL,
  `patente` varchar(8) DEFAULT NULL,
  `image` mediumblob,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`idmitrack`),
  KEY `idx_fechahora` (`fechahora`)
) ENGINE=InnoDB AUTO_INCREMENT=3014 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci