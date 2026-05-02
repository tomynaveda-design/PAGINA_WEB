from flask import Blueprint, jsonify
from Models.db import db
from Models.parking import Vehiculo

# Mantenemos tu Blueprint
products_bp = Blueprint('products', __name__)

@products_bp.route('/productos')
def listar_productos():
    # En vez de un texto, traemos los autos reales de la base bde_tc
    autos = Vehiculo.query.all()
    
    # Lo convertimos a una lista para que se vea como datos profesionales (JSON)
    lista_autos = []
    for auto in autos:
        lista_autos.append({
            "id": auto.id,
            "patente": auto.patente,
            "modelo": auto.modelo
        })
    
    return jsonify(lista_autos)

@products_bp.route('/cargar/<patente>/<modelo>')
def cargar_auto(patente, modelo):
    try:
        # Esta ruta permite cargar datos desde el link, como en el ejemplo de tu compañera
        nuevo = Vehiculo(patente=patente, modelo=modelo)
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"estado": "Guardado", "auto": patente})
    except Exception as e:
        return jsonify({"error": str(e)})