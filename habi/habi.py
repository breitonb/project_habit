#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
import pymysql  #libreria que me permite establecer conexión a una base de datos mysql
import json
db_user = "pruebas"  #Usuario db
db_pass = "VGbt3Day5R" #clave db
db_name = "habi_db"  # nombre db
db_host = "3.130.126.210" #host db
dirsocket = "/opt/lampp/var/mysql/mysql.sock" #socket de conexión a db
urls = (   #variable tipo tupla que contendra todas las url permitidas de la aplicación
    '/', 'Habit'
    )
app = web.application(urls, globals())   #carga las url a la framework que nos permitira que se puedan consumir los datos desde cualquier api

class Habit:  #definición de clase que se cargara cuando el usuario consuma los datos.
      def estados(self, idinmueble): #funcion para obtener el nombre del estado actual de inmueble
          query = "SELECT status_history.status_id, status.name FROM status_history INNER JOIN status ON status_history.status_id = status.id WHERE status_history.property_id = '%s' ORDER BY update_date DESC LIMIT 1"%idinmueble  #defino el query para mi primer consulta a la base de datos.
          resultado = consultabd(query)  #obtengo informacion de toda la tabla property
          return resultado[0][1]  #retorno el nombre del estado del inmueble a partir de la consulta generada

      def verifica_estado(self, idinmueble): #funcion para controlar los estados que puede visualizar el usuario
          query = "SELECT status_history.status_id FROM status_history INNER JOIN status ON status_history.status_id = status.id WHERE status_history.property_id = '%s' ORDER BY update_date DESC LIMIT 1"%idinmueble  #defino el query para mi primer consulta a la base de datos.
          print(query)
          resultado = consultabd(query)  #obtengo informacion de toda la tabla property
          if len(resultado) > 0:  #controlo la respuesta del estado del inmueble
             if resultado[0][0] == 3 or resultado[0][0] == 4 or resultado[0][0] == 5:  #evalua los id de los estados permitidos que son 3 pre_venta, 4 en_venta y 5 vendido
                return "S"  #
             else:
                return "N"
          else:
             return "N"
          
      def GET(self):
        #defino propiedades del header de mi aplicación------------------------------#
          web.header('Access-Control-Allow-Origin', '*')
          web.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
          web.header('Access-Control-Allow-Headers', 'X-Requested-With,content-type')
          web.header('Content-type', 'text/json', 'charset=iso-8859-1') 
        #----------------------------------------------------------------------------#
          varhtml = web.input()  #en esta variable se reciben todos los posibles filtros desde dónde se quieran consumir los datos
          query = "SELECT * FROM property"  #defino un query general de los inmuebles y si por algún motivo encuentro que viene un filtro, este query cambia mas abajo
          try:   #en el consumo de los datos, se pueden o no enviar los datos del filtro, en caso de que no se envíen, con esta condición el programa no genera error
             year = varhtml.year
          except:
             year = ""
          try:
             city = varhtml.city
          except:
             city = ""
          try:
             state = varhtml.state
          except:
             state = ""
          if year != "":  #verifico si vienen datos del filtro para que genere un nuevo query con el filtro
             query = "SELECT * FROM property WHERE year = '%s'"%year 
          if city != "":
             query = "SELECT * FROM property WHERE city = '%s'"%city  
          if city != "" and year != "":  #controlo si viene mas de un filtro para crear un neuvo query
             query = "SELECT * FROM property WHERE year = '%s' AND city = '%s'"%(year, city)  #defino el query para mi primer consulta a la base de datos.
          print(query)
          resultado = consultabd(query)  #obtengo informacion de toda la tabla property
          if resultado == "conexion0":
             return "Sin Conexion a base de datos"
          archivo_json = '[\n'  #inicializo una variable tipo json 
          contador = 0   #inicializo contador en 0 para controlar que el json quedebe con la estructura correcta
          listado = []
          if len(resultado) > 0:  #evaluo que la onsulta tenga información
             for data in resultado:  #recorro los datos 1 a 1
                 idinmueble = data[0]
                 estado = self.verifica_estado(idinmueble)  #funcion que controla los estados que se pueden visualizar
                 if estado == "S":
                    address = data[1]
                    city = data[2]
                    state = self.estados(idinmueble)
                    price = data[3]
                    description = data[4]
                    year = data[5]
                    archivo_json = archivo_json + '{"id":"%s", "address":"%s", "city":"%s", "state":"%s", "price":"%s", "description":"%s"},\n'%(idinmueble, address, city, state, price, description)
                    listado.append({"id": idinmueble, "address": address, "city": city, "state": state, "price": price, "description": description})
                    contador += 1
             else:
                if contador > 0:
                   archivo_json = archivo_json[:len(archivo_json)-2]  #en esta sentencia estoy quitanto los ultimos caracteres que son la coma(,) y el salto de linea ya que dejar eso en el ultimo registro genera error en el archivos json
          archivo_json = archivo_json + ']' #cerramos el archivo json
          print(archivo_json)
          return json.dumps(listado)
          return archivo_json 

def consultabd(query): #funcion que recibe el código para hacer una consulta a la base de datos y devolver un resultado
    try:
       #parametros para establecer conexión a la base de datos
       db = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name, port=3309)
    except:
       #si no tenemos respuesta de la base de datos, avisaremos con este mensaje
       return "conexion0"
    cursor = db.cursor()   #establecemos conexión a la base de datos
    cursor.execute(query)  #ejecutamos el query en la base de datos
    resultado = cursor.fetchall()  #obtenemos todos los datos de la consulta
    cursor.close()   #cerramos la consexión que hicimos a la base de datos
    return resultado  #Retornamos el valor de la consulta de la base de datos

def sentenciadb(query): #ejecución de sentencia a la base de datos, como insert, update o delete
    try:   
       #parametros para establecer conexión a la base de datos
       db = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name, port=3309)
    except:
       return "conexion0"
    cursor = db.cursor()  #establecemos conexión a la base de datos
    cursor.execute(query) #ejecutamos el query en la base de datos
    db.commit()   #con esto hacemos que la sentencia sea efectiva en la base de datos
    cursor.close()  #cerramos la consexión que hicimos a la base de datos
    return "OK"  #si todo va bien devolvemos un ok confirmando la ejecucion


#agregando un comentario
def main():
    web.internalerror = web.debugerror
    app.run()
    return 0

if __name__ == '__main__':
    app.run()
