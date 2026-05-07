# Multimedia RAG Web Application

AI-powered document and multimedia question-answering application built with FastAPI, React, PostgreSQL, pgvector, Ollama, and Whisper.

Users can:
- Upload PDFs, audio, and video files
- Ask questions about uploaded content
- Generate summaries
- Retrieve timestamps for specific topics in media
- Play relevant media sections directly from semantic search results

---

# Features

## Document Processing
- PDF upload + text extraction
- Automatic text chunking
- Vector embeddings using local LLM embeddings
- Semantic retrieval with pgvector

## Multimedia Processing
- Audio/video upload
- Whisper-based transcription
- Timestamp extraction
- Timestamp-based playback

## AI Features
- Retrieval-Augmented Generation (RAG)
- Semantic search
- AI summaries
- Context-aware chatbot

## Frontend
- React + Vite UI
- File upload interface
- Chat interface
- Summary generation UI
- Timestamp search UI
- Media playback UI

## Backend
- FastAPI REST API
- PostgreSQL + pgvector
- SQLAlchemy ORM
- Alembic migrations

## Infrastructure
- Docker + Docker Compose
- GitHub Actions CI/CD
- Automated tests with 95% coverage

---

# Tech Stack

## Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Alembic

## AI / ML
- Ollama
- Mistral
- nomic-embed-text
- Faster-Whisper

## Frontend
- React
- Vite
- Axios

## DevOps
- Docker
- Docker Compose
- GitHub Actions
- Pytest


---

# Project Structure

```text
backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── tests/
│
├── alembic/
│
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── api/
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd multimedia-qa-web-app
```

---

# 2. Start PostgreSQL

```bash
docker compose up -d
```

---

# 3. Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 4. Configure Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/rag_app
```

---

# 5. Run Database Migrations

```bash
alembic upgrade head
```

---

# 6. Start Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# 7. Frontend Setup

```bash
cd frontend

npm install
```

Start frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run coverage:

```bash
pytest --cov=app
```

Current coverage:

```text
95%
```

---

# API Endpoints

## Upload PDF

```http
POST /upload/pdf
```

## Upload Media

```http
POST /media/upload
```

## Chat

```http
POST /chat/
```

## Generate Summary

```http
POST /summary/{document_id}
```

## Timestamp Search

```http
POST /timestamps/
```

---

# Example Workflow

1. Upload PDF/audio/video
2. Generate embeddings/transcripts
3. Ask questions
4. Retrieve semantic answers
5. Generate summaries
6. Search timestamps
7. Play relevant media section