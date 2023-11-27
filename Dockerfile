# Utiliza una imagen base de Python
FROM python:3.11.6

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]