from flask import Blueprint, render_template, request
from .models import ImageModel
from app.extensions import mongo  # Cambiado para evitar el ciclo
from datetime import datetime
from math import ceil
from flask import jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    date = request.args.get('date')  # Fecha seleccionada
    page = int(request.args.get('page', 1))  # Página actual (por defecto, 1)
    per_page = 12  # Número de registros por página

    image_model = ImageModel(mongo)
    if date:
        images = list(image_model.get_images_by_date(date))
    else:
        images = list(image_model.get_all_images())

    total_records = len(images)
    total_pages = ceil(total_records / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = images[start:end]

    return render_template('index.html', images=paginated_images, page=page, total_pages=total_pages, date=date)

@main.route('/grafico')
def graficos():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))  # Fecha seleccionada o actual
    image_model = ImageModel(mongo)
    images = image_model.get_images_by_date(date)

    # Calcular registros por hora
    hours = [f"{hour:02d}:00" for hour in range(24)]
    data = [0] * 24
    for image in images:
        hour = int(image['fechahora'][11:13])  # Extraer la hora del campo fechahora
        data[hour] += 1

    # Devuelve los datos como JSON
    return jsonify({"labels": hours, "data": data})


@main.route('/chart')
def chart():
    # Simula datos para el gráfico
    labels = [f"{hour}:00" for hour in range(24)]  # Horas del día
    data = [0] * 24  # Inicializa con ceros

    # Aquí puedes agregar lógica para calcular los registros por hora
    # Ejemplo: data[hora] = cantidad_de_registros

    return render_template('chart.html', labels=labels, data=data)