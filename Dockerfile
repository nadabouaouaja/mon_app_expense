# Étape 1 : Build - avec une image plus légère
FROM python:3.11-slim


# Éviter les invites interactives (utile pour apt-get)
ENV DEBIAN_FRONTEND=noninteractive

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers nécessaires en premier (meilleure mise en cache Docker)
COPY requirements.txt .

# Installer les dépendances système (si besoin) et les packages Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier le reste des fichiers du projet
COPY . .

# Exposer le port (Flask par exemple)
EXPOSE 5000

# Commande de démarrage
CMD ["python", "app.py"]
