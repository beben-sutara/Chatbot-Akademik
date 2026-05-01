"""
LangChain Tools untuk Chatbot Akademik
"""
from langchain_core.tools import tool
from typing import Optional


@tool
def get_academic_schedule(student_id: int, semester: Optional[str] = None) -> str:
    """Mendapatkan jadwal kuliah mahasiswa berdasarkan ID dan semester."""
    return f"Jadwal kuliah untuk mahasiswa ID {student_id} semester {semester or 'aktif'} akan ditampilkan dari database."


@tool
def get_student_grades(student_id: int, semester: Optional[str] = None) -> str:
    """Mendapatkan nilai mahasiswa berdasarkan ID dan semester."""
    return f"Nilai mahasiswa ID {student_id} semester {semester or 'semua'} akan ditampilkan dari database."


@tool
def get_academic_calendar(kategori: Optional[str] = None) -> str:
    """Mendapatkan kalender akademik kampus."""
    return f"Kalender akademik kategori {kategori or 'semua'} akan ditampilkan dari database."


@tool
def search_faq(query: str) -> str:
    """Mencari jawaban dari FAQ akademik berdasarkan pertanyaan."""
    return f"Mencari FAQ untuk: {query}"


@tool
def get_registration_info(process_type: str) -> str:
    """Mendapatkan informasi tentang proses registrasi akademik (KRS, cuti, dll)."""
    processes = {
        "krs": "Pengisian KRS dilakukan melalui portal akademik pada awal semester.",
        "cuti": "Pengajuan cuti akademik memerlukan formulir yang ditandatangani dosen wali.",
        "transkrip": "Permohonan transkrip nilai diajukan ke bagian akademik.",
        "wisuda": "Pendaftaran wisuda dilakukan 2 bulan sebelum pelaksanaan.",
    }
    return processes.get(process_type.lower(), f"Informasi untuk proses {process_type} tidak tersedia.")


ACADEMIC_TOOLS = [
    get_academic_schedule,
    get_student_grades,
    get_academic_calendar,
    search_faq,
    get_registration_info,
]
