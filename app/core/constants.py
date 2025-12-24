from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    DEAN = "dean"
    DEPARTMENT_REP = "department_rep"


class InstructorTitle(str, Enum):
    PROF_DR = "Prof. Dr."
    DOC_DR = "Doç. Dr."
    DR_OGR_UYESI = "Dr. Öğr. Üyesi"
    OGR_GOR = "Öğr. Gör."
    ARS_GOR = "Arş. Gör."


class ClassLevel(str, Enum):
    FIRST = "1st"
    SECOND = "2nd"
    THIRD = "3rd"
    FOURTH = "4th"


class ClassLabel(str, Enum):
    FIRST_YEAR = "I. Year"
    SECOND_YEAR = "II. Year"
    THIRD_YEAR = "III. Year"
    FOURTH_YEAR = "IV. Year"


class CourseLevel(str, Enum):
    FIRST_YEAR = "1.Year"
    SECOND_YEAR = "2.Year"
    THIRD_YEAR = "3.Year"
    FOURTH_YEAR = "4.Year"


class CourseType(str, Enum):
    THEORY = "theory"
    LAB = "lab"
    PRACTICE = "practice"


class ClassroomType(str, Enum):
    CLASSROOM = "classroom"
    AMPHI = "amphi"
    LAB = "lab"


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class ScheduleStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReviewNoteType(str, Enum):
    CONFLICT = "conflict"
    SUGGESTION = "suggestion"
    APPROVAL = "approval"
    REJECTION = "rejection"


# Mapping between class_level and label
CLASS_LEVEL_TO_LABEL = {
    ClassLevel.FIRST: ClassLabel.FIRST_YEAR,
    ClassLevel.SECOND: ClassLabel.SECOND_YEAR,
    ClassLevel.THIRD: ClassLabel.THIRD_YEAR,
    ClassLevel.FOURTH: ClassLabel.FOURTH_YEAR,
}

