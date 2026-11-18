# SPHERE: AI-Driven Requirements Engineering for Sustainable Smart Cities

> **SPHERE** (*Stakeholder-centric Pipeline for Holistic Extraction and Requirements Engineering*) is an end-to-end, multi-tier natural language processing framework that automates the extraction, semantic classification, named entity recognition, clustering, and conflict-aware synthesis of non-functional sustainability requirements from citizen and stakeholder feedback.

---

## Architecture & System Overview

SPHERE processes unstructured citizen feedback into structured, prioritized engineering requirements across environmental, social, and economic sustainability dimensions.

```
Citizen & Stakeholder Feedback (Transcripts, Petitions, Reports)
                           │
                           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  Tier 1: Document Ingestion & Section Filtering             │
 │  (Heuristic keyword scoring: clean, climate, energy, etc.)  │
 └─────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  Tier 2: Binary Requirement Classifier                      │
 │  (DistilBERT Sequence Classification — 84.79% Validation F1) │
 └─────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  Tier 3: Domain Named Entity Recognition (NER)              │
 │  (spaCy Transformer bert-base-uncased — 95.24% Test F1)     │
 │  Entities: STAKEHOLDER, METRIC, INFRASTRUCTURE              │
 └─────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  Tier 4: Semantic Clustering & Deduplication                │
 │  (Sentence-Transformers all-MiniLM-L6-v2, Cosine Sim 0.85) │
 └─────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  Tier 5: Conflict Resolution & Requirement Synthesis        │
 │  (Heuristic Trade-off Detection + T5-Small Abstractive Sum) │
 └─────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
 Structured Sustainable Requirements & Interactive Analytics Dashboard
```

---

## Empirical Benchmark & Validation Results

Evaluated on real-world sustainability corpora (5,594 texts, 1,061 annotated requirement sentences, 10,691 semantic clusters):

| Pipeline Stage | Model Architecture | Metric | Result | Benchmark Details |
| :--- | :--- | :--- | :--- | :--- |
| **Requirement Classification** | DistilBERT (`distilbert-base-uncased`) | Validation F1 | **84.79%** | Evaluated across 5 training epochs on annotated requirements |
| **Named Entity Recognition** | spaCy Transformer (`bert-base-uncased`) | Overall Micro F1 | **95.24%** | `STAKEHOLDER` F1: **100%**, `METRIC` F1: **91.89%** |
| **Semantic Clustering** | Sentence-Transformers (`all-MiniLM-L6-v2`) | Total Clusters | **10,691** | Grouped at cosine similarity threshold $\ge 0.85$ |
| **Synthesis & Summarization** | T5-small Seq2Seq | Abstractive | Verified | Trade-off identification & unified requirement generation |

---

## Repository Structure

```
SPHERE/
├── Introduction_Methodology.docx           # Complete research methodology document
├── SPHERE_Architecture.docx                # Formal system architecture specification
├── SPHERE_Architecture.png                 # Serpentine workflow architecture diagram
├── SPHERE_Research_Gaps.docx               # Comprehensive review of prior art & research gaps
├── SPHERE_Results_and_Evaluation_Report.md # Rigorous empirical evaluation report
├── SPHERE_Codebase/                        # (Kept in local workspace via .gitignore)
│   ├── Frontend/                           # React 18 + Vite 6 + Tailwind CSS Dashboard
│   ├── Model/                              # PyTorch / spaCy / HuggingFace Pipeline
│   └── BackEnd/                            # Spring Boot 4.0.3 REST API Service
└── README.md                               # Project documentation & run guide
```

---

## Prerequisites

Before running the project components, ensure you have the following installed:

- **Node.js**: `v18.0.0` or higher (`v20+` recommended) & `npm`
- **Python**: `3.10` or `3.11` (with `pip` and virtual environment support)
- **Java JDK**: `21` (required only if running the Spring Boot backend)
- **Hardware**: Compatible with CPU execution; NVIDIA GPU with CUDA support recommended for training/inference acceleration.

---

## How to Run the Project

### Option A: Interactive Frontend Dashboard (Recommended for Demo)

The web dashboard provides an interactive user interface to explore extracted requirements, filter clusters, view NER tag visualizations, and analyze sustainability metrics.

1. Navigate to the Frontend directory:
   ```bash
   cd SPHERE_Codebase/Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the local Vite development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

*(Optional) To launch as a standalone desktop app via Electron:*
```bash
npm run electron:dev
```

---

### Option B: Python NLP Pipeline & End-to-End Inference

Run the core machine learning pipeline to process raw text through classification, NER extraction, semantic clustering, and requirement synthesis.

1. Navigate to the Model directory:
   ```bash
   cd SPHERE_Codebase/Model
   ```

2. (Recommended) Create and activate a Python virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the end-to-end pipeline validation script:
   ```bash
   python run_e2e_validation.py
   ```

---

### Option C: Run Full Model Evaluation Benchmarks

To reproduce the exact empirical evaluation metrics reported in the research documentation:

1. Ensure your virtual environment is active in `SPHERE_Codebase/Model`.
2. Run the unified evaluation test suite:
   ```bash
   python -m evaluation.run_all_evaluations
   ```

3. Run individual module evaluations:
   - **Requirement Classifier (DistilBERT):**
     ```bash
     python -m requirement_classifier.evaluate
     ```
   - **Named Entity Recognition (spaCy Transformer):**
     ```bash
     python -m ner_model.evaluate_ner
     ```

---

### Option D: Spring Boot Enterprise Backend (Optional Service)

The Spring Boot backend exposes REST endpoints for data persistence, multi-user project management, and pipeline orchestration.

1. Navigate to the BackEnd directory:
   ```bash
   cd SPHERE_Codebase/BackEnd
   ```

2. Start the application using Maven:
   - **Windows:**
     ```cmd
     mvnw.cmd spring-boot:run
     ```
   - **Linux / macOS:**
     ```bash
     ./mvnw spring-boot:run
     ```

3. The REST API will be accessible at:
   ```
   http://localhost:8080
   ```

---

## Documentation & Research Artifacts

Detailed technical documentation and research papers are available in the repository root:

- **[Introduction & Methodology](Introduction_Methodology.docx)**: Full formal problem formulation, mathematical models, pipeline definitions, and training hyperparameters.
- **[System Architecture](SPHERE_Architecture.docx)**: In-depth design of the five-tier pipeline, data flow contracts, and trade-off detection algorithms.
- **[Research Gaps & Prior Art](SPHERE_Research_Gaps.docx)**: Comparative analysis against Hey et al. (2020), Moon et al. (2021), and Falco & Kleinhans (2018).
- **[Evaluation Report](SPHERE_Results_and_Evaluation_Report.md)**: Full breakdown of validation scores, confusion matrices, and ablation observations.

---

## Authors & Acknowledgments

- **Core Contributors**: SPHERE Research & Engineering Team
- **Department**: Computer Science & Engineering
- **Domain**: Natural Language Processing, Requirements Engineering, Sustainable Urban Development
