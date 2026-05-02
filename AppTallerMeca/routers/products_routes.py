from flask import Blueprint, render_template, request, redirect, session
from Models.db import db
from Models.parking import Vehiculo, Usuario

products_bp = Blueprint('products', __name__)

# --- 1. HOME (PROTEGIDA) ---
@products_bp.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    autos_db = Vehiculo.query.all()
    usuarios_db = Usuario.query.all()
    
    return render_template('index.html', 
                         lista_autos=autos_db, 
                         lista_usuarios=usuarios_db,
                         nombre_usuario=session.get('usuario_nombre'))

# --- 2. LOGIN ---
@products_bp.route('/login')
def vista_login():
    return render_template('login.html')

@products_bp.route('/login-proceso', methods=['POST'])
def login_proceso():
    # .strip() elimina espacios invisibles que a veces causan error
    ema = request.form.get('email', '').strip()
    pas = request.form.get('password', '').strip()
    
    usuario_encontrado = Usuario.query.filter_by(email=ema, password=pas).first()
    
    if usuario_encontrado:
        session['usuario_id'] = usuario_encontrado.id
        session['usuario_nombre'] = usuario_encontrado.nombre
        return redirect('/')
    else:
        return "Email o contraseña incorrectos. <a href='/login'>Volver a intentar</a>"

# --- 3. REGISTRO (LA CLAVE PARA EVITAR LOS NULLS) ---
@products_bp.route('/registro')
def vista_registro():
    return render_template('registro.html')

@products_bp.route('/registrar-usuario', methods=['POST'])
def registrar_usuario():
    # Obtenemos los datos asegurándonos de que no sean None
    nom = request.form.get('nombre', '').strip()
    ema = request.form.get('email', '').strip()
    pas = request.form.get('password', '').strip()
    
    # Solo intentamos guardar si el usuario escribió algo en los 3 campos
    if nom and ema and pas:
        nuevo_user = Usuario(nombre=nom, email=ema, password=pas)
        try:
            db.session.add(nuevo_user)
            db.session.commit()
            # Al terminar de registrar, lo mandamos al login para que entre oficialmente
            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar en la base de datos: {e}"
    else:
        return "Error: Todos los campos son obligatorios. <a href='/registro'>Volver a intentar</a>"

# --- 4. LOGOUT ---
@products_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# --- 5. VEHÍCULOS ---
@products_bp.route('/guardar', methods=['POST'])
def guardar():
    if 'usuario_id' not in session:
        return redirect('/login')
        
    patente_f = request.form.get('patente')
    modelo_f = request.form.get('modelo')
    
    nuevo_vehiculo = Vehiculo(patente=patente_f, modelo=modelo_f)
    
    try:
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        db.session.rollback()
        return f"Error al guardar auto: {e}"