"""
Repository for data-access operations on Restaurant.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data_access_layer.models import Restaurant


class RestaurantRepository:
    """
    Provides CRUD operations abstracted from service and HTTP layers.
    """
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> List[Restaurant]:
        """List restaurants with pagination."""
        stmt = select(Restaurant).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, restaurant_id: int) -> Optional[Restaurant]:
        """Get a restaurant by its ID."""
        return self.db.get(Restaurant, restaurant_id)

    def find_by(self, **filters: Any) -> Optional[Restaurant]:
        """
        Fetch a single restaurant matching provided filters.
        Example: repo.find_by(name="Sushi Bar")
        """
        stmt = select(Restaurant).filter_by(**filters)
        return self.db.scalars(stmt).first()

    def add(self, **fields: Any) -> Restaurant:
        """Create and persist a new restaurant."""
        restaurant = Restaurant(**fields)
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def update(self, restaurant_id: int, data: Dict[str, Any]) -> Optional[Restaurant]:
        """Partially update an existing restaurant."""
        restaurant = self.get(restaurant_id)
        if not restaurant:
            return None
        for attr, val in data.items():
            setattr(restaurant, attr, val)
        self.db.commit()
        self.db.refresh(restaurant)
        return restaurant

    def delete(self, restaurant_id: int) -> Optional[Restaurant]:
        """Delete a restaurant by its ID."""
        restaurant = self.get(restaurant_id)
        if not restaurant:
            return None
        self.db.delete(restaurant)
        self.db.commit()
        return restaurant
