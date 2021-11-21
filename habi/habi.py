#!/usr/bin/env python
# -*- coding: utf-8 -*-
#autor: Breiton Bustos
#Fec Crecion: 2021-11-20
#framework que me permite consultar la app como peticiones request
import web 
#libreria que me permite establecer conexión a una base de datos mysql
import pymysql  
 #convierte una lista en archivo json para entregar los datos
import json 
#variable tipo tupla que contiene todas las url permitidas en la aplicacion
urls = (  
    '/habi', 'Habi'
    )
#carga las url al framework que nos permitira que se puedan consumir los 
#datos desde cualquier api
app = web.application(urls, globals())  

class Habi:  
      """Definición de clase que se cargara cuando el usuario consuma los datos"""

      def verifica_estado(self, idinmueble, filtro_estado): 
          """funcion para controlar los estados que puede visualizar el 
             usuario y adicional, devolver el nombre del estado"""

          #defino consulta mysql para obtener información del estado
          #del inmueble permitido y el nombre del estado a partir 
          #del id del inmueble
          query = "SELECT status_history.status_id, status.name\
                   FROM status_history INNER JOIN status ON \
                   status_history.status_id = status.id WHERE \
                   status_history.property_id = '%s' ORDER BY update_date \
                   DESC LIMIT 1"%idinmueble
          #capturo respuesta de la consulta en variable tipo lista
          resultado = consultabd(query)
          #controlo que la respuesta de la consulta tenga información
          #de lo contrario no se moestrará información del inmueble
          if len(resultado) > 0: 
             id_estado = resultado[0][0]
             nombre_estado = resultado[0][1]
             #evalua los id de los estados permitidos que son 3 pre_venta,
             #4 en_venta y 5 vendido
             if id_estado == 3 or id_estado == 4 or id_estado == 5:  
                #controlo que filtre estados especificos solicitados por el usuario
                if filtro_estado != "":  
                   if nombre_estado == filtro_estado:
                      return nombre_estado #retorno del nombre del estado
                   else:
                      return "N"
                else:
                   return nombre_estado
             else:
                return "N"
          else:
             return "N"
          
      def GET(self):
          """función GET que se carga cuando el usuario envia
             una solicitud tipo get"""

        #defino propiedades del header de mi aplicación
          web.header('Access-Control-Allow-Origin', '*')
          web.header('Access-Control-Allow-Methods', 
                     'GET, POST, OPTIONS, PUT, PATCH, DELETE')
          web.header('Access-Control-Allow-Headers', 
                     'X-Requested-With,content-type')
          web.header('Content-type', 'text/json', 'charset=iso-8859-1')
        #---------------------------------------------------------------------#
          #Defino variable varhtml que recibe todos los posibles filtros desde
          #dónde se quieran consumir los datos
          varhtml = web.input()  
          #defino consulta sql que listara información general de los 
          #inmuebles y si por algún motivo encuentro que viene un filtro, 
          #esta consulta sql cambia mas abajo
          query = "SELECT * FROM property" 
          #En la consulta de la aplicación, se pueden o no enviar los datos 
          #del filtro, en caso de que no se envíen, con esta condición el 
          #programa no genera error
          try:   
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
          #verifico si vienen datos para filtrar y con esto genero una 
          #nueva consulta
          if year != "":  
             query = "SELECT * FROM property WHERE year = '%s'"%year 
          if city != "":
             query = "SELECT * FROM property WHERE city = '%s'"%city  
          #controlo si viene mas de un filtro para crear una nueva sentencia mysql
          if city != "" and year != "":  
             query = "SELECT * FROM property WHERE year = '%s' \
                      AND city = '%s'"%(year, city)
          #llamo a la función consultadb pasando un sentencia mysql tipo
          #consulta y la respuesta la capturo en la variable resultado
          resultado = consultabd(query) 
          #Evaluo si se tiene conexión a la base de datos
          if resultado == "conexion0":  
             return "Sin Conexion a base de datos"
          #inicializo variable listado para agregar la información  
          #de la consulta
          listado = []
          #if que controla que la consulta si tiene información
          if len(resultado) > 0:  
             #for que recorre los datos de la consulta 1 a 1
             for data in resultado:  
                 idinmueble = data[0]
                 nombre_estado = self.verifica_estado(idinmueble, state)  
                 #si el nombre del estado no es igual a N, significa que es un
                 #estado permitido
                 if nombre_estado != "N":  
                    direccion = data[1]
                    ciudad = data[2]
                    precio = data[3]
                    descripcion = data[4]
                    anio = data[5]
                    #agrego los datos a la lista
                    listado.append({"id": idinmueble, "address": direccion, 
                                   "city": ciudad, "state": nombre_estado, 
                                   "price": precio, "description": descripcion})
          #retorno los datos de la consulta a la api rest
          #con su respectivo formato json
          return json.dumps(listado)  

def consultabd(query): 
    """funcion que recibe el código para hacer una consulta a la base de 
       datos y devolver un resultado"""
    #variables de conexión a base de datos
    db_user = "pruebas"  
    db_pass = "VGbt3Day5R"
    db_name = "habi_db" 
    db_host = "3.130.126.210" 
    try:
       #parametros para establecer conexión a la base de datos
       db = pymysql.connect(host=db_host, user=db_user, password=db_pass, 
                            db=db_name, port=3309)
    except:
       #si no tenemos respuesta de la base de datos, avisaremos con este mensaje
       return "conexion0"
    #establecemos conexión a la base de datos
    cursor = db.cursor()   
    #ejecutamos la sentencia en la base de datos
    cursor.execute(query) 
    #obtenemos todos los datos de la consulta
    resultado = cursor.fetchall()  
    #cerramos la consexión que hicimos a la base de datos
    cursor.close()   
    #Retornamos el valor de la consulta de la base de datos
    return resultado  

def main():  
    #función para evaluar los estado del framework
    web.internalerror = web.debugerror
    app.run()
    return 0

if __name__ == '__main__':
    #arrancamos la aplicación para que quede en línea
    app.run()   
