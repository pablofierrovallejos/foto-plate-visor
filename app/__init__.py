from flask import Flask
from config import Config
from app.extensions import mongo
from flask_sqlalchemy import SQLAlchemy
from config import Config
import base64


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Elimina esta línea si no necesitas MongoDB
    #mongo.init_app(app)
    
    #Inicializa SQLAlchemy
    db.init_app(app)
    
    # Registra el filtro personalizado para Base64
    @app.template_filter('b64encode')
    def b64encode_filter(data):
        if data is None:
            print("No data to encode")
            return ""
        if isinstance(data, bytes):  # Si los datos son de tipo bytes
            try:
                #encoded = base64.b64encode(data).decode('utf-8')  # Codifica y decodifica a str
                #print(f"Encoded data: {encoded[:50]}...")  # Muestra los primeros 50 caracteres
                
                #if data.startswith("b'") or data.startswith('b"'):  # Elimina el prefijo b' si existe
                #    cleaned_data = data[2:-1]  # Elimina los primeros 2 y el último carácter
                #    print(f"Cleaned string data: {cleaned_data[:50]}...")
                #    return cleaned_data
                
                
                
                return data.decode('utf-8')  # Decodifica bytes a str
            except Exception as e:
                print(f"Error encoding data: {e}")
                return ""
        elif isinstance(data, str):  # Si ya es una cadena
            if data.startswith("b'") or data.startswith('b"'):  # Elimina el prefijo b' si existe
                cleaned_data = data[2:-1]  # Elimina los primeros 2 y el último carácter
                print(f"Cleaned string data: {cleaned_data[:50]}...")
                return cleaned_data
            print(f"Data is already a valid string: {data[:50]}...")  # Muestra los primeros 50 caracteres
            return data
        else:
            print("Unsupported data type")
            return ""
        
    
    # Registra el blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app

app = create_app()