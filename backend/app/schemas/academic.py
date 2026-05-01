from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, time


class CourseOut(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int
    semester: Optional[int]
    deskripsi: Optional[str]

    class Config:
        from_attributes = True


class ScheduleOut(BaseModel):
    id: int
    hari: Optional[str]
    jam_mulai: Optional[time]
    jam_selesai: Optional[time]
    ruangan: Optional[str]
    dosen: Optional[str]
    semester_tahun: Optional[str]
    course: CourseOut

    class Config:
        from_attributes = True


class GradeOut(BaseModel):
    id: int
    nilai_angka: Optional[float]
    nilai_huruf: Optional[str]
    semester: Optional[str]
    course: CourseOut

    class Config:
        from_attributes = True


class AcademicCalendarOut(BaseModel):
    id: int
    judul: str
    deskripsi: Optional[str]
    tanggal_mulai: date
    tanggal_selesai: Optional[date]
    kategori: Optional[str]

    class Config:
        from_attributes = True


class FAQOut(BaseModel):
    id: int
    pertanyaan: str
    jawaban: str
    kategori: Optional[str]

    class Config:
        from_attributes = True
