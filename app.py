# imports
from flask import Flask, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask_cors import CORS

import mysql.connector

from funciones import listaProvincias  
from config import config
from conexionBD import connectionBD

import os
import time


# application init
app = Flask(__name__)
app.config.from_object(config['development'])
app.secret_key = config['development'].SECRET_KEY

CORS(app)

# Ruta para la página principal
@app.route('/')
def home():
    return app.send_static_file('home.html')

@app.route('/productos_music')
def productos_music():
    return app.send_static_file('productos_music.html')


@app.route('/contacto')
def contacto():
    return app.send_static_file('contacto.html')


@app.route('/registro_usuarios')
def registro_usuarios():
    return app.send_static_file('registro_usuarios.html')



#--------------------------------------------------------------------------------
def agregar_producto_db(idgenero, nombre, album, anio, descripcion, imagen, precio):
    connection = connectionBD()
    if connection is None:
        return None

    try:
        cursor = connection.cursor()
        sql = "INSERT INTO productos (idgenero, nombre, album, anio, descripcion, imagen, precio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (idgenero, nombre, album, anio, descripcion, imagen, precio)
        
        cursor.execute(sql, valores)
        connection.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#--------------------------------------------------------------------------------
def consultar_producto_db(id):
    try:
        connection = connectionBD()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        sql = "SELECT * FROM productos WHERE id = %s"
        cursor.execute(sql, (id,))
        
        producto = cursor.fetchone()
        return producto
    except mysql.connector.Error as e:
        print(f"Error al consultar el producto: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

#--------------------------------------------------------------------------------
def modificar_producto_db(id, nuevo_idgenero, nuevo_nombre, nuevo_album, nuevo_anio, nueva_descripcion, nuevo_imagen, nuevo_precio):
    try:                  
        connection = connectionBD()
        if connection is None:
            return False
        
        cursor = connection.cursor()

        sql = "UPDATE productos SET idgenero = %s, nombre = %s, album = %s, anio = %s, descripcion = %s, imagen = %s, precio = %s WHERE id = %s"
        valores = (nuevo_idgenero, nuevo_nombre, nuevo_album, nuevo_anio, nueva_descripcion, nuevo_imagen, nuevo_precio, id)
        cursor.execute(sql, valores)
        connection.commit()

        # Verificar si se realizó la modificación
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        print(f"Error al modificar el producto: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

#--------------------------------------------------------------------------------
def listar_productos_db():
    try:
        connection = connectionBD()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        return productos
        
    except mysql.connector.Error as e:
        print(f"Error al listar productos: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

#--------------------------------------------------------------------------------
def eliminar_producto_bd(id):
    try:
        connection = connectionBD()
        if connection is None:
            return False
        
        cursor = connection.cursor(dictionary=True)
        sql = "DELETE FROM productos WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()

        # Verificar si se eliminó algún producto
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except mysql.connector.Error as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

#--------------------------------------------------------------------------------
def mostrar_producto(id):
    # Mostramos los datos de un producto a partir de su código
    producto = consultar_producto_db(id)
    if producto is not None:
        print("-" * 40)
        print(f"Código.....: {producto['id']}")
        print(f"Género: {producto['idgenero']}")
        print(f"Nombre...: {producto['nombre']}")
        print(f"Álbum.....: {producto['album']}")
        print(f"Año.....: {producto['anio']}")
        print(f"Descripción..: {producto['descripcion']}")
        print(f"Imagen..: {producto['imagen']}")
        print(f"Precio..: {producto['precio']}")
        print("-" * 40)
    else:
        print("Producto no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------

# Carpeta para guardar las imagenes
RUTA_DESTINO = './static/img/'

#--------------------------------------------------------------------
# Obtener todos los productos
#--------------------------------------------------------------------
@app.route("/productos", methods=["GET"])
def obtener_productos():
    try:
        productos = listar_productos_db()
        if productos is None:
            return jsonify({"message": "No se encontraron productos"}), 404
        else:
            return jsonify(productos)
    except Exception as e:
        return jsonify({"error": f"Error al obtener productos desde listar_productos metodo GET: {e}"}), 500

#--------------------------------------------------------------------
# Mostrar un sólo producto según su código
#--------------------------------------------------------------------
#La ruta Flask /productos/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un producto específico basado en su código.
#El método busca en la base de datos el producto con el código especificado y devuelve un JSON con los detalles del producto si lo encuentra, o None si no lo encuentra.
@app.route("/productos/<int:id>", methods=["GET"])
def mostrar_producto(id):
    try:
        producto = consultar_producto_db(id)
        if producto:
            return jsonify(producto), 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al consultar el producto desde mostrar_producto: {e}"}), 500


#--------------------------------------------------------------------
# Agregar un producto
#--------------------------------------------------------------------
@app.route("/productos", methods=["POST"])
#La ruta Flask `/productos` con el método HTTP POST está diseñada para permitir la adición de un nuevo producto a la base de datos.
#La función agregar_producto se asocia con esta URL y es llamada cuando se hace una solicitud POST a /productos.
def agregar_producto():
    try:
        # Recojo los datos del form
        idgenero = request.form['idgenero']
        nombre = request.form['nombre']
        album = request.form['album']
        anio = request.form['anio']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        precio = request.form['precio']
        
        # Genero el nombre de la imagen
        nombre_imagen = secure_filename(imagen.filename)
        nombre_base, extension = os.path.splitext(nombre_imagen)
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        
        # Agrego el producto a la base de datos
        nuevo_codigo = agregar_producto_db(idgenero, nombre, album, anio, descripcion, nombre_imagen, precio)
        
        if nuevo_codigo:
            imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
            print("Se guardo!")
            return jsonify({"mensaje": "Producto agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
        else:
            return jsonify({"mensaje": "Error al agregar el producto."}), 500
    except Exception as e:
        return jsonify({"error": f"Error al agregar el producto: {e}"}), 500


#--------------------------------------------------------------------
# Modificar un producto según su código
#--------------------------------------------------------------------
@app.route("/productos/<int:id>", methods=["PUT"])
#La ruta Flask /productos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un producto existente en la base de datos, identificado por su código.
#La función modificar_producto se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /productos/ seguido de un número (el código del producto).
def modificar_producto(id):
    #Se recuperan los nuevos datos del formulario
    nuevo_idgenero = request.form.get("genero")
    nuevo_nombre = request.form.get("nombre")
    nuevo_album = request.form.get("album")
    nuevo_anio = request.form.get("anio")
    nueva_descripcion = request.form.get("descripcion")
    nuevo_precio = request.form.get("precio")
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Buscar el producto guardado
        producto = consultar_producto_db(id)
        if producto: # Si existe el producto...
            imagen_vieja = producto["imagen"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si la imagen vieja existe, la borra
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del producto
        producto = consultar_producto_db(id)
        if producto:
            nombre_imagen = producto["imagen"]


    # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos.
    if modificar_producto_db(id, nuevo_idgenero, nuevo_nombre, nuevo_album, nuevo_anio, nueva_descripcion, nombre_imagen, nuevo_precio):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        #Si el producto no se encuentra (por ejemplo, si no hay ningún producto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Producto no encontrado"}), 404




#--------------------------------------------------------------------
# Eliminar un producto según su código (id)
#--------------------------------------------------------------------
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    try:
        # Intenta eliminar el producto de la base de datos
        if eliminar_producto_bd(id):
            # Consulta el producto para obtener la imagen y eliminarla del servidor
            producto = consultar_producto_db(id)
            if producto:
                imagen_vieja = producto["imagen"]
                ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

                if os.path.exists(ruta_imagen):
                    os.remove(ruta_imagen)

            # Retorna una respuesta JSON indicando éxito
            return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
        else:
            # Retorna una respuesta JSON si no se pudo eliminar el producto
            return jsonify({"mensaje": "Producto no encontrado"}), 404
    except Exception as e:
        # Captura cualquier error y devuelve una respuesta de error JSON
        return jsonify({"mensaje": f"Error al eliminar producto: {str(e)}"}), 500




#--------------------------------------------------------------------
#                     LOGIN
#--------------------------------------------------------------------



# Función para autenticar al usuario
def authenticate_user(email, password):
    try:
        connection = connectionBD()
        if connection is None:
            return False
        
        cursor = connection.cursor(dictionary=True)
        sql = "SELECT * FROM usuario WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        
        user = cursor.fetchone()
        if user:
            return user
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Error en la autenticación: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Función para obtener información del usuario autenticado
def get_user(user_id):
    try:
        connection = connectionBD()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        sql = "SELECT * FROM usuario WHERE id = %s"
        cursor.execute(sql, (user_id,))
        
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as e:
        print(f"Error al obtener usuario: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Autenticar al usuario
        user = authenticate_user(email, password)

        if user:
            # Guardar el usuario en la sesión
            session['user_id'] = user['id']
            return jsonify({"mensaje": "Login exitoso"}), 200
        else:
            return jsonify({"mensaje": "Error en la autenticación. Verifica tus credenciales."}), 401



# Ejemplo de ruta protegida
@app.route('/dashboard')
def dashboard():
    # Verificar si el usuario está autenticado
    if 'user_id' in session:
        user_id = session['user_id']
        # Obtener información del usuario desde la base de datos
        user = get_user(user_id)
        if user:
            return jsonify({"mensaje": "Bienvenido al dashboard", "usuario": user}), 200
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    else:
        return jsonify({"mensaje": "Acceso no autorizado. Debes iniciar sesión"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully."}), 200


#-------------------------------------------------------------------------
#run application
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()