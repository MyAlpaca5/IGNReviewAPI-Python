"""
Model represents table stored in the database.
For this project, I use SQLAlchemy to interact with
database instead of manually managing the database.
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Table,
)
from sqlalchemy.orm import relationship

from .database import Base


review_genre_association = Table(
    "review_genre",
    Base.metadata,
    Column("review_id", ForeignKey("review.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)

review_creator_association = Table(
    "review_creator",
    Base.metadata,
    Column("review_id", ForeignKey("review.id"), primary_key=True),
    Column("creator_id", ForeignKey("creator.id"), primary_key=True),
)

review_publisher_association = Table(
    "review_publisher",
    Base.metadata,
    Column("review_id", ForeignKey("review.id"), primary_key=True),
    Column("publisher_id", ForeignKey("publisher.id"), primary_key=True),
)

review_franchise_association = Table(
    "review_franchise",
    Base.metadata,
    Column("review_id", ForeignKey("review.id"), primary_key=True),
    Column("franchise_id", ForeignKey("franchise.id"), primary_key=True),
)

review_region_association = Table(
    "review_region",
    Base.metadata,
    Column("review_id", ForeignKey("review.id"), primary_key=True),
    Column("region_id", ForeignKey("region.id"), primary_key=True),
)


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    short_name = Column(String)
    long_description = Column(String)
    short_description = Column(String)
    created_at = Column(DateTime, nullable=False)
    created_year = Column(Integer, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False)
    review_url = Column(String, nullable=False)
    review_score = Column(Float, nullable=False, index=True)
    slug = Column(String, nullable=False)
    # one to many relationship
    media_type_id = Column(Integer, ForeignKey("media_type.id"), nullable=False)
    media_type = relationship("MediaType", back_populates="reviews")
    # many to many relationship
    genres = relationship(
        "Genre", secondary=review_genre_association, back_populates="reviews"
    )
    # many to many relationship
    creators = relationship(
        "Creator", secondary=review_creator_association, back_populates="reviews"
    )
    # many to many relationship
    publishers = relationship(
        "Publisher", secondary=review_publisher_association, back_populates="reviews"
    )
    # many to many relationship
    franchises = relationship(
        "Franchise", secondary=review_franchise_association, back_populates="reviews"
    )
    # many to many relationship
    regions = relationship(
        "Region", secondary=review_region_association, back_populates="reviews"
    )


class MediaType(Base):
    __tablename__ = "media_type"

    id = Column(Integer, primary_key=True)
    type_name = Column(String)

    reviews = relationship(
        "Review", cascade="all, delete-orphan", back_populates="media_type"
    )


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    genre_name = Column(String)

    reviews = relationship(
        "Review", secondary=review_genre_association, back_populates="genres"
    )


class Creator(Base):
    __tablename__ = "creator"

    id = Column(Integer, primary_key=True)
    creator_name = Column(String)

    reviews = relationship(
        "Review", secondary=review_creator_association, back_populates="creators"
    )


class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True)
    publisher_name = Column(String)

    reviews = relationship(
        "Review", secondary=review_publisher_association, back_populates="publishers"
    )


class Franchise(Base):
    __tablename__ = "franchise"

    id = Column(Integer, primary_key=True)
    franchise_name = Column(String)

    reviews = relationship(
        "Review", secondary=review_franchise_association, back_populates="franchises"
    )


class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True)
    region_name = Column(String)

    reviews = relationship(
        "Review", secondary=review_region_association, back_populates="regions"
    )
