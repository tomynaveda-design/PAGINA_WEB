# --- CLASES BASE ---

class Persona:
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self._dni = dni # Encapsulamiento manual

    def get_dni(self):
        return self._dni

class Vehiculo:
    def __init__(self, patente, marca):
        self._patente = patente
        self.marca = marca

    def get_patente(self):
        return self._patente

# --- HERENCIA ---

class Cliente(Persona):
    def __init__(self, nombre, dni, telefono):
        Persona.__init__(self, nombre, dni) # Forma más simple de heredar
        self.telefono = telefono

class Mecanico(Persona):
    def __init__(self, nombre, dni, especialidad):
        Persona.__init__(self, nombre, dni)
        self.especialidad = especialidad

# --- POLIMORFISMO (Diferentes resultados para el mismo nombre de función) ---

class Reparacion:
    def __init__(self, costo_base):
        self.costo_base = costo_base

    def calcular_total(self):
        return self.costo_base

class ReparacionUrgente(Reparacion):
    def calcular_total(self):
        # Polimorfismo: esta versión suma un extra
        return self.costo_base + 2000 

# --- PRUEBA ---
mi_reparacion = ReparacionUrgente(5000)
print(f"Total a cobrar: {mi_reparacion.calcular_total()}")

class OrdenDeTrabajo:
    def __init__(self, cliente, vehiculo, mecanico, reparacion):
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.mecanico = mecanico
        self.reparacion = reparacion

    def mostrar_ticket(self):
        print(f"--- TICKET DEL TALLER ---")
        print(f"Cliente: {self.cliente.nombre}")
        print(f"Vehículo: {self.vehiculo.marca} (Patente: {self.vehiculo.get_patente()})")
        print(f"Atendido por: {self.mecanico.nombre}")
        print(f"Trabajo: {self.reparacion.costo_base}")
        print(f"Total a pagar: {self.reparacion.calcular_total()}")

    
    # --- PRUEBA MEJORADA ---

# 1. Creamos a las personas
claudio_mecanico = Mecanico("Claudio", "12345678", "Frenos")
juan_cliente = Cliente("Juan", "99888777", "11-2222-3333")

# 2. Creamos el vehículo
auto_juan = Vehiculo("ABC-123", "Ford")

# 3. Creamos la reparación (Urgente para usar el polimorfismo)
reparacion_juan = ReparacionUrgente(5000)

# 4. Juntamos todo en una orden
orden1 = OrdenDeTrabajo(juan_cliente, auto_juan, claudio_mecanico, reparacion_juan)

# 5. Mostramos el resultado
orden1.mostrar_ticket()