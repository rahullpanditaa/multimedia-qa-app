# Multimedia QA Web Application

An AI-powered full-stack application that allows users to upload PDF documents, audio, and video files, and interact with them through natural language.

Users can:

* Upload PDFs, MP3s, and videos
* Ask questions about uploaded content using Retrieval-Augmented Generation (RAG)
* Generate summaries
* Extract topic-specific timestamps from audio/video
* Play the relevant portion of media files
* Register and log in with JWT-based authentication

---

## Features

### Document and Media Upload
* Upload PDF documents
* Upload audio files (e.g. MP3)
* Upload video files
* Automatic file type detection

### AI-Powered Q&A
* Ask questions about uploaded files
* Semantic retrieval using vector embeddings and pgvector
* LLM-generated answers
* Streaming responses in the chat interface

### Summarization
* Generate concise summaries of uploaded documents and transcripts
* Redis caching for faster repeated summary requests

### Timestamp Extraction
* Identify where specific topics appear in audio/video transcripts
* Display start and end timestamps
* Show transcript snippets

### Media Playback
* Play the exact portion of audio/video associated with timestamp results

### Authentication and Authorization
* User registration and login
* JWT-based authentication
* Per-user document ownership and access control

### Infrastructure and DevOps
* Dockerized backend and frontend
* Docker Compose orchestration
* PostgreSQL with pgvector
* Redis for caching
* GitHub Actions CI
* Automated tests with 95%+ coverage

---

## Architecture Overview

```text
React Frontend
    |
    v
FastAPI Backend
    |
    +--> PostgreSQL + pgvector
    |
    +--> Redis
    |
    +--> Whisper / Speech-to-Text
    |
    +--> Embedding Model
    |
    +--> LLM (Ollama or API-based)
```

---

## Tech Stack

### Frontend
* React
* Vite
* Axios

### Backend
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

### AI / ML
* Sentence Transformers
* Whisper (speech-to-text)
* LLM via Ollama (default)

### Data Stores
* PostgreSQL
* pgvector
* Redis

### DevOps
* Docker
* Docker Compose
* GitHub Actions
* pytest + pytest-cov

---

## Project Structure

```text
multimedia-qa-web-app/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   └── pages/
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## Prerequisites
* Docker
* Docker Compose

Optional for local development without Docker:

* Python 3.12+
* Node.js 20+
* npm

---

## Quick Start (Recommended)

From the repository root:

```bash
docker compose up --build
```

This starts:
* Frontend
* Backend
* PostgreSQL
* Redis

### Application URLs

| Service      | URL                                                      |
| ------------ | -------------------------------------------------------- |
| Frontend     | [http://localhost:5173](http://localhost:5173)           |
| Backend API  | [http://localhost:8000](http://localhost:8000)           |
| Swagger Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |

---

## First-Time Setup

### 1. Register a User
Open the frontend and create an account.

### 2. Log In
Log in with your credentials.

### 3. Upload Files
Upload a PDF, MP3, or video.

### 4. Use the Application
* Ask questions
* Generate summaries
* Find timestamps
* Play relevant media segments

---

## Local Development (Without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

### Backend `.env`

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/qa_rag_app
REDIS_URL=redis://localhost:6379/0
LLM_PROVIDER=ollama
SECRET_KEY=change-this-in-production
```

---

## Database Migrations

Run from the `backend/` directory:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## Running Tests

From `backend/`:

```bash
pytest --cov=app --cov-report=term-missing
```

Target coverage:

```text
95%+
```

---

## CI/CD

GitHub Actions automatically:

* Installs dependencies
* Starts PostgreSQL
* Enables pgvector
* Runs Alembic migrations
* Executes tests with coverage

Workflow file:

```text
.github/workflows/ci.yml
```

---

## API Endpoints

### Authentication

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| POST   | `/auth/register` | Register a new user |
| POST   | `/auth/login`    | Obtain JWT token    |

### Documents

| Method | Endpoint      | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | `/documents/` | List current user's documents |

### Upload

| Method | Endpoint        | Description        |
| ------ | --------------- | ------------------ |
| POST   | `/upload/`      | Upload PDF         |
| POST   | `/media/upload` | Upload audio/video |

### AI Features

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| POST   | `/chat/`                 | Ask a question     |
| POST   | `/chat/stream`           | Streaming chat     |
| GET    | `/summary/{document_id}` | Generate summary   |
| POST   | `/timestamps/`           | Extract timestamps |

---

## Retrieval-Augmented Generation (RAG) Pipeline

### PDF Workflow

1. Upload PDF
2. Extract text
3. Chunk text
4. Generate embeddings
5. Store vectors in PostgreSQL
6. Retrieve relevant chunks
7. Generate answer with LLM

### Audio/Video Workflow

1. Upload media
2. Transcribe with Whisper
3. Store transcript segments with timestamps
4. Search transcript for relevant windows
5. Return timestamps and snippets

---

## Caching with Redis

Document summaries are cached in Redis.

### Cache Key Format

```text
summary:<document_id>
```

### Benefits

* Faster repeated summary requests
* Reduced LLM calls
* Lower computational cost

---

## Security

* Passwords hashed using bcrypt
* JWT authentication
* Protected API endpoints
* Per-user document ownership

---

## Docker Services

Defined in `docker-compose.yml`:

* `frontend`
* `backend`
* `postgres`
* `redis`

---

<!-- ## Demo Walkthrough

A walkthrough video demonstrating:

* Registration and login
* File upload
* Chat
* Summaries
* Timestamp extraction
* Media playback
* Code overview

**Demo Video:** Add your YouTube or Google Drive link here. -->

---

<!-- ## Optional Deployment

Suggested deployment stack:

* Frontend: Vercel
* Backend: Render
* Database: Neon or Render PostgreSQL
* Redis: Upstash or Render Redis

---

## Future Improvements

* Redis-based rate limiting
* Cloud deployment
* OAuth login
* Document deletion
* Background job processing
* Responsive mobile UI

--- -->

## Sample Use Cases

### PDF Q&A

Upload a research paper and ask:

* "What is the main conclusion?"
* "Summarize section 3."

### Audio Timestamp Search

Upload a podcast and ask:

* "Where do they discuss machine learning?"

### Video Analysis

Upload a lecture and ask:

* "When does the instructor explain backpropagation?"

<!-- ---

## Author

Rahul Pandita

---

## License

This project was developed as part of an SDE-1 programming assignment. -->
