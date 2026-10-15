# SPHERE Codebase

This directory houses the core technical infrastructure for the SPHERE (Civil Engineering & Urban Planning) project. It is logically divided into three primary components:

## 1. Frontend
The UI dashboard built using React, Vite, and Tailwind CSS. It is responsible for rendering the requirements engineering visualization, mapping JSON analysis outputs into priority cards, and presenting a seamless user interface for city planners.

## 2. Model
The Natural Language Processing (NLP) intelligence layer. This contains the HuggingFace DistilBERT classifiers and spaCy Named Entity Recognition (NER) models used to categorize and mathematically prioritize raw civil engineering texts (e.g., carbon emission mandates, public surveys).

## 3. BackEnd
The backend architecture designed to bridge the NLP pipeline with the Frontend, handling data ingestion and payload generation.

---
**Setup Note:** Each sub-folder contains its own specific README.md with instructions on how to install dependencies and run that specific module.
