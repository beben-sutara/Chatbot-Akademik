# Chatbot Akademik 🎓

Asisten virtual berbasis web untuk **Layanan Akademik Kampus**. Chatbot ini membantu mahasiswa dan calon mahasiswa mendapatkan informasi akademik secara cepat dan mudah.

## Tampilan

| Tampilan Awal | Contoh Percakapan |
|---|---|
| ![Initial](https://github.com/user-attachments/assets/1a29970f-7639-4506-8e5c-61efd27781e6) | ![Conversation](https://github.com/user-attachments/assets/95506949-a3b1-41be-959d-23908b023160) |

## Fitur

- 💬 **Antarmuka web** yang responsif dan ramah pengguna
- 🎯 **Quick-action buttons** untuk topik yang sering ditanyakan
- 📚 **Mencakup 20+ topik akademik**, antara lain:
  - Pendaftaran mahasiswa baru (PMB/SNBP/SNBT/Mandiri)
  - Biaya kuliah & UKT
  - Beasiswa (KIP-Kuliah, prestasi, industri, luar negeri)
  - Jadwal kuliah & Kalender Akademik
  - KRS (Kartu Rencana Studi)
  - Nilai & IPK
  - Wisuda & Skripsi/Tugas Akhir
  - Perpustakaan & Fasilitas kampus
  - Program Studi & Fakultas
  - PKL/Magang & Organisasi Mahasiswa
  - Cuti akademik & Transfer mahasiswa
  - Informasi kontak kampus

## Teknologi

- **Backend**: Python 3 + Flask
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Metode**: Intent-based matching dengan pencocokan kata kunci berbahasa Indonesia

## Instalasi & Menjalankan

```bash
# 1. Clone repository
git clone https://github.com/beben-sutara/Chatbot-Akademik.git
cd Chatbot-Akademik

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi
python app.py
```

Buka browser dan akses **http://127.0.0.1:5000**

## Struktur Proyek

```
Chatbot-Akademik/
├── app.py                  # Flask web application
├── chatbot.py              # Logika inti chatbot (intent matching)
├── requirements.txt        # Dependensi Python
├── data/
│   └── intents.json        # Data intent & respons akademik
├── templates/
│   └── index.html          # Tampilan antarmuka web
├── static/
│   ├── style.css           # Stylesheet
│   └── script.js           # JavaScript client
└── tests/
    └── test_chatbot.py     # Unit tests
```

## Menjalankan Tests

```bash
pytest tests/ -v
```

## API

### `POST /chat`

**Request:**
```json
{ "message": "informasi beasiswa" }
```

**Response:**
```json
{ "response": "Kampus menyediakan berbagai program beasiswa..." }
```
