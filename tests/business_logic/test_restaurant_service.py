import pytest

from app.exceptions import NotFoundError, ValidationError
from app.business_logic.restaurant_service import RestaurantService


@pytest.fixture
def service(db_session):
    return RestaurantService(db_session)


def test_create_and_unique(service):
    data = {"name": "Test", "cuisine": "C", "rating": 4.4}
    r1 = service.create_restaurant(data)
    assert r1.name == "Test"
    # duplicate name business rule
    with pytest.raises(ValidationError) as exc:
        service.create_restaurant(data)
    assert "already exists" in str(exc.value)


def test_get_not_found(service):
    with pytest.raises(NotFoundError):
        service.get_restaurant(9999)


def test_update_and_not_found(service):
    data = {"name": "Up", "cuisine": None, "rating": 1.0}
    r = service.create_restaurant(data)
    update_data = {"rating": 2.0}
    r2 = service.update_restaurant(r.id, update_data)
    assert abs(r2.rating - 2.0) < 1e-6
    with pytest.raises(NotFoundError):
        service.update_restaurant(9999, update_data)


def test_delete_and_not_found(service):
    data = {"name": "Del", "cuisine": None, "rating": 3.3}
    r = service.create_restaurant(data)
    d = service.delete_restaurant(r.id)
    assert d.id == r.id
    with pytest.raises(NotFoundError):
        service.delete_restaurant(9999)
