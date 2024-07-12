from flask import session
from conexionBD import * 

def listaProvincias():
    conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
    mycursor       = conexion_MySQLdb.cursor(dictionary=True)
    querySQL  = ("SELECT * FROM provincia")
    mycursor.execute(querySQL)
    provincias = mycursor.fetchall() #fetchall () Obtener todos los registros
    mycursor.close() #cerrrando conexion SQL
    conexion_MySQLdb.close() #cerrando conexion de la BD
    return provincias


def dataLoginSesion():
    inforLogin = {
        "idLogin"             :session['id'],
        "tipoLogin"           :session['tipo_user'],
        "nombre"              :session['nombre'],
        "apellido"            :session['apellido'],
        "fecha_nacimiento"    :session['fecha_nacimiento'],
        "direccion"           :session['direccion'],
        "telefono"           :session['telefono'],
        "provincia"           :session['provincia'],
        "sexo"                :session['sexo'],
        "emailLogin"          :session['email'],
        "create_at"           :session['create_at']      
    }
    return inforLogin