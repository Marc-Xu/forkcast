"""
Business-logic layer orchestrating restaurant use-cases.
"""

import random
from typing import List, Any
from sqlalchemy.orm import Session
from app.data_access_layer.general_repository import GeneralRepository
from app.data_access_layer.models import Restaurant
from app.exceptions import NotFoundError, ValidationError


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
            raise NotFoundError(f"Restaurant {restaurant_id} not found")
        return restaurant

    def get_restaurant_by_attributes(
        self, attributes: dict[str, Any], limit: int = 10, order_by_rating: bool = False
    ) -> List[Restaurant]:
        order_by = Restaurant.rating.desc() if order_by_rating else None
        restaurants = self.repo.find_by(limit=limit, order_by=order_by, **attributes)
        if not restaurants:
            raise NotFoundError(f"Restaurants with attributes {attributes} not found")
        return restaurants

    def create_restaurant(self, restaurant_data: dict[str, Any]) -> Restaurant:
        # Business rule: name must be unique
        if self.repo.find_by(name=restaurant_data["name"]):
            raise ValidationError(
                f"A restaurant named '{restaurant_data["name"]}' already exists"
            )
        return self.repo.add(**restaurant_data)

    def update_restaurant(self, restaurant_id: int, data: dict[str, Any]) -> Restaurant:
        updated = self.repo.update(restaurant_id, data)
        if not updated:
            raise NotFoundError(f"Restaurant {restaurant_id} not found")
        return updated

    def delete_restaurant(self, restaurant_id: int) -> Restaurant:
        deleted = self.repo.delete(restaurant_id)
        if not deleted:
            raise NotFoundError(f"Restaurant {restaurant_id} not found")
        return deleted

    def get_diverse_recommendations(self, limit: int = 5) -> List[Restaurant]:
        """
        Return a list of `limit` restaurants ensuring cuisine diversity.

        This method groups all restaurants by cuisine, randomly selects cuisines
        (with repetition if `limit` exceeds the number of cuisines), then picks
        one random restaurant from each selected cuisine, removing it from that
        group to avoid duplicates.

        Args:
            limit: The number of restaurants to recommend.

        Returns:
            A list of Restaurant objects sampled to maximize cuisine variety.
        """

        all_restaurants = self.repo.list()
        restaurant_by_cuisine = {}
        for restaurant in all_restaurants:
            restaurant_by_cuisine.setdefault(restaurant.cuisine, []).append(restaurant)
        cuisines = random.choices(list(restaurant_by_cuisine.keys()), k=limit)
        recommendations = []
        while restaurant_by_cuisine and len(recommendations) < limit:
            for cuisine in cuisines:
                if cuisine not in restaurant_by_cuisine:
                    continue
                if not restaurant_by_cuisine[cuisine]:
                    del restaurant_by_cuisine[cuisine]
                    continue
                restaurant = random.choice(restaurant_by_cuisine[cuisine])
                restaurant_by_cuisine[cuisine].remove(restaurant)
                recommendations.append(restaurant)
                if len(recommendations) == limit:
                    break
        return recommendations
