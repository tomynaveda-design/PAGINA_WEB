import os
from flask import Flask, request, jsonify
from modelos import db, Vehiculo, Espacio, Movimiento
from datetime import datetime
from dotenv import load_dotenv

# Carga las variables del archivo
load_dotenv()

app = Flask(__name__)

# Si os.getenv falla, usa la ruta directa como respaldo
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/bde_tc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    if Espacio.query.count() == 0:
        for i in range(1, 6):
            db.session.add(Espacio(numero=f"Cochera {i}", estado="libre"))
        db.session.commit()

# --- ENDPOINTS ---

@app.route('/')
def home():
    return {"mensaje": "API Estacionamiento Autónomo Activa"}, 200

# 1. LISTAR ESPACIOS (GET /espacios)
@app.route('/espacios', methods=['GET'])
def listar_espacios():
    espacios = Espacio.query.all()
    return jsonify([{"id": e.id, "numero": e.numero, "estado": e.estado} for e in espacios]), 200

# 2. REGISTRAR INGRESO (POST /ingreso) - INCLUYE BONUS VALIDACIÓN
@app.route('/ingreso', methods=['POST'])
def registrar_ingreso():
    datos = request.get_json()
    patente = datos.get('patente')
    id_espacio = datos.get('espacio_id')

    # BONUS: Evitar doble ingreso
    movimiento_activo = Movimiento.query.filter_by(patente_vehiculo=patente, fecha_egreso=None).first()
    if movimiento_activo:
        return jsonify({"error": "El vehículo ya se encuentra en el estacionamiento"}), 400

    # Verificar si el vehículo existe, sino crearlo
    vehiculo = Vehiculo.query.get(patente)
    if not vehiculo:
        vehiculo = Vehiculo(patente=patente, marca=datos.get('marca'), modelo=datos.get('modelo'))
        db.session.add(vehiculo)

    # Ocupar espacio
    espacio = Espacio.query.get(id_espacio)
    if not espacio or espacio.estado != 'libre':
        return jsonify({"error": "Espacio no disponible"}), 400

    nuevo_movimiento = Movimiento(patente_vehiculo=patente, espacio_id=id_espacio)
    espacio.estado = 'ocupado'
    
    db.session.commit()
    return jsonify({"mensaje": "Ingreso registrado correctamente"}), 201

# 3. REGISTRAR EGRESO CON CÁLCULO (POST /egreso)
@app.route('/egreso/<int:movimiento_id>', methods=['POST'])
def registrar_egreso(movimiento_id):
    movimiento = Movimiento.query.get(movimiento_id)
    if not movimiento or movimiento.fecha_egreso:
        return jsonify({"error": "Movimiento no válido"}), 404

    movimiento.fecha_egreso = datetime.now()
    
    # CÁLCULO AUTOMÁTICO (Basado en el tiempo transcurrido)
    diferencia = movimiento.fecha_egreso - movimiento.fecha_ingreso
    horas = max(1, diferencia.total_seconds() / 3600) # Mínimo 1 hora
    tarifa_hora = int(os.getenv('TARIF_POR_HORA', 500))
    movimiento.monto_total = round(horas * tarifa_hora, 2)

    # Liberar espacio
    espacio = Espacio.query.get(movimiento.espacio_id)
    espacio.estado = 'libre'
    
    db.session.commit()
    return jsonify({
        "mensaje": "Egreso registrado",
        "tiempo_total_horas": round(horas, 2),
        "monto_a_pagar": movimiento.monto_total
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('FLASK_PORT', 5000))