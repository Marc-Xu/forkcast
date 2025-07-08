"""
Generic repository for data-access operations.
"""

from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from sqlalchemy import select, ColumnElement
from sqlalchemy.orm import Session

from app.data_access_layer.database import Base


Model = TypeVar("Model", bound=Base)


class GeneralRepository(Generic[Model]):
    """
    Provides CRUD operations abstracted from service and HTTP layers.
    """

    def __init__(self, db: Session, model: Type[Model]):
        self.db = db
        self.model = model

    def list(self, skip: int = 0, limit: int = 100) -> List[Model]:
        """List Ts with pagination."""
        stmt = select(self.model).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, identifier: int) -> Optional[Model]:
        """Get an object by its ID."""
        return self.db.get(self.model, identifier)

    def find_by(
        self, limit: int = 10, order_by: ColumnElement = None, **filters: Any
    ) -> List[Model]:
        """
        Fetch up to `limit` objects matching provided filters.
        Example: repo.find_by(limit=2, name="Sushi Bar")
        """
        stmt = select(self.model).filter_by(**filters).order_by(order_by).limit(limit)
        return list(self.db.scalars(stmt).all())

    def add(self, **fields: Any) -> Model:
        """Create and persist a new object."""
        obj = self.model(**fields)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, identifier: int, data: Dict[str, Any]) -> Optional[Model]:
        """Partially update an existing object."""
        obj = self.get(identifier)
        if not obj:
            return None
        for attr, val in data.items():
            setattr(obj, attr, val)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, identifier: int) -> Optional[Model]:
        """Delete an object by its ID."""
        obj = self.get(identifier)
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj
