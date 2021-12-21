from biblioteca import db
from flask_login import UserMixin

class Biblioteca (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(120))
    lugar = db.Column(db.String(120))
    libros = db.relationship('Libro', backref='biblioteca', lazy=True)


class Libro (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120))
    autor = db.Column(db.String(120))
    id_biblioteca = db.Column(db.Integer, db.ForeignKey('biblioteca.id'))
    ocupado = db.Column(db.Boolean)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Rol (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    roles = db.relationship('Usuario', backref='rol', lazy=True)


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ci = db.Column(db.String(10))
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    correo = db.Column(db.String(120))
    clave = db.Column(db.String(120))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    id_publico = db.Column(db.String(120))
    libros   = db.relationship('Libro', backref='usuario', lazy=True)
    computadoras = db.relationship('Computadora', backref='usuario', lazy=True)
    sillas = db.relationship('Silla', backref='usuario', lazy=True )

class Computadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer)
    os = db.Column(db.String(120))
    estado = db.Column(db.String(120))
    ocupado = db.Column(db.Boolean)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Silla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    ocupado = db.Column(db.Boolean)
    nombre =db.Column(db.String(120))
class Bitacora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    id_biblioteca = db.Column(db.Integer, db.ForeignKey('biblioteca.id'))
    fecha = db.Column(db.DateTime)

class Detalle_Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Detalle_Computadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    