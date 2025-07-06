"""
schemas.py

Pydantic models for request validation and response serialization.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RestaurantBase(BaseModel):
    """
    Shared properties of a restaurant.

    Attributes:
        name: Name of the restaurant.
        cuisine: Type of cuisine served.
        price_level: Price indicator, 1 (cheap) to 3 (expensive).
        rating: Customer rating 0.0–5.0.
    """
    name: str = Field(..., description="Restaurant name")
    cuisine: Optional[str] = Field(None, description="Cuisine type")
    price_level: int = Field(..., ge=1, le=3, description="Price level")
    rating: float = Field(..., ge=0.0, le=5.0, description="Average rating")


class RestaurantCreate(RestaurantBase):
    """Properties for creating a new restaurant."""
    pass


class Restaurant(RestaurantBase):
    """
    Properties returned in API responses.

    Attributes:
        id: Unique identifier.
    """
    id: int = Field(..., description="Unique ID")
    model_config = ConfigDict(from_attributes=True)


class RestaurantUpdate(BaseModel):
    """
    Properties for updating an existing restaurant. All fields are optional.
    """
    name: Optional[str] = Field(None, description="Restaurant name")
    cuisine: Optional[str] = Field(None, description="Cuisine type")
    price_level: Optional[int] = Field(None, ge=1, le=3, description="Price level")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Average rating")

    model_config = ConfigDict(from_attributes=True)
