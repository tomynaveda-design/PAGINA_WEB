from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    patente = db.Column(db.String(10), primary_key=True)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    movimientos_rel = db.relationship('Movimiento', backref='vehiculo_ref', lazy=True)

class Espacio(db.Model):
    __tablename__ = 'espacios'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    estado = db.Column(db.String(20), default='libre')
    patente = db.Column(db.String(10), nullable=True)
    movimientos_rel = db.relationship('Movimiento', backref='espacio_ref', lazy=True)

class Movimiento(db.Model):
    __tablename__ = 'movimientos'
    id = db.Column(db.Integer, primary_key=True)
    patente_vehiculo = db.Column(db.String(10), db.ForeignKey('vehiculos.patente', ondelete='CASCADE'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id', ondelete='CASCADE'), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now)
    fecha_egreso = db.Column(db.DateTime, nullable=True)
    monto_total = db.Column(db.Float, default=0.0)

class Tarifa(db.Model):
    __tablename__ = 'tarifas'
    id = db.Column(db.Integer, primary_key=True)
    tipo_vehiculo = db.Column(db.String(50), default='Estandar')
    valor_hora = db.Column(db.Float, nullable=False)