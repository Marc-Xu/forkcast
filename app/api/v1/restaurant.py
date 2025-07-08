"""
Defines all /restaurants endpoints via APIRouter.
"""

from typing import List
from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from app.business_logic.restaurant_service import RestaurantService
from app.data_access_layer.database import get_db
from app.api.v1.schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    Restaurant,
)


router = APIRouter()


def get_restaurant_service(db: Session = Depends(get_db)) -> RestaurantService:
    """
    Dependency to provide a RestaurantService instance for use cases.
    """
    return RestaurantService(db)


@router.post("/", response_model=Restaurant, summary="Create restaurant")
def create_restaurant(
    payload: RestaurantCreate,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Restaurant:
    """
    Create a new restaurant using service layer.
    """
    return service.create_restaurant(payload.model_dump(exclude_unset=True))


@router.get("/", response_model=List[Restaurant], summary="List restaurants")
def list_restaurants(
    skip: int = 0,
    limit: int = Query(10, ge=1, le=100),
    service: RestaurantService = Depends(get_restaurant_service),
) -> List[Restaurant]:
    """
    List restaurants with pagination via service.
    """
    return service.list_restaurants(skip=skip, limit=limit)


@router.get(
    "/top", response_model=List[Restaurant], summary="Top N restaurants by cuisine"
)
def get_top_by_cuisine(
    cuisine: str = Query(..., description="Cuisine to filter by"),
    limit: int = Query(3, ge=1, description="Number of top restaurants to return"),
    service: RestaurantService = Depends(get_restaurant_service),
) -> List[Restaurant]:
    """
    Return the top `limit` restaurants for a given cuisine, ordered by rating.
    """
    return service.get_restaurant_by_attributes(
        attributes={"cuisine": cuisine}, limit=limit, order_by_rating=True
    )


@router.get(
    "/recommend",
    response_model=List[Restaurant],
    summary="Diverse restaurant recommendations",
)
def get_diverse_recommendations(
    limit: int = Query(5, ge=1, description="Number of restaurants to recommend"),
    service: RestaurantService = Depends(get_restaurant_service),
) -> List[Restaurant]:
    """
    Recommend `limit` restaurants ensuring varied cuisines.
    """
    return service.get_diverse_recommendations(limit=limit)


@router.get(
    "/{restaurant_id}", response_model=Restaurant, summary="Get restaurant by ID"
)
def get_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Restaurant:
    """
    Fetch a single restaurant by ID via service.
    """
    return service.get_restaurant(restaurant_id)


@router.patch(
    "/{restaurant_id}", response_model=Restaurant, summary="Update restaurant"
)
def patch_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Restaurant:
    """
    Partially update a restaurant via service.
    """
    return service.update_restaurant(
        restaurant_id, payload.model_dump(exclude_unset=True)
    )


@router.delete(
    "/{restaurant_id}", response_model=Restaurant, summary="Delete restaurant"
)
def delete_restaurant(
    restaurant_id: int,
    service: RestaurantService = Depends(get_restaurant_service),
) -> Restaurant:
    """
    Delete a restaurant via service.
    """
    return service.delete_restaurant(restaurant_id)
