# Chatbot Akademik API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "nim_nip": "12345678",
  "full_name": "Budi Santoso",
  "email": "budi@kampus.ac.id",
  "password": "password123",
  "role": "mahasiswa"
}
```

### POST /auth/login
Login and get JWT token.

**Request Body:**
```json
{
  "nim_nip": "12345678",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { ... }
}
```

## Academic Endpoints (requires Bearer token)

### GET /academic/schedules
Get student's class schedules.

**Query params:** `semester_tahun` (optional)

### GET /academic/grades
Get student's grades.

**Query params:** `semester` (optional)

### GET /academic/calendar
Get academic calendar events.

**Query params:** `kategori` (optional)

### GET /academic/faqs
Get FAQ list.

**Query params:** `kategori` (optional)

### GET /academic/courses
Get all available courses.

## Chat Endpoints (requires Bearer token)

### POST /chat/
Send a message to the AI chatbot.

**Request Body:**
```json
{
  "message": "Tampilkan jadwal kuliah saya",
  "session_id": null
}
```

**Response:**
```json
{
  "session_id": 1,
  "message": "Berikut jadwal kuliah Anda...",
  "role": "assistant"
}
```

### GET /chat/sessions
List all chat sessions.

### GET /chat/sessions/{session_id}
Get messages in a chat session.

### DELETE /chat/sessions/{session_id}
Delete a chat session.
