from sqlalchemy.orm import Session
from typing import Generic, List, Optional, Type, TypeVar, Dict, Any
from fastapi.encoders import jsonable_encoder

from .database import Base
from .data_models import Creator, Franchise, Genre, MediaType, Publisher, Region, Review


ModelType = TypeVar("ModelType", bound=Base)

# Generic CRUD class
class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def read_one_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).get(id)

    def read_range(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, pair: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**pair)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, old_db_obj: ModelType, updated_pair: Dict[str, Any]
    ) -> ModelType:
        old_db_data = jsonable_encoder(old_db_obj)

        for field in old_db_data:
            if field in updated_pair:
                setattr(old_db_obj, field, updated_pair[field])

        db.add(old_db_obj)
        db.commit()
        db.refresh(old_db_obj)
        return old_db_obj

    def delete(self, db: Session, id: int) -> ModelType:
        db_obj = db.query(self.model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj


class MediaTypeCRUD(CRUDBase[MediaType]):
    def get_overview(self, db: Session) -> Dict[str, Any]:
        records = db.query(self.model).all()
        overview = {"size": len(records), "items": []}
        for r in records:
            overview["items"].append((r.id, r.type_name))
        return overview


class GenreCRUD(CRUDBase[Genre]):
    ...


class CreatorCRUD(CRUDBase[Creator]):
    ...


class PublisherCRUD(CRUDBase[Publisher]):
    def get_overview(self, db: Session) -> Dict[str, Any]:
        records = db.query(self.model).all()
        overview = {"size": len(records), "items": []}
        for r in records:
            overview["items"].append((r.id, r.publisher_name))
        return overview


class FranchiseCRUD(CRUDBase[Franchise]):
    ...


class RegionCRUD(CRUDBase[Region]):
    ...


class ReviewCRUD(CRUDBase[Review]):
    def get_reviews_with_parameters(
        self, db: Session, parameters: Dict[str, Any]
    ) -> List[ModelType]:
        """
        Get a list of Review filtered and sorted by user input parameters

        Parameters:
        db: database connection session
        parameters: a list of parameters that will be used as filters

        Returns:
        List[ModelType]: a list of Review records
        """

        filters = []
        order = []

        if "media_type_id" in parameters:
            filters.append(self.model.media_type_id == parameters["media_type_id"])

        if "publisher_id" in parameters:
            # publisher is a many-to-many relationship, need special care
            filters.append(
                self.model.publishers.any(Publisher.id == parameters["publisher_id"])
            )

        if "posted_year" in parameters:
            filters.append(self.model.created_year == parameters["posted_year"])

        if "score" in parameters:
            filters.append(self.model.review_score >= parameters["score"])

        order.append(self.model.name)
        order.append(self.model.review_score)

        return db.query(self.model).filter(*filters).order_by(*order).all()


mediatypeCRUD = MediaTypeCRUD(MediaType)
genreCRUD = GenreCRUD(Genre)
creatorCRUD = CreatorCRUD(Creator)
publisherCRUD = PublisherCRUD(Publisher)
franchiseCRUD = FranchiseCRUD(Franchise)
regionCRUD = RegionCRUD(Region)
reviewCRUD = ReviewCRUD(Review)
