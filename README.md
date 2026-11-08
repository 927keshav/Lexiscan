# 🧠 LexiScan Auto

**AI-Powered Legal Contract Entity Extractor**

```
PDF Upload → OCR → NER → Postprocessing → JSON Output
```

---

## Project Structure

```
LexiScan_Auto/
├── 1_frontend/          # Member 1 — Web UI (HTML/CSS/JS)
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── README.md
├── 2_backend/           # Member 2 — Flask API
│   ├── app.py
│   └── README.md
├── 3_nlp_engine/        # Member 3 — OCR + NER + Postprocessing
│   ├── ocr_engine.py
│   ├── train_ner.py
│   ├── ner_predict.py
│   ├── postprocessor.py
│   └── README.md
├── 4_devops/            # Member 4 — Docker, Testing, Docs
│   ├── Dockerfile
│   └── README.md
├── sample_pdfs/         # 3 sample legal PDFs
├── requirements.txt     # All dependencies
├── .gitignore
└── README.md            # This file
```

## Team Roles

| Folder | Member | Role |
|--------|--------|------|
| `1_frontend/` | 1 | **Frontend** — Upload UI, results display, responsive design |
| `2_backend/` | 2 | **Backend** — Flask API, routing, pipeline orchestration |
| `3_nlp_engine/` | 3 | **NLP Engine** — OCR, NER model, postprocessing |
| `4_devops/` | 4 | **DevOps** — Docker, testing, CI/CD, documentation |

> Each member works only in their own folder. See individual README for 30-day task plan.

---

## Quick Start

### With Docker (Run once to build)
```powershell
cd D:\Project_zaalima\P1\LexiScan_Auto
docker build -t lexiscan -f 4_devops/Dockerfile .
docker run -d -p 5000:5000 --name lexiscan lexiscan
```

### Daily Usage (After it's built)
```powershell
# To start the app
docker start lexiscan

# Open http://localhost:5000

# To stop the app when done
docker stop lexiscan
```

### Without Docker
```powershell
cd D:\Project_zaalima\P1\LexiScan_Auto
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python 3_nlp_engine/train_ner.py
python 2_backend/app.py
# Open http://localhost:5000
```

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/health` | `{"status": "ok"}` |
| POST | `/extract` | Upload PDF → JSON |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Flask 3.x |
| OCR | Tesseract + PyMuPDF |
| NER | spaCy 3.8+ |
| Container | Docker (python:3.10-slim) |

---

## Commit Rules
- Commit to your own folder only
- Daily commit by 5 PM
- Format: `[role] Day X: description`
