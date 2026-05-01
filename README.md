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

- [Supabase](https://supabase.com) account & project (free tier works)
- Docker & Docker Compose
- OpenAI API Key (optional, fallback mode available)

### 1. Buat Project Supabase

1. Buka [supabase.com](https://supabase.com) → **New project**
2. Setelah project dibuat, buka **SQL Editor** dan jalankan:
   - `database/schema.sql` — buat semua tabel
   - `database/seed.sql` — isi data awal (FAQ, kalender, mata kuliah)
3. Ambil kredensial dari **Project Settings → API**:
   - `SUPABASE_URL` — Project URL (`https://xxxx.supabase.co`)
   - `SUPABASE_KEY` — `anon` public key
4. Ambil connection string dari **Project Settings → Database → Connection String → Transaction pooler** (port 6543) untuk `DATABASE_URL`

### 2. Clone & Configure

```bash
git clone https://github.com/beben-sutara/Chatbot-Akademik.git
cd Chatbot-Akademik
cp .env.example .env
```

Edit `.env` dan isi:

```env
DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=your-supabase-anon-key
OPENAI_API_KEY=your-openai-api-key   # opsional
```

### 3. Run with Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Development Setup (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env dengan kredensial Supabase Anda
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Default Accounts

Daftarkan akun pertama via API:
- `POST /api/v1/auth/register`

Atau gunakan endpoint register di Swagger UI: http://localhost:8000/docs

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
| Database | Supabase (PostgreSQL) |
| ORM | SQLAlchemy |
| Frontend | React + Tailwind CSS |
| Auth | JWT (python-jose) |
| Container | Docker + Docker Compose |

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
