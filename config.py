class Config:
    MONGO_URI = "mongodb://192.168.2.38:27017/traking"  # Cambia esto a la URI de tu base de datos MongoDB
    SECRET_KEY = "your_secret_key"  # Change this to a random secret key for production use.
    # Configuración de SQLAlchemy
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sasa@192.168.2.38/traking"  # Cambia 'root', 'password' y 'traking' según tu configuración
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:sasa@10.128.0.3/traking"  # Cambia 'root', 'password' y 'traking' según tu configuración  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva el seguimiento de modificaciones para mejorar el rendimiento
    SECRET_KEY = "your_secret_key"  # Cambia esto a una clave secreta aleatoria para producción
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'plate_track:'
    
    # Google OAuth configuration
    GOOGLE_CLIENT_ID = "your-google-client-id.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "your-google-client-secret"    