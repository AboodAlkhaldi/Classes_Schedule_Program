from datetime import time, date
from typing import List, Dict


def check_time_overlap(
    slot1_start: time,
    slot1_end: time,
    slot2_start: time,
    slot2_end: time
) -> bool:
    """Check if two time slots overlap"""
    slot1_start_minutes = slot1_start.hour * 60 + slot1_start.minute
    slot1_end_minutes = slot1_end.hour * 60 + slot1_end.minute
    slot2_start_minutes = slot2_start.hour * 60 + slot2_start.minute
    slot2_end_minutes = slot2_end.hour * 60 + slot2_end.minute
    
    # Check if slots overlap
    return not (slot1_end_minutes <= slot2_start_minutes or slot2_end_minutes <= slot1_start_minutes)


def check_date_range_overlap(
    range1_start: date,
    range1_end: date,
    range2_start: date,
    range2_end: date
) -> bool:
    """Check if two date ranges overlap"""
    return not (range1_end < range2_start or range2_end < range1_start)


def calculate_conflict_severity(conflict_type: str) -> int:
    """Calculate severity score for conflict type (0-100)"""
    severity_map = {
        "instructor_double_booking": 100,
        "classroom_double_booking": 90,
        "student_group_conflict": 85,
        "capacity_exceeded": 80,
        "instructor_unavailable": 75,
        "classroom_unavailable": 70,
        "weekly_load_exceeded": 60,
        "preference_violation": 40,
        "suggestion": 20,
    }
    return severity_map.get(conflict_type, 50)


def group_conflicts_by_type(
    conflicts: List[Dict]
) -> Dict[str, List[Dict]]:
    """Group conflicts by type for reporting"""
    grouped = {}
    for conflict in conflicts:
        conflict_type = conflict.get("type", "unknown")
        if conflict_type not in grouped:
            grouped[conflict_type] = []
        grouped[conflict_type].append(conflict)
    return grouped


def is_within_time_range(check_time: time, start_time: time, end_time: time) -> bool:
    """Check if a time is within a time range"""
    check_minutes = check_time.hour * 60 + check_time.minute
    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute
    return start_minutes <= check_minutes < end_minutes

