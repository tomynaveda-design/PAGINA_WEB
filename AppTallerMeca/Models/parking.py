from .db import db

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), nullable=False)
    modelo = db.Column(db.String(50))
    ocupado = db.Column(db.Boolean, default=False)

# CLASE SEPARADA (Sin espacios extra a la izquierda)
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)