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


Para conectar la base de datos mysql
1.- En:
  Crear el archivo C:\Program Files\MySQL\MySQL Server 9.32\my.ini
  con:
    [mysqld]
    bind-address = 0.0.0.0

2.- Reiniciar servicio mysql

3.- Desde:
  C:\Program Files\MySQL\MySQL Server 9.32\bin
  Ejecutar:
    mysql -u root -p
    mysql> update user set Host='%' where User='root'
    mysql> flush privileges;
    mysql> SELECT User, Host FROM mysql.user;
    mysql> exit
    
