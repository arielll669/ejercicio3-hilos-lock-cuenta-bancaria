FROM python:3.12-slim

# Muestra la salida de print() en tiempo real dentro del contenedor
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY main.py .

CMD ["python", "main.py"]
