from flask import Flask, request, jsonify
from modelos import db, Vehiculo, Espacio, Movimiento
from datetime import datetime

app = Flask(__name__)

# Configuración de tu base de datos (Puerto 3307 y base bde_tc)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/bde_tc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Esto crea las tablas automáticamente al iniciar
with app.app_context():
    db.create_all()
    # Cargamos 5 cocheras iniciales si la tabla está vacía
    if Espacio.query.count() == 0:
        for i in range(1, 6):
            db.session.add(Espacio(numero=f"Cochera {i}", estado="libre"))
        db.session.commit()
        print("¡Tablas de estacionamiento creadas y cocheras listas!")

@app.route('/')
def home():
    return {"mensaje": "Bienvenido al Sistema de Estacionamiento de la Facu"}, 200

# ENDPOINT INDIVIDUAL: Listar espacios
@app.route('/espacios', methods=['GET'])
def listar_espacios():
    espacios = Espacio.query.all()
    lista = [{"id": e.id, "numero": e.numero, "estado": e.estado} for e in espacios]
    return jsonify(lista), 200

# REGISTRAR INGRESO (POST)
@app.route('/ingreso', methods=['POST'])
def registrar_ingreso():
    datos = request.get_json()
    patente = datos.get('patente')
    marca = datos.get('marca')
    modelo = datos.get('modelo')
    id_espacio = datos.get('espacio_id')

    # 1. Verificar si el vehículo ya existe, si no, crearlo
    vehiculo = Vehiculo.query.get(patente)
    if not vehiculo:
        vehiculo = Vehiculo(patente=patente, marca=marca, modelo=modelo)
        db.session.add(vehiculo)

    # 2. Verificar si el espacio está libre
    espacio = Espacio.query.get(id_espacio)
    if not espacio or espacio.estado != 'libre':
        return jsonify({"error": "Espacio no disponible o inexistente"}), 400

    # 3. Registrar el movimiento y ocupar el espacio
    nuevo_movimiento = Movimiento(patente_vehiculo=patente, espacio_id=id_espacio)
    espacio.estado = 'ocupado'
    
    db.session.add(nuevo_movimiento)
    db.session.commit()

    return jsonify({"mensaje": f"Ingreso registrado: {patente} en {espacio.numero}"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)