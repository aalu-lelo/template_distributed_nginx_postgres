FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential

RUN pip install psycopg2

COPY app.py /app/
COPY images/hyderabad.jpg /app/hyderabad.jpg

EXPOSE 8000

CMD ["python", "app.py"]
