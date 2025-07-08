"""
Defines ORM models for the application.
"""

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.data_access_layer.database import Base


class Restaurant(Base):
    """
    ORM model for a restaurant entry.

    Attributes:
        id: Primary key.
        name: Restaurant name.
        cuisine: Cuisine type.
        rating: Average rating (0.0–5.0).
    """

    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    cuisine: Mapped[Optional[str]] = mapped_column(index=True)
    rating: Mapped[Optional[float]] = mapped_column(index=True)
