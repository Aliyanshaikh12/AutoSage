# Auto Sage — Intelligent Car Fault Diagnosis System

Auto Sage is an explainable, symptom-based Knowledge-Based System (KBS) for automotive fault diagnosis and workshop triage. It uses deterministic propositional logic deduction (*Modus Ponens*) and dynamic technician inquiry to isolate mechanical and electrical vehicle faults with verifiable physical bench testing procedures.

---

## Technologies Used

- **Backend:** Python 3.10+, Flask, REST API
- **Inference Engine:** Deterministic Forward-Chaining Propositional Logic
- **Frontend:** React 18, Vite, Tailwind CSS, Lucide Icons
- **Knowledge Base:** JSON Schema (8 Subsystems, 93 Production Rules, 120 Symptoms, 4 Diagnostic Decision Flowcharts)

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (with npm)

### Option 1: One-Click Startup (Windows)

Double-click `start.bat` in the root folder. This automatically launches both the backend API server (`http://127.0.0.1:5000`) and the Vite frontend (`http://127.0.0.1:5173`), then opens the dashboard in your default web browser.

### Option 2: Manual Startup

#### 1. Backend Setup
```bash
# Activate virtual environment
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate # Linux / macOS

# Install Python dependencies
pip install -r backend/requirements.txt

# Start Flask API server
python backend/app.py
```
*Backend runs on `http://127.0.0.1:5000`.*

#### 2. Frontend Setup
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
*Frontend runs on `http://127.0.0.1:5173`.*

---

## Running Tests

### Backend Test Suite
```bash
# Validate knowledge base integrity and schema
python backend/validate_knowledge_base.py

# Run unittest suite
python -B -m unittest discover -s backend/tests -v
```

### Frontend Test Suite
```bash
npm --prefix frontend test
npm --prefix frontend run build
```

---

## License

This project is licensed under the Creative Commons Attribution 4.0 International License ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
