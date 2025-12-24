from datetime import time, date, timedelta
from typing import List, Tuple
from app.models.schedule_assignment import ScheduleAssignment


def generate_time_slots_for_day(
    start_hour: int = 8,
    end_hour: int = 20,
    slot_duration_minutes: int = 50,
    break_duration_minutes: int = 10
) -> List[Tuple[time, time]]:
    """Generate time slots for a day"""
    slots = []
    current_minutes = start_hour * 60
    
    while current_minutes + slot_duration_minutes <= end_hour * 60:
        start_time = time(
            hour=current_minutes // 60,
            minute=current_minutes % 60
        )
        end_minutes = current_minutes + slot_duration_minutes
        end_time = time(
            hour=end_minutes // 60,
            minute=end_minutes % 60
        )
        slots.append((start_time, end_time))
        
        # Move to next slot (add break duration)
        current_minutes += slot_duration_minutes + break_duration_minutes
    
    return slots


def calculate_total_weekly_hours(
    assignments: List[ScheduleAssignment]
) -> int:
    """Calculate total weekly teaching hours"""
    # Each assignment represents one time slot per week
    # Since time slots are 50 minutes, we count them as 1 hour each
    return len(assignments)


def get_academic_week_number(check_date: date, term_start: date) -> int:
    """Get academic week number (1-based)"""
    if check_date < term_start:
        return 0
    
    delta = check_date - term_start
    week_number = (delta.days // 7) + 1
    return week_number


def is_within_term_dates(
    check_date: date,
    term_start: date,
    term_end: date
) -> bool:
    """Check if date is within term"""
    return term_start <= check_date <= term_end


def time_to_minutes(t: time) -> int:
    """Convert time to minutes since midnight"""
    return t.hour * 60 + t.minute


def minutes_to_time(minutes: int) -> time:
    """Convert minutes since midnight to time"""
    return time(hour=minutes // 60, minute=minutes % 60)


def add_minutes_to_time(t: time, minutes: int) -> time:
    """Add minutes to a time"""
    total_minutes = time_to_minutes(t) + minutes
    return minutes_to_time(total_minutes % (24 * 60))

