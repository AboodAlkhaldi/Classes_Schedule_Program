# This file imports all models so Alembic can detect them
from app.models.base import Base
from app.models import *  # noqa: F401, F403

__all__ = ["Base"]

