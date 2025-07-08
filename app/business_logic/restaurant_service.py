"""
Business-logic layer orchestrating restaurant use-cases.
"""
from typing import List, Any
from sqlalchemy.orm import Session
from app.data_access_layer.general_repository import GeneralRepository
from app.api.v1.schemas import RestaurantCreate
from app.data_access_layer.models import Restaurant


class RestaurantService:
    """
    Orchestrates business rules and use-cases for Restaurant.
    """
    def __init__(self, db: Session):
        self.repo = GeneralRepository(db=db, model=Restaurant)

    def list_restaurants(self, skip: int = 0, limit: int = 100) -> List[Restaurant]:
        return self.repo.list(skip=skip, limit=limit)

    def get_restaurant(self, restaurant_id: int) -> Restaurant:
        restaurant = self.repo.get(restaurant_id)
        if not restaurant:
            raise ValueError(f"Restaurant {restaurant_id} not found")
        return restaurant

    def get_restaurant_by_attributes(self, attributes: dict[str, Any]) -> Restaurant:
        restaurant = self.repo.find_by(**attributes)
        if not restaurant:
            raise ValueError(f"Restaurant with attributes {attributes} not found")
        return restaurant

    def create_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        # Business rule: name must be unique
        if self.repo.find_by(name=restaurant.name):
            raise ValueError(f"A restaurant named '{restaurant.name}' already exists")
        return self.repo.add(
            name=restaurant.name,
            cuisine=restaurant.cuisine,
            rating=restaurant.rating,
        )

    def update_restaurant(self, restaurant_id: int, data: dict[str, Any]) -> Restaurant:
        updated = self.repo.update(restaurant_id, data)
        if not updated:
            raise ValueError(f"Restaurant {restaurant_id} not found")
        return updated

    def delete_restaurant(self, restaurant_id: int) -> Restaurant:
        deleted = self.repo.delete(restaurant_id)
        if not deleted:
            raise ValueError(f"Restaurant {restaurant_id} not found")
        return deleted
