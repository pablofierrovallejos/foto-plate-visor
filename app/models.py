from flask_pymongo import PyMongo
from datetime import datetime
from app import db


class ImageModel:
    def __init__(self, mongo):
        self.mongo = mongo

    #def get_all_images(self):
    #    return self.mongo.db.mitrack.image.find()
    
    def get_all_images(self):
        # Obtiene la fecha actual en formato "YYYY-MM-DD"
        today = datetime.now().strftime("%Y-%m-%d")
        # Define el rango de fechas para la consulta
        start_of_day = f"{today} 00:00:00"
        end_of_day = f"{today} 23:59:59"
        # Consulta para obtener solo los registros de hoy
        return self.mongo.db.mitrack.find(
            {"fechahora": {"$gte": start_of_day, "$lt": end_of_day}},
            {"_id": 0, "tipo": 1, "direccion": 1, "image": 1, "fechahora": 1}
        ).sort("fechahora", -1)
        
    def get_images_by_date(self, date):
        start_of_day = f"{date} 00:00:00"
        end_of_day = f"{date} 23:59:59"
        return self.mongo.db.mitrack.find(
            {"fechahora": {"$gte": start_of_day, "$lt": end_of_day}},
            {"_id": 0, "tipo": 1, "direccion": 1, "image": 1, "fechahora": 1}
        ).sort("fechahora", -1)
                
    def get_image_by_id(self, image_id):
        return self.mongo.db.mitrack.find_one({"_id": image_id})

    def add_image(self, image_data):
        self.mongo.db.mitrack.insert_one(image_data)
        
        
        
        
        
        

class MiTrack(db.Model):
    __tablename__ = 'mitrack'

    idmitrack = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(15), nullable=True)
    fechahora = db.Column(db.DateTime, nullable=True)
    direccion = db.Column(db.String(10), nullable=True)
    color = db.Column(db.String(15), nullable=True)
    marca = db.Column(db.String(15), nullable=True)
    modelo = db.Column(db.String(15), nullable=True)
    patente = db.Column(db.String(8), nullable=True)
    #image = db.Column(db.LargeBinary, nullable=True)
    #imageplate = db.Column(db.LargeBinary, nullable=True)
    imagefile_env = db.Column(db.String(35), nullable=True)
    imagefile_plt = db.Column(db.String(35), nullable=True)
    
    def __repr__(self):
        return f"<MiTrack {self.idmitrack} - {self.tipovehiculo}>"

    @staticmethod
    def get_all_images():
        # Obtiene todas las imágenes ordenadas por fecha y hora descendente
        return MiTrack.query.order_by(MiTrack.fechahora.desc()).all()

    @staticmethod
    def get_images_by_date(date):
        # Filtra las imágenes por una fecha específica
        start_of_day = datetime.strptime(f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_of_day = datetime.strptime(f"{date} 23:59:59", "%Y-%m-%d %H:%M:%S")
        return MiTrack.query.filter(MiTrack.fechahora >= start_of_day, MiTrack.fechahora <= end_of_day).order_by(MiTrack.fechahora.desc()).all()

    @staticmethod
    def get_image_by_id(image_id):
        # Obtiene una imagen específica por su ID
        return MiTrack.query.get(image_id)

    @staticmethod
    def add_image(data):
        # Agrega una nueva imagen a la base de datos
        new_image = MiTrack(**data)
        db.session.add(new_image)
        db.session.commit()        