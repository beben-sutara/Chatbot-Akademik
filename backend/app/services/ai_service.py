from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.chat import ChatMessage, MessageRole
from ..models.user import User
from ..models.academic import FAQ, AcademicCalendar, Schedule, Grade
from ..config import settings


SYSTEM_PROMPT = """Anda adalah asisten akademik yang membantu mahasiswa dan staff kampus.
Nama Anda adalah "Akad" - Asisten Akademik Digital.

Tugas Anda:
1. Menjawab pertanyaan tentang jadwal kuliah, nilai, dan kalender akademik
2. Membantu proses registrasi dan pendaftaran mata kuliah
3. Memberikan informasi layanan mahasiswa
4. Menjawab FAQ akademik
5. Memberikan konsultasi akademik secara ramah dan profesional

Gunakan bahasa Indonesia yang sopan dan mudah dipahami.
Jika Anda tidak memiliki informasi yang diminta, arahkan mahasiswa untuk menghubungi bagian akademik langsung.
"""


async def get_ai_response(
    message: str,
    history: List[ChatMessage],
    user: User,
    db: Session,
) -> str:
    # Gather context from database
    context = _build_context(message, user, db)

    if settings.openai_api_key:
        return await _get_openai_response(message, history, context)
    else:
        return _get_fallback_response(message, context, db)


def _build_context(message: str, user: User, db: Session) -> str:
    context_parts = [f"Pengguna: {user.full_name} ({user.role})"]
    msg_lower = message.lower()

    if any(k in msg_lower for k in ["jadwal", "kuliah", "schedule", "kelas"]):
        schedules = db.query(Schedule).filter(Schedule.student_id == user.id).limit(10).all()
        if schedules:
            sched_info = "\n".join(
                f"- {s.course.nama_mk}: {s.hari} {s.jam_mulai}-{s.jam_selesai}, Ruangan: {s.ruangan}, Dosen: {s.dosen}"
                for s in schedules
            )
            context_parts.append(f"Jadwal kuliah:\n{sched_info}")

    if any(k in msg_lower for k in ["nilai", "grade", "ipk", "ip"]):
        grades = db.query(Grade).filter(Grade.student_id == user.id).limit(10).all()
        if grades:
            grade_info = "\n".join(
                f"- {g.course.nama_mk}: {g.nilai_huruf} ({g.nilai_angka}), Semester: {g.semester}"
                for g in grades
            )
            context_parts.append(f"Nilai:\n{grade_info}")

    if any(k in msg_lower for k in ["kalender", "akademik", "event", "kegiatan"]):
        events = db.query(AcademicCalendar).order_by(AcademicCalendar.tanggal_mulai).limit(5).all()
        if events:
            cal_info = "\n".join(
                f"- {e.judul}: {e.tanggal_mulai} s/d {e.tanggal_selesai or '-'}"
                for e in events
            )
            context_parts.append(f"Kalender Akademik:\n{cal_info}")

    return "\n\n".join(context_parts)


async def _get_openai_response(message: str, history: List[ChatMessage], context: str) -> str:
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

        llm = ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.7,
        )

        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        if context:
            messages.append(SystemMessage(content=f"Konteks data pengguna:\n{context}"))

        for msg in history[-10:]:
            if msg.role == MessageRole.user:
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.assistant:
                messages.append(AIMessage(content=msg.content))

        response = await llm.ainvoke(messages)
        return response.content
    except Exception as e:
        return f"Maaf, terjadi kesalahan pada layanan AI. Silakan coba lagi. ({str(e)})"


def _get_fallback_response(message: str, context: str, db: Session) -> str:
    msg_lower = message.lower()

    # Check FAQ
    faqs = db.query(FAQ).filter(FAQ.is_active == True).all()  # noqa: E712
    for faq in faqs:
        keywords = faq.pertanyaan.lower().split()
        if any(kw in msg_lower for kw in keywords if len(kw) > 3):
            return f"📚 **{faq.pertanyaan}**\n\n{faq.jawaban}"

    if "jadwal" in msg_lower or "kuliah" in msg_lower:
        if "Jadwal kuliah:" in context:
            lines = [l for l in context.split("\n") if "Jadwal kuliah:" in l or l.startswith("- ")]
            return "📅 **Jadwal Kuliah Anda:**\n" + "\n".join(lines[1:]) if len(lines) > 1 else "Jadwal kuliah Anda belum tersedia."
        return "Maaf, jadwal kuliah Anda belum tersedia di sistem. Silakan hubungi bagian akademik."

    if "nilai" in msg_lower or "grade" in msg_lower:
        if "Nilai:" in context:
            lines = [l for l in context.split("\n") if "Nilai:" in l or l.startswith("- ")]
            return "📊 **Nilai Anda:**\n" + "\n".join(lines[1:]) if len(lines) > 1 else "Nilai Anda belum tersedia."
        return "Maaf, nilai Anda belum tersedia di sistem. Silakan hubungi bagian akademik."

    if "kalender" in msg_lower or "kegiatan" in msg_lower:
        if "Kalender Akademik:" in context:
            lines = [l for l in context.split("\n") if "Kalender" in l or l.startswith("- ")]
            return "📆 **Kalender Akademik:**\n" + "\n".join(lines[1:]) if len(lines) > 1 else "Kalender akademik belum tersedia."
        return "Maaf, kalender akademik belum tersedia."

    if any(k in msg_lower for k in ["halo", "hai", "hello", "hi", "selamat"]):
        return f"Halo! 👋 Saya **Akad**, asisten akademik digital Anda. Saya siap membantu Anda dengan:\n\n• 📅 Jadwal kuliah\n• 📊 Informasi nilai\n• 📆 Kalender akademik\n• ❓ FAQ akademik\n• 🎓 Konsultasi akademik\n\nApa yang bisa saya bantu hari ini?"

    if "registrasi" in msg_lower or "daftar" in msg_lower or "krs" in msg_lower:
        return "📝 **Informasi Registrasi:**\n\nUntuk proses registrasi/KRS, silakan:\n1. Login ke portal akademik\n2. Pilih menu 'Pengisian KRS'\n3. Pilih mata kuliah yang tersedia\n4. Konfirmasi dengan dosen wali\n\nJika mengalami kendala, hubungi bagian akademik di gedung rektorat lantai 2."

    if "bantuan" in msg_lower or "help" in msg_lower or "apa" in msg_lower:
        return "🤖 **Saya bisa membantu Anda dengan:**\n\n• Cek jadwal kuliah\n• Lihat nilai/IPK\n• Kalender akademik\n• Proses registrasi/KRS\n• FAQ akademik\n• Informasi layanan mahasiswa\n\nKetik pertanyaan Anda dan saya akan membantu!"

    return "Halo! 👋 Saya **Akad**, asisten akademik Anda. Saya belum memahami pertanyaan Anda. Bisa Anda ulangi atau tanyakan hal lain? Ketik **'bantuan'** untuk melihat apa yang bisa saya bantu."
