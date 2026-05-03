import os
import re
from flask import Flask, render_template, request, jsonify
from modelos import db, Vehiculo, Espacio, Movimiento
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN ---
db_uri = os.getenv('DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/bde_tc'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- INICIALIZACIÓN ---
with app.app_context():
    db.create_all()
    # Sincronizamos a 30 cocheras si la base está vacía o incompleta
    if Espacio.query.count() != 30:
        Movimiento.query.delete() 
        Espacio.query.delete()
        for i in range(1, 31): 
            db.session.add(Espacio(numero=f"Cochera {i}", estado="libre", patente=None))
        db.session.commit()

# --- LÓGICA DE TARIFAS ---
def calcular_tarifa_avanzada(fecha_ingreso, fecha_egreso):
    diferencia = fecha_egreso - fecha_ingreso
    # Mínimo cobramos 1 hora para evitar montos en $0 al inicio
    horas_totales = max(1, diferencia.total_seconds() / 3600)
    tarifa_base = int(os.getenv('TARIF_POR_HORA', 500))
    
    hora_entrada = fecha_ingreso.hour
    es_hora_pico = (8 <= hora_entrada <= 12) or (17 <= hora_entrada <= 21)
    
    precio_hora = tarifa_base * 1.5 if es_hora_pico else tarifa_base
    detalle = "Tarifa Especial (Hora Pico)" if es_hora_pico else "Tarifa Estándar"
    
    return round(horas_totales * precio_hora, 2), round(horas_totales, 2), detalle

# --- RUTAS DE NAVEGACIÓN ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrar')
def vista_registro():
    return render_template('ingreso.html')

@app.route('/admin')
def vista_admin():
    return render_template('admin.html')

# --- ENDPOINTS API ---

@app.route('/espacios', methods=['GET'])
def listar_espacios():
    espacios = Espacio.query.all()
    resultado = []
    ahora = datetime.now()
    
    for e in espacios:
        tiempo_display = "00:00 hs"
        monto_calculado = 0
        patente_display = e.patente if e.patente else "Libre"
        
        if e.estado == 'ocupado':
            # Buscamos el movimiento activo (sin fecha de egreso)
            mov = Movimiento.query.filter_by(espacio_id=e.id, fecha_egreso=None).first()
            if mov:
                # Aseguramos que la patente mostrada sea la del movimiento
                patente_display = mov.patente_vehiculo 
                
                # Cálculo de tiempo transcurrido
                diff = ahora - mov.fecha_ingreso
                hs, resto = divmod(diff.total_seconds(), 3600)
                mins, _ = divmod(resto, 60)
                tiempo_display = f"{int(hs):02d}:{int(mins):02d} hs"
                
                try:
                    total, _, _ = calcular_tarifa_avanzada(mov.fecha_ingreso, ahora)
                    monto_calculado = total
                except:
                    monto_calculado = 0
            else:
                patente_display = "Pendiente..."

        resultado.append({
            "id": e.id,
            "numero": e.numero,
            "estado": e.estado,
            "patente": patente_display,
            "tiempo": tiempo_display,
            "monto": monto_calculado
        })
    return jsonify(resultado), 200

@app.route('/ingreso', methods=['POST'])
def registrar_ingreso():
    # Detectar origen de datos (JSON o Formulario)
    if request.is_json:
        datos = request.get_json()
        patente_raw = datos.get('patente', '')
        id_cochera = datos.get('espacio_id') or datos.get('cochera')
    else:
        patente_raw = request.form.get('patente', '')
        id_cochera = request.form.get('cochera')

    if not patente_raw or not id_cochera:
        return jsonify({"error": "Faltan datos obligatorios."}), 400

    # Limpieza de patente
    patente = re.sub(r'[^A-Z0-9]', '', patente_raw.upper())
    
    # Búsqueda flexible: por ID, por nombre exacto o por número solo
    espacio = Espacio.query.filter(
        (Espacio.id == id_cochera) | 
        (Espacio.numero == id_cochera) | 
        (Espacio.numero == f"Cochera {id_cochera}")
    ).first()

    if not espacio:
        return jsonify({"error": f"La cochera '{id_cochera}' no existe."}), 404

    if espacio.estado != 'libre':
        return jsonify({"error": f"La {espacio.numero} ya está ocupada."}), 400

    # Registrar vehículo si es la primera vez que viene
    vehiculo = Vehiculo.query.get(patente)
    if not vehiculo:
        vehiculo = Vehiculo(patente=patente, marca="Genérico", modelo="Genérico")
        db.session.add(vehiculo)

    # Actualizar estado de la cochera y crear el movimiento de tiempo
    espacio.estado = 'ocupado'
    espacio.patente = patente
    
    nuevo_movimiento = Movimiento(
        patente_vehiculo=patente, 
        espacio_id=espacio.id, 
        fecha_ingreso=datetime.now()
    )
    
    db.session.add(nuevo_movimiento)
    db.session.commit()
    
    return jsonify({"mensaje": "Ingreso registrado con éxito", "patente": patente}), 201

@app.route('/egreso/<int:espacio_id>', methods=['POST'])
def registrar_egreso(espacio_id):
    mov = Movimiento.query.filter_by(espacio_id=espacio_id, fecha_egreso=None).first()
    if not mov:
        return jsonify({"error": "No hay un vehículo activo en esta cochera."}), 404

    mov.fecha_egreso = datetime.now()
    total, horas, desc = calcular_tarifa_avanzada(mov.fecha_ingreso, mov.fecha_egreso)
    
    mov.monto_total = total
    espacio = Espacio.query.get(espacio_id)
    espacio.estado = 'libre'
    espacio.patente = None
    
    db.session.commit()
    return jsonify({"mensaje": "Salida exitosa", "total": total, "detalle": desc}), 200

@app.route('/admin/reset', methods=['POST'])
def reset_sistema():
    Movimiento.query.delete()
    Espacio.query.delete()
    for i in range(1, 31):
        db.session.add(Espacio(numero=f"Cochera {i}", estado="libre", patente=None))
    db.session.commit()
    return jsonify({"mensaje": "Sistema reiniciado a cero correctamente."}), 200

if __name__ == '__main__':
    puerto = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=True, port=puerto)