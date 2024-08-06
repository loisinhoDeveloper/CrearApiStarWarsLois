"""
Este módulo se encarga de iniciar el servidor de API, cargar la base de datos y añadir los endpoints.
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Usuario, Favoritos, Planetas, Personajes, Vehiculos #importamos las tablas
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__) #Blueprint = es el culpable que se agregue /api a nuestras peticiones. Evita conflitos entre las rutas. Configuración específica de este proyecto.

# Allow CORS requests to this API
CORS(api)


# Ruta para obtener todos los personajes
@api.route('/personajes', methods=['GET'])
def lista_personajes():
    personajes = Personajes.query.all()
    return jsonify([personaje.serialize() for personaje in personajes]), 200

# Ruta para obtener un personaje por su ID
@api.route('/personajes/<int:id>', methods=['GET'])
def obtener_personaje(id):
    personaje = Personajes.query.get(id)
    if personaje:
        return jsonify(personaje.serialize()), 200
    return jsonify({'Mensaje': 'Personaje no encontrado'}), 404





# Ruta para obtener todos los planetas
@api.route('/planetas', methods=['GET'])
def lista_planetas():
    planetas = Planetas.query.all()
    return jsonify([p.serialize() for p in planetas]), 200

# Ruta para obtener un planeta por su ID
@api.route('/planetas/<int:id>', methods=['GET'])
def obtener_planeta(id):
    planeta = Planetas.query.get(id)
    if planeta:
        return jsonify(planeta.serialize()), 200
    return jsonify({'Mensaje': 'Planeta no encontrado'}), 404




@api.route('/vehiculos', methods=['GET'])
def lista_vehiculos():
    vehiculos = Vehiculos.query.all()
    return jsonify([v.serialize() for v in vehiculos]), 200

@api.route('/vehiculos/<int:id>', methods=['GET'])
def obtener_vehiculo(id):
    vehiculo = Vehiculos.query.get(id)
    if vehiculo:
        return jsonify(vehiculo.serialize()), 200
    return jsonify({'Mensaje': 'Vehículo no encontrado'}), 404




# Ruta para crear un nuevo usuario
@api.route('/usuarios', methods=['POST'])
def crear_usuarios():
    data = request.json

    # Verificar si 'email' y 'password' están en los datos recibidos
    if 'email' in data and 'password' in data:
        # Comprobar si ya existe un usuario con el mismo correo electrónico
        usuario = Usuario.query.filter_by(email=data['email']).first()

        # Si el usuario existe, devolver un mensaje de error
        if usuario:
            return jsonify({'Mensaje': 'El usuario ya existe, intentalo de nuevo'}), 200

        # Crear un nuevo usuario ya que el correo electrónico no existe
        usuario_nuevo = Usuario(email=data['email'], password=data['password'], is_active=True)
        db.session.add(usuario_nuevo)
        db.session.commit()
        return jsonify({'Mensaje': 'Registrada/o', 'usuario': usuario_nuevo.serialize()}), 201

    # Si no se proporcionan todos los datos, devolver un mensaje de error
    return jsonify({"Mensaje": "Todos los datos son necesarios"}), 400
  

# Ruta para gestionar un usuario por su ID (obtener o eliminar)
@api.route('/usuarios/<int:id>', methods=['GET', 'DELETE'])
def gestionar_usuario(id):
    if request.method == 'GET':
        usuario = Usuario.query.get(id)
        if usuario:
            return jsonify(usuario.serialize()), 200
        return jsonify({'Mensaje': 'Usuario no encontrado'}), 404

    if request.method == 'DELETE':
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'Mensaje': 'Usuario eliminado correctamente'}), 200
        return jsonify({'Mensaje': 'Usuario no encontrado'}), 404



# Ruta para activar un favorito
@api.route('/activar_favorito/<int:id>', methods=['POST'])
def activar_favorito(id):
    data = request.json # Obtener los datos enviados en la solicitud POST (en formato JSON)
    try:
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({"Mensaje": "Usuario no encontrado"}), 404

        # Validar si ya existe en los favoritos
        favorito = Favoritos.query.filter_by(usuario_id=id, vehiculo_id=data.get('vehiculo_id'), personaje_id=data.get('personaje_id'), planeta_id=data.get('planeta_id')).first()
        if favorito:
            return jsonify({"Mensaje": "Este elemento ya está en los favoritos"}), 400

# Crear un nuevo favorito
        favorito_nuevo = Favoritos(
            usuario_id=id,
            vehiculo_id=data.get('vehiculo_id'),
            personaje_id=data.get('personaje_id'),
            planeta_id=data.get('planeta_id')
        )
        db.session.add(favorito_nuevo)
        db.session.commit()
        return jsonify({"Mensaje": "Favorito añadido correctamente", "favorito": favorito_nuevo.serialize()}), 201

#Podría ponerse sin este bloque excepción.
    except Exception as e:
        db.session.rollback()
        return jsonify({"Mensaje": "Error al añadir favorito", "Error": str(e)}), 500 


# Ruta para desactivar un favorito
@api.route('/desactivar_favorito/<int:id>', methods=['DELETE'])
def desactivar_favorito(id):
    data = request.json
    try:
        favorito = Favoritos.query.filter_by(usuario_id=id, vehiculo_id=data.get('vehiculo_id'), personaje_id=data.get('personaje_id'), planeta_id=data.get('planeta_id')).first()
        if not favorito:
            return jsonify({"Mensaje": "Favorito no encontrado"}), 404

        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"Mensaje": "Favorito eliminado correctamente"}), 200

    except Exception as e: # Exception= clase base para todas las excepciones integradas en Python. Esta cláusula captura cualquier tipo de excepción que se produzca dentro del bloque try
        db.session.rollback() #Si ocurre un error durante la operación de la base de datos (en el bloque try). El rollback(), asegura que la base de datos regrese al estado anterior al error.
        return jsonify({"Mensaje": "Error al eliminar favorito", "Error": str(e)}), 500











