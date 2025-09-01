# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el código de la aplicación al contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

