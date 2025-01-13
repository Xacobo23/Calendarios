# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copia y instala las dependencias del archivo requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia el código fuente del proyecto
COPY . /app

# Comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
