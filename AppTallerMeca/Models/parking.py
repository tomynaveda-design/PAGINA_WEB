from .db import db

class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), nullable=False)
    modelo = db.Column(db.String(50)) # Para saber qué auto es
    ocupado = db.Column(db.Boolean, default=False) # Para saber si está en el garage