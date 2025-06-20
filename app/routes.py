from flask import Blueprint, render_template, request
from .models import ImageModel
from app.extensions import mongo  # Cambiado para evitar el ciclo
from datetime import datetime
from math import ceil
from flask import jsonify
import requests  # Import the requests library
from requests.auth import HTTPDigestAuth
from flask import Response

import cv2
from flask import Response
from app.models import MiTrack
from app import db 
from flask import redirect

main = Blueprint('main', __name__)

# para instalar el servidor de imagenes
# npm install -g http-server  //Para instalar el servidor
# cd F:\imageplate .    //ejemplo original->  http-server ./desktop-main1/imageplate
# http-server .

#@main.route('/')
#def index():
#    date = request.args.get('date')  # Fecha seleccionada
#    page = int(request.args.get('page', 1))  # Página actual (por defecto, 1)
#    per_page = 12  # Número de registros por página

    # image_model = ImageModel(mongo)
    # if date:
    #     images = list(image_model.get_images_by_date(date))
    # else:
    #     images = list(image_model.get_all_images())

    # total_records = len(images)
    # total_pages = ceil(total_records / per_page)
    # start = (page - 1) * per_page
    # end = start + per_page
    # paginated_images = images[start:end]

    # return render_template('index.html', images=paginated_images, page=page, total_pages=total_pages, date=date)


@main.route('/')
def index():
    # Obtén la fecha seleccionada desde los parámetros de la URL
    selected_date = request.args.get('date', None)
    page = request.args.get('page', 1, type=int)  # Página actual (por defecto, 1)
    
    
    # Si no hay fecha o página, redirige a la URL con la fecha de hoy y página 1
    if not selected_date or not page:
        today = datetime.now().strftime("%Y-%m-%d")
        return redirect(f"/?date={today}&page=1")
    per_page = 15  # Número de elementos por página

    if selected_date:
        images_query = MiTrack.query.filter(
            db.func.date(MiTrack.fechahora) == selected_date
        ).order_by(MiTrack.fechahora.desc())
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        images_query = MiTrack.query.filter(
            db.func.date(MiTrack.fechahora) == today
        ).order_by(MiTrack.fechahora.desc())

    pagination = images_query.paginate(page=page, per_page=per_page)
    images = pagination.items
  
    return render_template(
        'index.html',
        images=images,
        pagination=pagination,
        selected_date=selected_date,
    )

@main.route('/images_by_date')
def images_by_date():
    date = request.args.get('date')
    if not date:
        return "Por favor, proporciona una fecha en el formato YYYY-MM-DD.", 400

    # Filtra las imágenes por fecha
    images = MiTrack.get_images_by_date(date)
    return render_template('index.html', images=images)





@main.route('/grafico')
def graficos():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))  # Fecha seleccionada o actual
    images = MiTrack.get_images_by_date(date)  # Usa el método estático del modelo MiTrack

    # Calcular registros por hora
    hours = [f"{hour:02d}:00" for hour in range(24)]
    data = [0] * 24
    for image in images:
        hour = image.fechahora.hour  # Extraer la hora directamente del objeto datetime
        data[hour] += 1

    # Devuelve los datos como JSON
    return jsonify({"labels": hours, "data": data})


@main.route('/chart')
def chart():
    date = request.args.get('date')  # Obtiene la fecha seleccionada
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')  # Usa la fecha actual si no se proporciona una

    # Obtén las imágenes de la fecha seleccionada
    images = MiTrack.get_images_by_date(date)

    # Calcular registros por hora
    labels = [f"{hour}:00" for hour in range(24)]
    data = [0] * 24
    for image in images:
        # Asegúrate de que `fechahora` sea un objeto datetime
        hour = image.fechahora.hour  # Extraer la hora directamente del objeto datetime
        data[hour] += 1

    return render_template('chart.html', labels=labels, data=data, date=date)


#Esto funciona pero colapsa la camara
#@main.route('/snapshot')
#def snapshot():
#    url = "http://192.168.2.64/ISAPI/Streaming/channels/101/picture?videoResolutionWidth=1920&videoResolutionHeight=1080"
##    auth = HTTPDigestAuth('admin', '96552333A')  # Use Digest Authentication
#    try:
#        response = requests.get(url, auth=auth, stream=True, timeout=5)  # Add a timeout for better error handling
##        if response.status_code == 200:
#            return Response(response.content, content_type=response.headers['Content-Type'])
#        else:
##            return f"Error fetching snapshot: {response.status_code} {response.reason}", response.status_code
##    except requests.exceptions.RequestException as e:
#        return f"Error connecting to the camera: {str(e)}", 500
    
    
    
@main.route('/video_feed')
def video_feed():
    rtsp_url = "rtsp://admin:96552333A@192.168.2.64:554/Streaming/channels/101"  # URL RTSP de la cámara
    #rtsp_url = "rtsp://admin:96552333A@host.docker.internal:554/Streaming/channels/101"
    def generate_frames():
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print("Error: No se pudo abrir el flujo RTSP.")
            return

        while True:
            success, frame = cap.read()
            if not success:
                break

            # Codifica el frame como JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Devuelve el frame como parte del flujo MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')