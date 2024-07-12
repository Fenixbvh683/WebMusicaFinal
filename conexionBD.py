#Importando Libreria mysql.connector para conectar Python con MySQL
# conexionBD.py
import mysql.connector
from mysql.connector import Error
from config import config

def connectionBD():
    try:
        connection = mysql.connector.connect(
            host=config['development'].MYSQL_HOST,
            user=config['development'].MYSQL_USER,
            password=config['development'].MYSQL_PASSWORD,
            database=config['development'].MYSQL_DB
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None