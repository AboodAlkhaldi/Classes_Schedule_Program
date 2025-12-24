import re
from typing import Optional


def normalize_string(text: str) -> str:
    """Normalize string (trim, lowercase, remove extra spaces)"""
    if not text:
        return ""
    # Remove extra whitespace and trim
    normalized = re.sub(r'\s+', ' ', text.strip())
    return normalized


def normalize_code(code: str) -> str:
    """Normalize codes to uppercase, trim"""
    if not code:
        return ""
    return code.strip().upper()


def normalize_email(email: str) -> str:
    """Normalize email to lowercase"""
    if not email:
        return ""
    return email.strip().lower()


def normalize_name(name: str) -> str:
    """Normalize person names (title case)"""
    if not name:
        return ""
    # Trim and title case
    normalized = " ".join(word.capitalize() for word in name.strip().split())
    return normalized


def normalize_faculty_code(code: str) -> str:
    """Normalize faculty code to uppercase, exactly 3 characters"""
    normalized = normalize_code(code)
    if len(normalized) != 3:
        raise ValueError(f"Faculty code must be exactly 3 characters, got: {normalized}")
    return normalized


def normalize_department_code(code: str) -> str:
    """Normalize department code to uppercase, exactly 3 characters"""
    normalized = normalize_code(code)
    if len(normalized) != 3:
        raise ValueError(f"Department code must be exactly 3 characters, got: {normalized}")
    return normalized

