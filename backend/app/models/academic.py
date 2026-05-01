from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Float, Enum, Time, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base


class DayOfWeek(str, enum.Enum):
    senin = "Senin"
    selasa = "Selasa"
    rabu = "Rabu"
    kamis = "Kamis"
    jumat = "Jumat"
    sabtu = "Sabtu"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    kode_mk = Column(String(20), unique=True, index=True, nullable=False)
    nama_mk = Column(String(255), nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer)
    deskripsi = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    schedules = relationship("Schedule", back_populates="course")
    grades = relationship("Grade", back_populates="course")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    hari = Column(Enum(DayOfWeek))
    jam_mulai = Column(Time)
    jam_selesai = Column(Time)
    ruangan = Column(String(50))
    dosen = Column(String(200))
    semester_tahun = Column(String(20))

    student = relationship("User", back_populates="schedules")
    course = relationship("Course", back_populates="schedules")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    nilai_angka = Column(Float)
    nilai_huruf = Column(String(5))
    semester = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("User", back_populates="grades")
    course = relationship("Course", back_populates="grades")


class AcademicCalendar(Base):
    __tablename__ = "academic_calendar"

    id = Column(Integer, primary_key=True, index=True)
    judul = Column(String(255), nullable=False)
    deskripsi = Column(Text)
    tanggal_mulai = Column(Date, nullable=False)
    tanggal_selesai = Column(Date)
    kategori = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    pertanyaan = Column(Text, nullable=False)
    jawaban = Column(Text, nullable=False)
    kategori = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
