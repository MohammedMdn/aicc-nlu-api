# Étape 1: Utiliser une image de base Python officielle
FROM python:3.9-slim

# Étape 2: Définir le répertoire de travail dans le container
WORKDIR /app

# Étape 3: Copier le fichier des dépendances
COPY requirements.txt requirements.txt

# Étape 4: Installer les dépendances
# --no-cache-dir pour garder l'image légère
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier tout le reste de votre projet dans le container
# Cela inclut main.py et le dossier de votre modèle (ex: "marbert-darija-nlu-aicc")
COPY . .

# Étape 6: Exposer le port que votre API utilise
EXPOSE 8000

# Étape 7: La commande pour lancer l'API quand le container démarre
# Uvicorn est lancé avec host="0.0.0.0" pour être accessible de l'extérieur du container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]