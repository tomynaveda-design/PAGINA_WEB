import mysql.connector
from mysql.connector import Error

def conexion_db():
    try:
        # Aquí configuramos el "puente" hacia tu base BDE
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", # <--- ASEGURATE QUE ESTA SEA TU CLAVE
            database="BDE"
        )
        
        if conexion.is_connected():
            return conexion
            
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
    return None # Por si algo falla fuera del try

# Este bloque tiene que estar pegado al borde izquierdo
if __name__ == "__main__":
    con = conexion_db()
    if con:
        print("¡Conexión exitosa a BDE! El sistema de estacionamiento está listo.")
        con.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        