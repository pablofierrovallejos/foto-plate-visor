from flask_pymongo import PyMongo
from datetime import datetime

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