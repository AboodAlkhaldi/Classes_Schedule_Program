# Import all models for Alembic to detect them
from app.models.base import Base, BaseModel, TimestampMixin, IDMixin, SoftDeleteMixin
from app.models.faculty import Faculty
from app.models.department import Department
from app.models.term import Term
from app.models.user import User
from app.models.instructor import Instructor
from app.models.instructor_availability import InstructorAvailability
from app.models.program_class import ProgramClass
from app.models.course import Course
from app.models.course_offering import CourseOffering
from app.models.classroom import Classroom
from app.models.time_slot import TimeSlot
from app.models.schedule import Schedule
from app.models.schedule_assignment import ScheduleAssignment
from app.models.schedule_review_note import ScheduleReviewNote

__all__ = [
    "Base",
    "BaseModel",
    "TimestampMixin",
    "IDMixin",
    "SoftDeleteMixin",
    "Faculty",
    "Department",
    "Term",
    "User",
    "Instructor",
    "InstructorAvailability",
    "ProgramClass",
    "Course",
    "CourseOffering",
    "Classroom",
    "TimeSlot",
    "Schedule",
    "ScheduleAssignment",
    "ScheduleReviewNote",
]

