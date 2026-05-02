from flask import Flask
from config.config import Config
from Models.db import db
from routers.products_routes import products_bp

# 1. Creamos la aplicación
app = Flask(__name__)

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

if __name__ == "__main__":
    # Iniciamos el servidor en el puerto 5000
    app.run(debug=True, port=5000)