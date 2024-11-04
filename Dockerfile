# Usa una imagen base de Python
FROM python:3.9

# Configura el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto en el que correrá la API
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
