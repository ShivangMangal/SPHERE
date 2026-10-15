# SPHERE AI Models

This folder contains the core Natural Language Processing pipeline for SPHERE.
It uses HuggingFace Transformers (DistilBERT) and spaCy (NER) to categorize Civil Engineering text.

## Pipeline Flow
1. **Classifier**: Categorizes text into Environmental, Sustainability, Public Health, etc.
2. **NER Model**: Extracts critical entities (emissions, materials, structures).
3. **Prioritization Engine**: Scores each requirement mathematically.

Run python run_e2e_validation.py to generate new analysis payloads.
