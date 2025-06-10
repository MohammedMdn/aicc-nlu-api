# main.py

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from typing import Dict, Any

# --- Configuration ---
# Chemin vers votre modèle fine-tuné. Assurez-vous que ce dossier est correct.
MODEL_PATH = "./mon_modele_darija_final"

# --- Chargement du modèle (partie critique) ---
# Cette partie est exécutée une seule fois, au démarrage du serveur.
# C'est une bonne pratique pour éviter de recharger le modèle à chaque requête.
try:
    print("Chargement du tokenizer et du modèle MARBERT fine-tuné...")
    
    # On spécifie le device (GPU si disponible, sinon CPU)
    device = 0 if torch.cuda.is_available() else -1
    
    # Création du pipeline de classification de texte de Hugging Face.
    # C'est la manière la plus simple d'utiliser un modèle pour l'inférence.
    nlu_pipeline = pipeline(
        "text-classification",
        model=MODEL_PATH,
        tokenizer=MODEL_PATH,
        device=device  # Utilise le GPU si disponible
    )
    print("Modèle chargé avec succès !")

except Exception as e:
    # Si le modèle ne peut pas être chargé, on lève une erreur claire.
    print(f"Erreur critique lors du chargement du modèle: {e}")
    nlu_pipeline = None

# --- Définition de l'application FastAPI ---
app = FastAPI(
    title="API de NLU pour Darija Marocaine",
    description="Une API pour classifier l'intention d'un texte en Darija, basée sur MARBERT.",
    version="1.0.0"
)

# --- Définition des modèles de données (Pydantic) ---
# C'est pour la validation automatique des requêtes.

class TextInput(BaseModel):
    """Modèle pour le corps de la requête de prédiction."""
    text: str # Le champ doit s'appeler 'text'
    # Exemple de requête JSON attendue: {"text": "3afak bghit nchouf lfactura"}

class PredictionResponse(BaseModel):
    """Modèle pour la réponse de l'API."""
    intent: str
    confidence: float

# --- Définition des routes de l'API ---

@app.get("/", tags=["Général"])
def read_root() -> Dict[str, str]:
    """Route principale qui retourne un message de bienvenue."""
    return {"message": "Bienvenue sur l'API de NLU Darija. Utilisez le endpoint /predict pour faire une prédiction."}


@app.get("/health", tags=["Général"])
def health_check() -> Dict[str, str]:
    """Route de 'health check' pour vérifier si le service est en ligne et le modèle chargé."""
    if nlu_pipeline is None:
        raise HTTPException(status_code=500, detail="Erreur: Le modèle NLP n'a pas pu être chargé.")
    return {"status": "ok", "model_status": "loaded"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prédiction"])
def predict_intent(request: TextInput) -> PredictionResponse:
    """
    Endpoint principal pour la prédiction d'intention.
    Prend un texte en entrée et retourne l'intention prédite et son score de confiance.
    """
    if nlu_pipeline is None:
        raise HTTPException(status_code=503, detail="Le service est indisponible car le modèle n'est pas chargé.")

    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Le champ 'text' ne peut pas être vide.")

    try:
        # Utilisation du pipeline pour faire la prédiction
        prediction = nlu_pipeline(request.text, top_k=1)[0]
        
        # Le pipeline retourne un dictionnaire avec 'label' et 'score'
        # On renomme pour correspondre à notre modèle de réponse
        intent = prediction['label']
        confidence = prediction['score']

        return PredictionResponse(intent=intent, confidence=confidence)

    except Exception as e:
        # Gestion d'erreurs inattendues pendant la prédiction
        raise HTTPException(status_code=500, detail=f"Une erreur interne est survenue: {str(e)}")