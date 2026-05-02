from flask import Flask
from config.config import Config
from Models.db import db
from routers.products_routes import products_bp

# 1. Creamos la aplicación
app = Flask(__name__)

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_super_segura' # AGREGÁ ESTO

# 2. Cargamos la configuración (puerto 3307, base bde_tc, etc.)
app.config.from_object(Config)

# 3. Inicializamos la base de datos
db.init_app(app)

# 4. Registramos el Blueprint de las rutas
app.register_blueprint(products_bp)

# TRÁMITE: Creamos las tablas si no existen
with app.app_context():
    db.create_all()
    print("¡Tablas creadas correctamente en bde_tc!")

@app.route('/vehiculos', methods=['GET'])
def listar_vehiculos():
    # 1. Consultamos todos los vehículos usando SQLAlchemy
    lista = Vehiculo.query.all()
    
    # 2. Formateamos los datos para que se vean como JSON
    resultado = []
    for v in lista:
        resultado.append({
            "patente": v.patente,
            "marca": v.marca,
            "modelo": v.modelo
        })
    
    # 3. Retornamos la respuesta
    return {"vehiculos": resultado}, 200

if __name__ == "__main__":
    # Iniciamos el servidor en el puerto 5000
   if __name__ == '__main__':
    app.run(debug=True, port=5001)