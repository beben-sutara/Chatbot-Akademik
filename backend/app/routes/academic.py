from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User
from ..models.academic import Schedule, Grade, AcademicCalendar, FAQ, Course
from ..schemas.academic import ScheduleOut, GradeOut, AcademicCalendarOut, FAQOut, CourseOut
from ..utils.auth import get_current_user

router = APIRouter(prefix="/academic", tags=["Academic"])


@router.get("/schedules", response_model=List[ScheduleOut])
def get_schedules(
    semester_tahun: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Schedule).filter(Schedule.student_id == current_user.id)
    if semester_tahun:
        query = query.filter(Schedule.semester_tahun == semester_tahun)
    return query.all()


@router.get("/grades", response_model=List[GradeOut])
def get_grades(
    semester: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Grade).filter(Grade.student_id == current_user.id)
    if semester:
        query = query.filter(Grade.semester == semester)
    return query.all()


@router.get("/calendar", response_model=List[AcademicCalendarOut])
def get_calendar(
    kategori: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(AcademicCalendar).order_by(AcademicCalendar.tanggal_mulai)
    if kategori:
        query = query.filter(AcademicCalendar.kategori == kategori)
    return query.all()


@router.get("/faqs", response_model=List[FAQOut])
def get_faqs(
    kategori: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(FAQ).filter(FAQ.is_active == 1)
    if kategori:
        query = query.filter(FAQ.kategori == kategori)
    return query.all()


@router.get("/courses", response_model=List[CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
