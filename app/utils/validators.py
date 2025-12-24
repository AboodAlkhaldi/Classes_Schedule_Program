import re
from datetime import time
from typing import List


def validate_course_code(code: str) -> bool:
    """Validate course code format (XXX000)"""
    pattern = r"^[A-Z]{3}[0-9]{3}$"
    return bool(re.match(pattern, code))


def validate_classroom_code(code: str) -> bool:
    """Validate classroom code format (alphanumeric with optional dash/building prefix)"""
    pattern = r"^[A-Z0-9\-]+$"
    return bool(re.match(pattern, code)) and len(code) <= 20


def validate_term_name(name: str) -> bool:
    """Validate term name format (YYYY-YYYY Season)"""
    pattern = r"^20\d{2}-20\d{2} (Spring|Fall)$"
    if not re.match(pattern, name):
        return False
    
    # Check that second year = first year + 1
    years = name.split("-")
    first_year = int(years[0])
    second_year = int(years[1].split()[0])
    return second_year == first_year + 1


def validate_email_domain(email: str, allowed_domains: List[str]) -> bool:
    """Validate email is from allowed domain"""
    if "@" not in email:
        return False
    domain = email.split("@")[1]
    return domain.lower() in [d.lower() for d in allowed_domains]


def validate_time_slot_duration(start_time: time, end_time: time) -> bool:
    """Validate time slot is exactly 50 minutes"""
    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute
    duration = end_minutes - start_minutes
    return duration == 50


def validate_weekly_hours_for_type(hours: int, course_type: str) -> bool:
    """Validate weekly hours match course type conventions"""
    if course_type == "theory":
        return 2 <= hours <= 4
    elif course_type == "lab":
        return 2 <= hours <= 6
    elif course_type == "practice":
        return 1 <= hours <= 3
    return False


def validate_faculty_code(code: str) -> bool:
    """Validate faculty code format (exactly 3 uppercase letters)"""
    pattern = r"^[A-Z]{3}$"
    return bool(re.match(pattern, code))


def validate_department_code(code: str) -> bool:
    """Validate department code format (exactly 3 uppercase letters)"""
    pattern = r"^[A-Z]{3}$"
    return bool(re.match(pattern, code))

