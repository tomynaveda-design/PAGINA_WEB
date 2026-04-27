from Models.db import conexion_db

class Vehiculo:
    def __init__(self, patente, modelo=None, id=None, hora_entrada=None, estado='Estacionado'):
        self.id = id
        self.patente = patente
        self.modelo = modelo
        self.hora_entrada = hora_entrada
        self.estado = estado

    # Método para registrar la entrada de un auto
    def registrar_entrada(self):
        conexion = conexion_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                # Insertamos la patente y el modelo. La hora se pone sola por el DEFAULT del Workbench.
                sql = "INSERT INTO vehiculos (patente, modelo) VALUES (%s, %s)"
                valores = (self.patente, self.modelo)
                
                cursor.execute(sql, valores)
                conexion.commit()
                print(f"Ingreso registrado: Patente {self.patente}")
            except Exception as e:
                print(f"Error al registrar entrada: {e}")
            finally:
                cursor.close()
                conexion.close()

    # Método para ver qué autos hay hoy
    @staticmethod
    def listar_estacionados():
        conexion = conexion_db()
        lista = []
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM vehiculos WHERE estado = 'Estacionado'")
                resultados = cursor.fetchall()
                for r in resultados:
                    lista.append(r)
            finally:
                conexion.close()
        return lista
    
    
    
if __name__ == "__main__":
    # Todo esto tiene que estar corrido a la derecha (4 espacios)
    nuevo_auto = Vehiculo(patente="ABC-123", modelo="Fiat Cronos")
    nuevo_auto.registrar_entrada()

    autos = Vehiculo.listar_estacionados()
    print("Autos actualmente en la BDE:")
    print(autos)