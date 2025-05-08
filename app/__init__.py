from flask import Flask
from config import Config
from app.extensions import mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa PyMongo
    mongo.init_app(app)

    # Registra el blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app

app = create_app()