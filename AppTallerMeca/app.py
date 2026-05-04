import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from modelos import db, Vehiculo, Espacio, Movimiento, Tarifa
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'smartpark_2026_key' # Clave para mensajes flash

# --- CONFIGURACIÓN DE BASE DE DATOS ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bde_tc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- INICIALIZACIÓN DE DATOS ---
with app.app_context():
    db.create_all()
    
    # Sincronización de las 30 cocheras
    if Espacio.query.count() != 30:
        Movimiento.query.delete() 
        Espacio.query.delete()
        for i in range(1, 31): 
            db.session.add(Espacio(numero=f"Cochera {i}", estado="libre", patente=None))
        db.session.commit()
    
    # Crear tarifa inicial si la tabla está vacía
    if Tarifa.query.count() == 0:
        db.session.add(Tarifa(valor_hora=1000.0))
        db.session.commit()

# --- LÓGICA DE CÁLCULO ---
def calcular_tarifa_avanzada(fecha_ingreso, fecha_egreso):
    diferencia = fecha_egreso - fecha_ingreso
    horas = max(1, diferencia.total_seconds() / 3600)
    
    tarifa_db = Tarifa.query.first()
    precio_base = tarifa_db.valor_hora if tarifa_db else 1000.0
    
    return round(horas * precio_base, 2), round(horas, 2)

# --- RUTAS DEL SISTEMA ---

@app.route('/')
def home():
    tarifa_actual = Tarifa.query.first()
    return render_template('index.html', tarifa=tarifa_actual)

@app.route('/registrar')
def vista_registro():
    return render_template('ingreso.html')

@app.route('/actualizar_tarifa', methods=['POST'])
def actualizar_tarifa():
    nuevo_valor = request.form.get('nuevo_valor')
    if nuevo_valor:
        tarifa = Tarifa.query.first()
        if tarifa:
            tarifa.valor_hora = float(nuevo_valor)
        else:
            db.session.add(Tarifa(valor_hora=float(nuevo_valor)))
        db.session.commit()
        flash(f"Tarifa actualizada correctamente a ${nuevo_valor}")
    return redirect(url_for('home'))

@app.route('/ingreso', methods=['POST'])
def registrar_ingreso():
    # Soporte híbrido: JSON (fetch) o Formulario tradicional
    if request.is_json:
        data = request.get_json()
        patente_raw = data.get('patente', '')
        id_cochera = data.get('espacio_id')
    else:
        patente_raw = request.form.get('patente', '')
        id_cochera = request.form.get('espacio_id') or request.form.get('cochera')

    # Validar datos mínimos
    if not patente_raw or not id_cochera:
        error_msg = "Datos incompletos."
        return jsonify({"error": error_msg}) if request.is_json else (flash(error_msg), redirect(url_for('home')))[1]

    # Limpiar patente (mayúsculas y sin caracteres raros)
    patente = re.sub(r'[^A-Z0-9]', '', patente_raw.upper())
    
    # 1. BLOQUEO: Verificar si el vehículo ya está en el sistema
    ya_esta = Movimiento.query.filter_by(patente_vehiculo=patente, fecha_egreso=None).first()
    if ya_esta:
        error_msg = f"El vehículo {patente} ya posee un ingreso activo."
        return jsonify({"error": error_msg}) if request.is_json else (flash(error_msg), redirect(url_for('home')))[1]

    # 2. Verificar disponibilidad de la cochera
    espacio = Espacio.query.get(int(id_cochera))
    if not espacio or espacio.estado != 'libre':
        error_msg = "Cochera no disponible."
        return jsonify({"error": error_msg}) if request.is_json else (flash(error_msg), redirect(url_for('home')))[1]

    # 3. Registrar en base de datos
    if not Vehiculo.query.get(patente):
        db.session.add(Vehiculo(patente=patente, marca="Genérico"))

    espacio.estado = 'ocupado'
    espacio.patente = patente
    
    nuevo_mov = Movimiento(patente_vehiculo=patente, espacio_id=espacio.id, fecha_ingreso=datetime.now())
    db.session.add(nuevo_mov)
    db.session.commit()
    
    res_msg = f"Ingreso exitoso: {patente} en {espacio.numero}"
    if request.is_json:
        return jsonify({"mensaje": res_msg})
    else:
        flash(res_msg)
        return redirect(url_for('home'))

@app.route('/espacios')
def listar_espacios():
    espacios = Espacio.query.all()
    resultado = []
    
    for e in espacios:
        fecha_iso = None
        if e.estado == 'ocupado':
            mov = Movimiento.query.filter_by(espacio_id=e.id, fecha_egreso=None).first()
            if mov:
                # Enviamos la fecha en formato ISO para que JavaScript la reconozca
                fecha_iso = mov.fecha_ingreso.isoformat()
        
        resultado.append({
            "id": e.id,
            "numero": e.numero,
            "estado": e.estado,
            "patente": e.patente or "Libre",
            "fecha_ingreso": fecha_iso # Nuevo campo
        })
    return jsonify(resultado)

@app.route('/egreso/<int:espacio_id>', methods=['POST'])
def registrar_egreso(espacio_id):
    mov = Movimiento.query.filter_by(espacio_id=espacio_id, fecha_egreso=None).first()
    if not mov:
        return jsonify({"error": "No se encontró un vehículo en esta cochera"}), 404

    mov.fecha_egreso = datetime.now()
    total, _ = calcular_tarifa_avanzada(mov.fecha_ingreso, mov.fecha_egreso)
    mov.monto_total = total
    
    espacio = Espacio.query.get(espacio_id)
    espacio.estado = 'libre'
    espacio.patente = None
    
    db.session.commit()
    return jsonify({"mensaje": "Egreso procesado", "total": total})

if __name__ == '__main__':
    app.run(debug=True, port=5000)