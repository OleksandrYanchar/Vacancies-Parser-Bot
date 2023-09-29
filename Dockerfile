FROM python:3.9-slim

WORKDIR /Vacancies-pasrser-bot

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["python", "main.py"]
CMD ["celery", "-A", "my_schedule", "worker", "--loglevel=info"]