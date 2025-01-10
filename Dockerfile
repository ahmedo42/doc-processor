# Use the official Python image from the DockerHub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create media directory
RUN mkdir -p /app/media

# Set permissions for media directory
RUN chmod 755 /app/media

# Copy the content of the local src directory to the working directory
COPY . .

# Expose ports for http/https
EXPOSE 8000 443

# Command to run migrations
CMD python manage.py makemigrations api && \
    python manage.py migrate && \
    python manage.py test api.tests && \
    python manage.py runserver 0.0.0.0:8000