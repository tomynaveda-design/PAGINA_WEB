from flask import Flask
# Le decimos: "De la carpeta config, traé la clase Config"
from config.config import Config         # Traemos la configuración (puerto 3307, etc)
from Models.db import db            # Traemos el objeto que maneja la base
from Models.parking import Vehiculo # Traemos el modelo de tu auto
from routers.products_routes import products_bp 

app = Flask(__name__)

# Le cargamos la configuración de la base de datos
app.config.from_object(Config)

# Inicializamos la base de datos con la app
db.init_app(app)

# Registramos el pasillo (Blueprint)
app.register_blueprint(products_bp)

# TRÁMITE: Creamos las tablas si no existen
with app.app_context():
    db.create_all()
    print("¡Tablas creadas correctamente en bde_tc!")

@app.route("/")
def index():
    return "HOLA, EL ESTACIONAMIENTO ESTA FUNCIONANDO Y CONECTADO"

@app.route("/hola")
def hola():
    return "HOLA FUNCIONA"

@app.route("/probar-guardar")
def probar_guardar():
    try:
        # Creamos un objeto 'auto' basado en tu modelo de parking.py
        nuevo_auto = Vehiculo(patente="ABC-123", modelo="Fiat Cronos")
        
        # Le decimos a la base de datos: "Che, prepará este auto"
        db.session.add(nuevo_auto)
        
        # Le decimos: "Listo, guardalo definitivamente" (Confirmar)
        db.session.commit()
        
        return "¡AUTO GUARDADO EXITOSAMENTE EN LA BASE DE DATOS!"
    except Exception as e:
        return f"Error al guardar: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True, port=5000)