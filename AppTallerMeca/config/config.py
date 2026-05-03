import os

class Config:
    # Ruta con el puerto 3307 de tu XAMPP
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'mysql+pymysql://root:@localhost:3307/bde_tc'
    
    # Desactivar el rastreo de modificaciones para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta opcional (útil si después usas sesiones o formularios protegidos)
    SECRET_KEY = os.getenv('SECRET_KEY') or 'clave_secreta_muy_dificil'