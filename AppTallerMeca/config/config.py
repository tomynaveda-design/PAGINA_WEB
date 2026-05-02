class Config:
    # Esta es la ruta para que Python encuentre tu MySQL
    # Formato: mysql+pymysql://usuario:contraseña@localhost:puerto/nombre_base
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3307/bde_tc'
    
    # Esto se pone en False para que Flask no consuma recursos extra rastreando cambios
    SQLALCHEMY_TRACK_MODIFICATIONS = False