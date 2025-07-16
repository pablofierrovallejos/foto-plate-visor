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
import logging

# Configurar logging para SQL
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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
    selected_date_end = request.args.get('date_end', None)  # Nueva fecha fin
    selected_plate = request.args.get('plate', None)  # Nuevo parámetro para buscar por patente
    page = request.args.get('page', 1, type=int)  # Página actual (por defecto, 1)
    
    
    # Si no hay fecha o página, redirige a la URL con la fecha de hoy y página 1
    if not selected_date or not page:
        today = datetime.now().strftime("%Y-%m-%d")
        return redirect(f"/?date={today}&page=1")
    per_page = 15  # Número de elementos por página

    # Construir la consulta base con rango de fechas
    print(f"Parámetros recibidos - Fecha inicio: {selected_date}, Fecha fin: {selected_date_end}, Patente: {selected_plate}")
    
    if selected_date and selected_date_end:
        # Búsqueda por rango de fechas - convertir strings a datetime
        try:
            start_date = datetime.strptime(selected_date, '%Y-%m-%d')
            end_date = datetime.strptime(selected_date_end, '%Y-%m-%d')
            
            # Establecer horarios completos para el rango
            start_of_day = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            print(f"Rango de fechas convertido: {start_of_day} hasta {end_of_day}")
            
            # CORREGIDO: fechahora >= fecha_inicio AND fechahora <= fecha_fin
            images_query = MiTrack.query.with_entities(
                MiTrack.idmitrack,
                MiTrack.tipo,
                MiTrack.fechahora,
                MiTrack.direccion,
                MiTrack.imagefile_env,
                MiTrack.imagefile_plt
            ).filter(
                MiTrack.fechahora >= start_of_day,
                MiTrack.fechahora <= end_of_day
            )
            print(f"Consulta de rango: fechahora >= {start_of_day} AND fechahora <= {end_of_day}")
            
        except ValueError as e:
            print(f"Error al convertir fechas: {e}")
            # Si hay error en la conversión, usar fecha de hoy
            today = datetime.now()
            start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
            images_query = MiTrack.query.with_entities(
                MiTrack.idmitrack,
                MiTrack.tipo,
                MiTrack.fechahora,
                MiTrack.direccion,
                MiTrack.imagefile_env,
                MiTrack.imagefile_plt
            ).filter(
                MiTrack.fechahora >= start_of_day,
                MiTrack.fechahora <= end_of_day
            )
    elif selected_date:
        # Búsqueda por fecha única - convertir string a datetime
        try:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            print(f"Fecha única convertida: {start_of_day} hasta {end_of_day}")
            
            images_query = MiTrack.query.with_entities(
                MiTrack.idmitrack,
                MiTrack.tipo,
                MiTrack.fechahora,
                MiTrack.direccion,
                MiTrack.imagefile_env,
                MiTrack.imagefile_plt
            ).filter(
                MiTrack.fechahora >= start_of_day,
                MiTrack.fechahora <= end_of_day
            )
            print(f"Consulta única: fechahora >= {start_of_day} AND fechahora <= {end_of_day}")
            
        except ValueError as e:
            print(f"Error al convertir fecha: {e}")
            # Si hay error en la conversión, usar fecha de hoy
            today = datetime.now()
            start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
            images_query = MiTrack.query.with_entities(
                MiTrack.idmitrack,
                MiTrack.tipo,
                MiTrack.fechahora,
                MiTrack.direccion,
                MiTrack.imagefile_env,
                MiTrack.imagefile_plt
            ).filter(
                MiTrack.fechahora >= start_of_day,
                MiTrack.fechahora <= end_of_day
            )
    else:
        # Fecha por defecto (hoy)
        today = datetime.now()
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        print(f"Usando fecha por defecto: {start_of_day} hasta {end_of_day}")
        images_query = MiTrack.query.with_entities(
            MiTrack.idmitrack,
            MiTrack.tipo,
            MiTrack.fechahora,
            MiTrack.direccion,
            MiTrack.imagefile_env,
            MiTrack.imagefile_plt
        ).filter(
            MiTrack.fechahora >= start_of_day,
            MiTrack.fechahora <= end_of_day
        )
        print(f"Consulta por defecto: fechahora >= {start_of_day} AND fechahora <= {end_of_day}")
    
    # Verificar si hay datos en la tabla antes de aplicar filtros
    total_records = MiTrack.query.count()
    print(f"Total de registros en la tabla: {total_records}")
    
    # Mostrar algunos registros de ejemplo para verificar formato de fechas
    sample_records = MiTrack.query.limit(3).all()
    print("Ejemplos de fechas en la base de datos:")
    for record in sample_records:
        print(f"  ID: {record.idmitrack}, Fecha: {record.fechahora}, Tipo: {record.tipo}")
    print("-" * 60)
    
    # Agregar filtro por patente si se proporciona
    if selected_plate:
        print(f"Filtrando por patente: {selected_plate}")
        try:
            # Limpiar el parámetro de patente y asegurar que sea string
            clean_plate = str(selected_plate).strip()
            if clean_plate:  # Solo filtrar si no está vacío
                images_query = images_query.filter(
                    MiTrack.tipo.ilike(f'%{clean_plate}%')  # Búsqueda parcial, insensible a mayúsculas
                )
        except Exception as e:
            print(f"Error al filtrar por patente: {e}")
            # Continuar sin filtro de patente si hay error
    
    # Ordenar por fecha descendente
    images_query = images_query.order_by(MiTrack.fechahora.desc())
    
    # Mostrar la consulta SQL que se va a ejecutar
    print("=" * 60)
    print("CONSULTA SQL GENERADA:")
    print("=" * 60)
    print(str(images_query.statement.compile(compile_kwargs={"literal_binds": True})))
    print("=" * 60)
    print(f"Parámetros de búsqueda:")
    print(f"  - Fecha inicio: {selected_date}")
    print(f"  - Fecha fin: {selected_date_end}")
    print(f"  - Patente: {selected_plate}")
    print(f"  - Página: {page}")
    print("=" * 60)

    pagination = images_query.paginate(page=page, per_page=per_page)
    images = pagination.items
    
    # Convertir los resultados a objetos más manejables
    processed_images = []
    for img in images:
        if hasattr(img, 'idmitrack'):  # Si es un objeto completo
            processed_images.append({
                'idmitrack': img.idmitrack,
                'tipo': img.tipo,
                'fechahora': img.fechahora,
                'direccion': img.direccion,
                'imagefile_env': img.imagefile_env,
                'imagefile_plt': img.imagefile_plt
            })
        else:  # Si es una tupla de with_entities
            processed_images.append({
                'idmitrack': img[0],
                'tipo': img[1],
                'fechahora': img[2],
                'direccion': img[3],
                'imagefile_env': img[4],
                'imagefile_plt': img[5]
            })
    
    print(f"Resultados encontrados: {pagination.total}")
    print(f"Registros en esta página: {len(processed_images)}")
    print("=" * 60)
  
    return render_template(
        'index.html',
        images=processed_images,
        pagination=pagination,
        selected_date=selected_date,
        selected_date_end=selected_date_end,  # Pasar la fecha fin al template
        selected_plate=selected_plate,  # Pasar la patente seleccionada al template
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