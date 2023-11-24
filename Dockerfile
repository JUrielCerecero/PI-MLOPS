# Utiliza una imagen base con Python
FROM python:3.11-slim-buster

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos al contenedor
COPY requirements.txt ./requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el contenido actual al contenedor en /app
COPY . .

# Expone el puerto en el que la aplicación va a estar escuchando
EXPOSE 8000

# Comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
