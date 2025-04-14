FROM python:3.11-slim

# Configuration de base
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copie des fichiers avec vérification explicite
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY app.py .

# Vérification finale des permissions
RUN find . -type f -exec chmod 644 {} \; && \
    find . -type d -exec chmod 755 {} \;

EXPOSE 5000
CMD ["python", "app.py"]
