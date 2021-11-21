# Entregable Prueba Técnica Habi

Tecnologías usadas:
1. python 3
2. web.py  https://webpy.org/
3. pymysql  https://pypi.org/project/PyMySQL/
4. json  https://docs.python.org/es/3/library/json.html

Instalación:
1. Para Instalar python3 se puede descargar el paquete completo en https://www.anaconda.com/products/individual 
2. pip3 install web.py.
3. pip3 install pymysql ó pip3 install PyMySQL.
4. pip3 install json  #por lo general viene instalado en las versiones de python.

Las pruebas de la aplicación fueron realizadas en python 3, sin embargo también puede funcionar en python 2, realizando unas pocas adecuaciones.

Primer Requerimiento, Servicio Consulta:

Para este primer requerimiento, empece a trabajar en la estructura de los datos que debía entregar a la api, para esto, estudie primero las tablas y arme los datos que debía entregar, esto me tomo algo de tiempo ya que la estructura de la tabla property tenía el estado en otra tabla(status_history) y este dato se repetia tantas veces haya cambiado el estado, esto hace que tenga que realizar lectura a 3 tablas, para obtener el resultado esperado, en mi opinión, el estado debe de ser un dato de la tabla property, ya que es una propiedad del inmueble, con esto, se harían lectura solo a la tabla property y a la tabla status, esto hace que la consulta se genere mas rápido y en status_history, debería quedar ese dato pero como log.

A continuación, realaciono print de las pruebas realizadas, con los filtros solicitados.

Prueba 1: Consultando los datos sin filtro, solo los estados permitidos.
![image](https://user-images.githubusercontent.com/94751889/142778745-22c41134-9cfa-4231-96e1-485d8f1ac238.png)

Prueba 2: Consulta datos, con filtro de ciudad.
![image](https://user-images.githubusercontent.com/94751889/142778786-da41ae5d-7b2f-4a3e-a8e3-06e824cfb596.png)

Prueba 3: Consultado datos, con filtro de ciudad y año.
![image](https://user-images.githubusercontent.com/94751889/142778808-ad2f5b10-22c3-4c12-a6ea-8ef557cd1551.png)

Prueba 4: Consultado datos, aplicando todos los filtros permitidos.
![image](https://user-images.githubusercontent.com/94751889/142778881-1ee4c9a0-ba09-4a03-a827-becc4e6f295b.png)

En todas las pruebas, se esta generando información en archivo json, con los datos solicitados y un dato adicional que es el id del inmueble.

Segundo Requerimiento, Servicio "Me Gusta":

                                  DIAGRAMA ENTIDAD REALICIÓN SERVICIO ME GUSTA

![image](https://user-images.githubusercontent.com/94751889/142780318-6f275b87-8bee-49f0-ae74-8566b9f6981f.png)


Creación tabla user:
CREATE TABLE "user" ( id int(9) NOT NULL, username varchar(25) NOT NULL, first_name varchar(50) NOT NULL, last_name varchar(50) NOT NULL, email varchar(244) NOT NULL, state tinyint(1) NOT NULL, PRIMARY KEY(id, username) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  

Creación tabla like_property:
CREATE TABLE "like_property" ( id int(9) NOT NULL, id_user int(9) NOT NULL, id_property int(11) NOT NULL, action enum('', 'like', 'do not like') NOT NULL, last_update datetime NOT NULL, PRIMARY KEY(id) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 

Incluyendo información en tabla user:
INSERT INTO user (id, username, first_name, last_name, email, state) VALUES (1,"breitonb","Breiton","Bustos Bustos","breitonb_16@hotmail.com",1);

Incluyendo información en tabla property:
INSERT INTO property (id, address, city, price, description, year) VALUES (1, "calle 23 #45-67", "bogota", "120000000", "Hermoso apartamento en el centro de la ciudad", "2000");

Incluyendo información en tabla like_property:
INSERT INTO like_property  (id, id_user, id_property, action, last_update) VALUES (1, 1, 1, 'like', '2021-11-21 12:00:00');

Para el segundo requerimiento y teniendo en cuenta la estructura de las tablas, es necesario crear una tabla user, para registrar información del usuario que interactura con la aplicación y una tabla de like_property, para registrar información de los productos de interes del usuario, esta tabla debe ser alterna ya que a un usuario le pueden gustar muchos productos y esta información debe quedar almacenada en la base de datos.

Puntos Extras:

2. Proponer un mejor modelo de la estructura actual de base de datos, con el objetivo de
mejorar la velocidad de las consultas, se espera un diagrama y la explicación de porque
lo modelaste de esa forma.

Rta: Para este punto sugiero que el estado debe de ser un dato de la tabla property, por tal motivo se debería agregar la columna state en la tabla property ya que es una propiedad del inmueble, con esto, se harían lectura solo a la tabla property y a la tabla status, esto hace que la consulta se genere mas rápido y en status_history solo quedaría el logs de los estados del inmueble.
