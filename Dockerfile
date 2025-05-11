# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará la aplicación Flask
EXPOSE 5000

# Establece la variable de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para ejecutar la aplicación
CMD ["python", "-m", "flask", "run"]