from flask import Blueprint, render_template, request, redirect
from Models.db import db
from Models.parking import Vehiculo

# Definimos el Blueprint
products_bp = Blueprint('products', __name__)

# RUTA PRINCIPAL: Muestra el formulario y la tabla con datos
@products_bp.route('/')
def index():
    # Traemos todos los autos de la base de datos
    autos_db = Vehiculo.query.all()
    # Los mandamos al HTML
    return render_template('index.html', lista_autos=autos_db)

# RUTA DE GUARDADO: Recibe los datos del HTML y los mete en MySQL
@products_bp.route('/guardar', methods=['POST'])
def guardar():
    # Agarramos lo que el usuario escribió en las cajas de texto
    patente_f = request.form['patente']
    modelo_f = request.form['modelo']
    
    # Creamos el nuevo objeto vehículo
    nuevo_vehiculo = Vehiculo(patente=patente_f, modelo=modelo_f)
    
    try:
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        # Una vez guardado, volvemos a la página principal
        return redirect('/')
    except Exception as e:
        db.session.rollback()
        return f"Hubo un error al guardar: {e}"