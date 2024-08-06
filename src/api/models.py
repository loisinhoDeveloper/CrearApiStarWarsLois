from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()




class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellidos = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(80), unique=False , nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    # Relaciones de uno a muchos con Favoritos
    favoritos = db.relationship('Favoritos', back_populates='usuario') # indicando que un usuario puede tener múltiples registros de favoritos.


    # def __init__(self, email, password):__init__ se utiliza para cambiar la forma de creara el objeto Usuario
    #     self.email=email
    #     self.password=password,
    #     self.is_active=True

    def __repr__(self): #Se utiliza para obtener una representación legible del objeto. información es más útil para identificar el objeto
        return f'< El Usuario tiene este {self.email}>'

    def serialize(self): #Lenguaje intermediario JSON. Convierte los atributos del objeto Usuario en un diccionario, formato que puede ser fácilmente convertido a JSON, útil para respuestas de API
        return {
            "id": self.id,
            "username": self.username,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "is_active": self.is_active,
            # No serializar la contraseña, es una brecha de seguridad
        }
    
class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=True)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)  # Campo para manejar el estado del favorito (activado o desactivado en routes.py )

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='favoritos')
    vehiculo = db.relationship('Vehiculos', back_populates='favoritos', foreign_keys=[vehiculo_id])
    personaje = db.relationship('Personajes', back_populates='favoritos', foreign_keys=[personaje_id])
    planeta = db.relationship('Planetas', back_populates='favoritos', foreign_keys=[planeta_id])

    
    def __repr__(self):#Se utiliza para obtener una representación legible del objeto. información es más útil para identificar el objeto
        return f'<Favoritos {self.id}>'

    def serialize(self): #Lenguaje intermediario JSON. Convierte los atributos del objeto Usuario en un diccionario, formato que puede ser fácilmente convertido a JSON, útil para respuestas de API
        return {
            "id": self.id,
            "vehiculo_id": self.vehiculo_id,
            "personaje_id": self.personaje_id,
            "planeta_id": self.planeta_id,
            "usuario_id": self.usuario_id,
            'activo': self.activo,
        }



class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False, unique=True) 
    apellidos = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.Enum('hombre', 'mujer', 'desconocido', name='genero_tipo'))
    nacimiento = db.Column(db.Date, nullable=False)
    altura = db.Column(db.Integer)
    peso = db.Column(db.Integer)
    color_pelo = db.Column(db.String(50))
    color_ojos = db.Column(db.String(50))
    
    # Relaciones de uno a muchos con Favoritos
    favoritos = db.relationship('Favoritos', back_populates='personaje', foreign_keys=[Favoritos.personaje_id])


    def __repr__(self):
        return f'<Personajes {self.id} {self.nombre} {self.apellidos}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "genero": self.genero,
            "nacimiento": self.nacimiento.isoformat(), #isoformat() se usa para convertir un objeto de fecha (datetime.date) a una cadena en el formato ISO 8601, para representar fechas y horas
            "altura": self.altura,
            "peso": self.peso,
            "color_pelo": self.color_pelo,
            "color_ojos": self.color_ojos,
        }

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False, unique=True)
    temperatura = db.Column(db.String(200))
    diametro = db.Column(db.Integer)
    gravedad = db.Column(db.Integer)
    poblacion = db.Column(db.Integer)
    terreno = db.Column(db.String(250))
    superficie_agua = db.Column(db.Integer)
    descripcion = db.Column(db.String(2000))
    # indica que un planeta puede aparecer en múltiples registros de la tabla Favoritos. 
    # Ejemplo desde una perspectiva de db.Model de datos: un mismo planeta puede estar en la lista de favoritos de diferentes usuarios, pero cada usuario verá solo sus propios favoritos.
    #favoritos = db.relationship('Favoritos', back_populates='planetas')

    # Relaciones de uno a muchos con Favoritos
    favoritos = db.relationship('Favoritos', back_populates='planeta', foreign_keys=[Favoritos.planeta_id])

    def __repr__(self): #ID y el nombre del planeta, lo que puede ser útil para identificar rápidamente en los registros o la consola.
        return f'<Planetas {self.id} {self.nombre} >'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "temperatura": self.temperatura,
            "diametro": self.diametro,
            "gravedad": self.gravedad, 
            "poblacion": self.poblacion,
            "terreno": self.terreno,
            "superficie_agua": self.superficie_agua,
            "descripcion": self.descripcion,
        }

class Vehiculos(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False, unique=True)
    tipo_vehiculo = db.Column(db.String(200))
    fabricante = db.Column(db.String(200))
    precio = db.Column(db.String(200))
    longitud = db.Column(db.Float)
    pilotos = db.Column(db.Integer)
    pasajeros = db.Column(db.Integer)
    velocidad = db.Column(db.Integer)
    capacidad = db.Column(db.Integer)
    consumibles = db.Column(db.Integer)
    descripcion = db.Column(db.String(2000))
    
    # Relaciones de uno a muchos con Favoritos
    favoritos = db.relationship('Favoritos', back_populates='vehiculos', foreign_keys=[Favoritos.vehiculo_id])

    def __repr__(self):
        return f'<Vehiculos {self.id} {self.nombre} >'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo_vehiculo": self.tipo_vehiculo,
            "fabricante": self.fabricante,
            "precio": self.precio,
            "longitud": self.longitud,
            "pilotos": self.pilotos,
            "pasajeros": self.pasajeros,
            "velocidad": self.velocidad,
            "capacidad": self.capacidad,
            "consumibles": self.consumibles,
            "descripcion": self.descripcion,
        }

def to_dict(self):
    return {}



