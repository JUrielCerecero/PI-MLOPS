# Utiliza una imagen base con Python
FROM python:Python 3.11.6

# Establece el directorio de trabajo en /app
WORKDIR / app

# Copia el archivo de requisitos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido actual al contenedor en /app
COPY . .

# Expone el puerto en el que la aplicación va a estar escuchando
EXPOSE 8000

# Comando para ejecutar la aplicación cuando el contenedor se inicie
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
