# Chandas — Sanskrit Meter Identification & Translator

> **छन्दांसि जगतां पदवीम्** — Meters are the footsteps of the universe

A web application that identifies **Sanskrit poetic meters (Chandas)** from input text or scanned images, provides detailed prosodic analysis (syllable breakdown, Laghu-Guru patterns, Gaṇa notation, sandhi analysis), and translates Sanskrit text to **Hindi and English** with word-by-word analysis.

## Features

- 🔍 **Chandas Identification** — Custom-built 3-tier engine (exact match → fuzzy search → LSTM)
- 📝 **Sandhi Analysis** — Rule-based splitter covering 45+ sandhi rules
- 🔤 **Sanskrit Translator** — Padaccheda (word-by-word analysis) + full translation
- 📸 **Image OCR** — Gemini Vision + Tesseract with meter-aware correction
- 📚 **Meter Encyclopedia** — Browse 200+ Sanskrit meters
- 👤 **User Dashboard** — Save and review past analyses

## Tech Stack

| Layer | Technologies |
|:---|:---|
| **Frontend** | React 18, Vite 5, React Router v6, Framer Motion, Axios |
| **Backend** | Python 3.11, Flask 3.x, SQLAlchemy, Gunicorn |
| **NLP Engine** | Custom syllable parser, L-G classifier, Sandhi splitter, PyTorch LSTM |
| **AI/OCR** | Google Gemini API, Groq API, Tesseract 5, OpenCV |
| **Database** | PostgreSQL (Render), SQLite (dev) |
| **Deployment** | Render (Backend), Vercel (Frontend) |

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Tesseract OCR (optional, for local OCR testing)

### Backend Setup

```bash
cd server
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # macOS/Linux
pip install -r requirements.txt

# Copy and fill in environment variables
copy ..\.env.example .env
# Edit .env with your API keys

# Run development server
python run.py
```

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and the backend at `http://localhost:5000`.

## Project Structure

```
chandas-project/
├── client/          # React + Vite Frontend
├── server/          # Flask Backend
│   ├── app/         # Flask application
│   │   ├── models/  # Database models
│   │   ├── routes/  # API endpoints
│   │   ├── services/# Business logic
│   │   └── utils/   # Utility functions
│   ├── data/        # Meter DB, sandhi rules, training data
│   ├── ml/          # LSTM model training
│   └── tests/       # Test suite
├── notebooks/       # Google Colab notebooks
├── docs/            # Project documentation
└── scripts/         # Build & evaluation scripts
```

## API Endpoints

| Endpoint | Method | Description |
|:---|:---|:---|
| `/api/health` | GET | Health check |
| `/api/chandas/analyze` | POST | Full meter analysis |
| `/api/chandas/meters` | GET | List all meters |
| `/api/chandas/syllabify` | POST | Syllable breakdown |
| `/api/translate` | POST | Simple translation |
| `/api/translate/padaccheda` | POST | Word-by-word analysis |
| `/api/ocr/extract` | POST | Image text extraction |
| `/api/auth/register` | POST | User registration |
| `/api/auth/login` | POST | User login |
| `/api/history` | GET | Analysis history |

## Timeline

- **Phase 0** (Aug 2026): Project setup ✅
- **Phase 1** (Sep-Oct 2026): Custom Chandas engine
- **Phase 2** (Oct 2026): Sandhi analysis module
- **Phase 3** (Oct-Nov 2026): Frontend UI
- **Phase 4** (Nov-Dec 2026): Translation with Padaccheda
- **Phase 5** (Dec 2026): OCR with meter-aware correction
- **Phase 6** (Jan 2027): User system & history
- **Phase 7** (Jan 2027): LSTM classifier training
- **Phase 8** (Feb 2027): Evaluation & polish
- **Phase 9** (Feb-Mar 2027): Deployment & documentation

## License

MIT
