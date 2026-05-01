# 🎓 Chatbot Akademik

Chatbot Agent dengan AI untuk Layanan Akademik Kampus — membantu mahasiswa dan staff dengan informasi jadwal kuliah, nilai, kalender akademik, registrasi, dan konsultasi akademik.

## ✨ Fitur Utama

- 🤖 **AI Chatbot** — Natural language processing dengan LangChain + OpenAI
- 📅 **Jadwal Kuliah** — Informasi jadwal perkuliahan real-time
- 📊 **Nilai & IPK** — Cek nilai dan indeks prestasi
- 📆 **Kalender Akademik** — Event dan jadwal akademik kampus
- ❓ **FAQ Akademik** — Jawaban otomatis untuk pertanyaan umum
- 🔐 **Autentikasi** — Login berbasis JWT untuk mahasiswa dan staff
- 💬 **Chat History** — Riwayat percakapan tersimpan

## 🏗️ Arsitektur

```
chatbot-akademik/
├── backend/          # FastAPI REST API
│   └── app/
│       ├── models/   # SQLAlchemy database models
│       ├── routes/   # API endpoints
│       ├── schemas/  # Pydantic schemas
│       ├── services/ # Business logic & AI service
│       └── utils/    # Auth utilities
├── frontend/         # React + Tailwind CSS
│   └── src/
│       ├── pages/    # LoginPage, ChatPage
│       ├── context/  # AuthContext
│       └── services/ # API client
├── ai-agent/         # LangChain AI agent (standalone)
├── database/         # SQL schema & seed data
├── docs/             # API documentation
└── docker-compose.yml
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key (optional, fallback mode available)

### 1. Clone & Configure

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

### 2. Run with Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 3. Development Setup (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Default Accounts

After running seeds, you can register a new account via:
- `POST /api/v1/auth/register`

Or use the register endpoint to create your first user.

## 🤖 AI Configuration

The chatbot works in two modes:

1. **With OpenAI** — Set `OPENAI_API_KEY` in `.env` for full LLM capabilities
2. **Fallback mode** — Rule-based responses when no API key is set (great for development)

## 📚 API Documentation

- Interactive docs: http://localhost:8000/docs (Swagger UI)
- Full API reference: [docs/API.md](docs/API.md)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| AI/LLM | LangChain + OpenAI GPT |
| Database | PostgreSQL + SQLAlchemy |
| Frontend | React + Tailwind CSS |
| Auth | JWT (python-jose) |
| Container | Docker + Docker Compose |

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
