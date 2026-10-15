# 🌐 SPHERE: AI-Powered Requirements Engineering for Urban Planning

SPHERE is an advanced, end-to-end Natural Language Processing (NLP) pipeline and visualization dashboard designed specifically for **Civil Engineering, Urban Planning, and Public Infrastructure**. 

By ingesting unstructured text from public surveys, environmental activists, city council mandates, and structural policies, SPHERE automatically extracts, categorizes, and mathematically prioritizes civil engineering requirements, allowing city planners to make data-driven infrastructure decisions instantly.

---

## 🚀 Key Features

* **Intelligent Classification**: Uses a fine-tuned HuggingFace **DistilBERT** model to instantly categorize unstructured text into critical civil domains (e.g., *Environmental, Sustainability, Public Health, Infrastructure*).
* **Named Entity Recognition (NER)**: Leverages a custom **spaCy NER** architecture to precisely extract physical materials, structural constraints, and numerical metrics (e.g., *"20% reduction in carbon emissions"*, *"electric buses"*).
* **Mathematical Prioritization Engine**: Automatically assigns priority scores (High, Medium, Low) to requirements based on urgency, environmental impact, and safety risks, filtering out irrelevant noise (e.g., *"paint the benches blue"*).
* **Monolithic Dashboard**: An ultra-fast, responsive UI built with **React and Tailwind CSS** that utilizes **Virtual Scrolling** (`react-window`) to smoothly render up to 10,000+ AI-processed cards without browser lag.

---

## 📁 Repository Structure

The project is logically divided to separate the NLP intelligence from the frontend user interface:

* **/SPHERE_Codebase/**: The core technical infrastructure.
  * **/Model/**: The Python AI backend containing the DistilBERT sequence classifiers, spaCy NER pipelines, and prioritization scoring logic.
  * **/Frontend/**: The React/Vite web application that renders the requirements dashboard.
  * **/BackEnd/**: The integration layer linking model outputs to the frontend.
* **/Dataset_Sustainability/**: Contains raw, unstructured civil engineering and sustainability CSV/JSON datasets used to demonstrate the model's capabilities.
* **/Training Scripts/**: An archive of the original Python scripts used by the research team to clean data and fine-tune the initial NER and DistilBERT models.

---

## ⚙️ Quick Start

### 1. Launching the Dashboard (Frontend)
The SPHERE UI runs locally on your machine, pulling data directly from the processed model payload.
\\\ash
cd SPHERE_Codebase/Frontend
npm install
npm run dev
\\\
*Navigate to \http://localhost:5173\ in your browser to view the interface.*

### 2. Running the AI Pipeline (Model)
To process new civil engineering datasets through the AI engine and generate new visualizations:
\\\ash
cd SPHERE_Codebase/Model
pip install -r requirements.txt
python run_e2e_validation.py
\\\
*This will ingest your raw text, categorize it, and export a finalized \mockData.json\ for the dashboard to render.*

---

## 🎓 Research Context
This project was developed as an academic software engineering and civil infrastructure thesis, demonstrating how AI can resolve requirements engineering bottlenecks in public planning sectors.

