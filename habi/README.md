# Entregable Prueba Técnica Habi

Tecnologías usadas:
1. python 3
2. web.py
3. pymysql
4. json

Instalación:
1. Para Instalar python3 se puede descargar el paquete completo en https://www.anaconda.com/products/individual 
2. pip3 install web.py.
3. pip3 install pymysql ó pip3 install PyMySQL.
4. pip3 install json  #por lo general viene instalado en las versiones de python.

Dudas: 


Dudas Resueltas:




Primer Requerimiento:



Segundo Requerimiento:

![image](https://user-images.githubusercontent.com/94751889/142776772-5afdd5ae-fa86-4408-b6c5-0b3317bdf999.png)

Creación tabla user:
 
CREATE TABLE "user" ( id int(9) NOT NULL, username varchar(25) NOT NULL, first_name varchar(50) NOT NULL, last_name varchar(50) NOT NULL, email varchar(244) NOT NULL, state tinyint(1) NOT NULL, PRIMARY KEY(id, username) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 
Creación tabla property:
CREATE TABLE "property" ( id int(11) NOT NULL, address varchar(120) NOT NULL, city varchar(32) NOT NULL, price bigint(20) NOT NULL, description text NOT NULL, year int(4) NOT NULL, PRIMARY KEY(id) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 
Creación tabla like_property:
CREATE TABLE "like_property" ( id int(9) NOT NULL, id_user int(9) NOT NULL, id_property int(11) NOT NULL, action enum('', 'like', 'do not like') NOT NULL, last_update datetime NOT NULL, PRIMARY KEY(id) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 


Incluyendo información en tabla user:
INSERT INTO user (id, username, first_name, last_name, email, state) VALUES (1,"breitonb","Breiton","Bustos Bustos","breitonb_16@hotmail.com",1);

Incluyendo información en tabla property:
INSERT INTO property (id, address, city, price, description, year) VALUES (1, "calle 23 #45-67", "bogota", "120000000", "Hermoso apartamento en el centro de la ciudad", "2000");

Incluyendo información en tabla like_property:
INSERT INTO like_property  (id, id_user, id_property, action, last_update) VALUES (1, 1, 1, 'like', '2021-11-21 12:00:00');


Puntos Extras:

2. Proponer un mejor modelo de la estructura actual de base de datos, con el objetivo de
mejorar la velocidad de las consultas, se espera un diagrama y la explicación de porque
lo modelaste de esa forma.

Rta: La tabla property, debería tener una columna con el estado, ya que esto es una propiedad del inmueble y aunque este cambié, solo debería tener un estado actual, el cual podría cambiar y este si debería estan en la tabla status_history solo para llevar un log de cambio de estados, con esto se podría hacer una consulta directa a la tabla y la generación de la información sería mas rápida.
