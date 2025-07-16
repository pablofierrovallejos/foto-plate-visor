# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para libGL.so.1
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxext6 \
    vlc \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Configurar zona horaria Santiago
ENV TZ=America/Santiago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Crear un usuario no root
#RUN useradd -m vlcuser
#USER vlcuser

# Expone el puerto en el que se ejecutará la aplicación Flask
EXPOSE 5000

# Establece la variable de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para ejecutar la aplicación
CMD ["python", "-m", "flask", "run"]

# docker build -t webtrack-app:v2 .
# docker tag webtrack-app:v2 96552333aa/webtrack-app:v2
# docker push 96552333aa/webtrack-app:v2
# docker run -p 5000:5000 -d webtrack-app:v2
# docker run -p 5000:5000 -d --net=host --name web-track -it webtrack-app:v2

