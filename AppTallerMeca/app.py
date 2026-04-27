
from flask import Flask, render_template, request, redirect
from Models.parking import Vehiculo

app = Flask(__name__)

@app.route('/')
def index():
    # Esta es la página principal
    return "<h1>Bienvenido al Estacionamiento</h1><p>El sistema está online.</p>"

@app.route('/registrar', methods=['POST'])
def registrar():
    patente = request.form.get('patente')
    modelo = request.form.get('modelo')
    
    if patente:
        nuevo_auto = Vehiculo(patente, modelo)
        nuevo_auto.registrar_entrada()
        return f"Vehículo {patente} registrado con éxito."
    return "Error: Falta la patente."

if __name__ == '__main__':
    app.run(debug=True)




