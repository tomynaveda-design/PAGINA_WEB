from flask import Blueprint, render_template, request, redirect, session
# IMPORTANTE: Cambiamos las rutas de importación para que coincidan con tu proyecto actual
from modelos import db, Vehiculo, Espacio 
# Nota: Si no tenés una clase "Usuario" en modelos.py, el login va a fallar.
# Por ahora uso las que pasaste antes.

products_bp = Blueprint('products', __name__)

# --- 1. HOME (PROTEGIDA) ---
@products_bp.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    autos_db = Vehiculo.query.all()
    # Cambiamos la lógica para mostrar los espacios (cocheras) en lugar de usuarios
    espacios_db = Espacio.query.all()
    
    return render_template('index.html', 
                         lista_autos=autos_db, 
                         lista_espacios=espacios_db,
                         nombre_usuario=session.get('usuario_nombre'))

# --- 2. LOGIN ---
@products_bp.route('/login')
def vista_login():
    return render_template('login.html')

@products_bp.route('/login-proceso', methods=['POST'])
def login_proceso():
    ema = request.form.get('email', '').strip()
    pas = request.form.get('password', '').strip()
    
    # IMPORTANTE: Asegurate de tener la clase Usuario en tu modelos.py
    # Si no la tenés, esta parte va a tirar error.
    try:
        from modelos import Usuario
        usuario_encontrado = Usuario.query.filter_by(email=ema, password=pas).first()
        
        if usuario_encontrado:
            session['usuario_id'] = usuario_encontrado.id
            session['usuario_nombre'] = usuario_encontrado.nombre
            return redirect('/')
        else:
            return "Email o contraseña incorrectos. <a href='/login'>Volver a intentar</a>"
    except ImportError:
        return "Error: La tabla de Usuarios no está definida en modelos.py"

# --- 3. REGISTRO ---
@products_bp.route('/registro')
def vista_registro():
    return render_template('registro.html')

@products_bp.route('/registrar-usuario', methods=['POST'])
def registrar_usuario():
    nom = request.form.get('nombre', '').strip()
    ema = request.form.get('email', '').strip()
    pas = request.form.get('password', '').strip()
    
    if nom and ema and pas:
        try:
            from modelos import Usuario
            nuevo_user = Usuario(nombre=nom, email=ema, password=pas)
            db.session.add(nuevo_user)
            db.session.commit()
            return redirect('/login')
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar: {e}"
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
    
    # Ajustamos a los campos de tu clase Vehiculo en modelos.py
    nuevo_vehiculo = Vehiculo(patente=patente_f, modelo=modelo_f, marca="Genérico")
    
    try:
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        db.session.rollback()
        return f"Error al guardar auto: {e}"