---
title: Darija AICC NLU API
emoji: 🚀
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 8000
---

# API de Classification d'Intention en Darija pour AICC

Ce projet a été développé dans le cadre d'un stage de fin d'études visant à intégrer le dialecte marocain "Darija" dans la solution **AICC (Artificial Intelligence Contact Center)** de Huawei.

L'API utilise un modèle **MARBERTv2**, un Transformer pré-entraîné pour l'arabe et ses dialectes, qui a été fine-tuné sur un corpus personnalisé pour classifier les intentions des utilisateurs s'exprimant en Darija.

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Spaces-Live%20Demo%20API-yellow)](https://mediani-darija-aicc-api.hf.space/docs)

---

## 🚀 API Déployée et Documentation Interactive

L'API est en ligne et pleinement fonctionnelle. Vous pouvez la tester en direct grâce à l'interface Swagger UI générée automatiquement.

**➡️ [Tester l'API interactivement ici](https://mediani-darija-aicc-api.hf.space/docs)**

---

## 🔧 Comment Utiliser l'API

L'API expose un endpoint principal `/predict` qui accepte les requêtes `POST` pour la classification d'intention.

### Exemple de Requête avec `curl`

Voici comment interroger l'API depuis un terminal :

```bash
curl -X 'POST' \
  'https://mediani-darija-aicc-api.hf.space/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Salam, la connexion 4G naqsa 3ndi bzaf"}'
```

### Exemple de Réponse Attendue

L'API retournera un objet JSON avec l'intention (intent) prédite par le modèle et son score de confiance (confidence).

```json
{
  "intent": "declarer_panne",
  "confidence": 0.9954321098
}
```

---

## 📋 Liste des Intentions Reconnues

Le modèle a été entraîné pour reconnaître et classifier les 9 intentions suivantes, qui sont les plus courantes dans un contexte de service client :

- **consulter_solde**: Demandes concernant le solde, la recharge ou les données restantes.
- **reclamer_facture**: Réclamations concernant une facture (montant élevé, erreur...).
- **declarer_panne**: Signalement d'un problème technique (panne réseau, connexion lente...).
- **info_forfait**: Demandes d'informations sur les produits, offres et abonnements.
- **recuperer_mot_de_passe**: Demandes liées à la réinitialisation d'un mot de passe ou d'un code.
- **salutations**: Salutations et début de conversation.
- **remerciements**: Expressions de gratitude.
- **demander_agent_humain**: Demande explicite de parler à un conseiller humain.
- **hors_scope**: Toute demande hors du périmètre du service client.

## 🛠️ Stack Technique & Cycle de Vie du Projet

Ce projet a été réalisé en suivant un cycle de vie complet, du prototypage au déploiement :

- **Modèle**: UBC-NLP/MARBERTv2 fine-tuné avec la bibliothèque transformers de Hugging Face.
- **Corpus**: Un corpus personnalisé a été assemblé en combinant la collecte de données (Twitter, YouTube), la génération par IA, et l'annotation manuelle avec Doccano.
- **Framework API**: FastAPI, pour sa rapidité et sa génération automatique de documentation.
- **Conteneurisation**: Docker, pour garantir la portabilité et la reproductibilité de l'environnement.
- **Versionnement**: Git & Git LFS pour gérer les gros fichiers de modèle (plus de 100 Mo).
- **Déploiement**: L'API est hébergée sur Hugging Face Spaces, fournissant une solution CI/CD (intégration et déploiement continus) à partir d'un dépôt Git.
