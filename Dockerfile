FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
