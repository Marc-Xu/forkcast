import pytest

from app.data_access_layer.models import Restaurant
from app.data_access_layer.general_repository import GeneralRepository


@pytest.fixture
def repo(db_session):
    return GeneralRepository(db_session, Restaurant)


def test_add_and_get(repo):
    r = repo.add(name="Test", cuisine="X", rating=4.2)
    assert isinstance(r, Restaurant)
    fetched = repo.get(r.id)
    assert fetched.id == r.id
    assert fetched.name == "Test"


def test_list_pagination(repo):
    # add 3 items
    for i in range(3):
        repo.add(name=f"R{i}", cuisine=None, rating=0.0)
    all_rest = repo.list()
    assert len(all_rest) >= 3
    first_two = repo.list(limit=2)
    assert len(first_two) == 2


def test_find_by(repo):
    repo.add(name="Unique", cuisine="U", rating=1.1)
    found: Restaurant = repo.find_by(name="Unique")[0]
    assert found is not None and found.name == "Unique"
    assert not repo.find_by(name="DoesNotExist")


def test_update(repo):
    r = repo.add(name="Old", cuisine=None, rating=0.0)
    updated = repo.update(r.id, {"name": "New", "rating": 3.3})
    assert updated.name == "New"
    assert abs(updated.rating - 3.3) < 1e-6
    # updating non-existing
    assert repo.update(9999, {}) is None


def test_delete(repo):
    r = repo.add(name="ToDelete", cuisine=None, rating=2.2)
    deleted = repo.delete(r.id)
    assert deleted.id == r.id
    assert repo.get(r.id) is None
