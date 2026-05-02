from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    patente = db.Column(db.String(10), primary_key=True)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    movimientos = db.relationship('Movimiento', backref='vehiculo', lazy=True)

class Espacio(db.Model):
    __tablename__ = 'espacios'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    estado = db.Column(db.String(20), default='libre')

class Movimiento(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    patente_vehiculo = db.Column(db.String(10), db.ForeignKey('vehiculos.patente'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now)
    fecha_egreso = db.Column(db.DateTime, nullable=True)
    monto_total = db.Column(db.Float, default=0.0)