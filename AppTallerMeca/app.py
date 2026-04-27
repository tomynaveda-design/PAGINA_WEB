import sqlite3

# CREAR / ABRIR BASE DE DATOS
conn = sqlite3.connect("taller.db")

# CREAR CURSOR (para ejecutar SQL)
cursor = conn.cursor()

# CREAR TABLA
cursor.execute("""
CREATE TABLE IF NOT EXISTS autos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marca TEXT,
    modelo TEXT
)
""")

# GUARDAR CAMBIOS
conn.commit()

# CERRAR CONEXIÓN
conn.close()

print("Base de datos creada correctamente")















