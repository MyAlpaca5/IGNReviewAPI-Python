"""
Schema represents data structure used in the API service.
"""

from datetime import datetime
from pydantic import BaseModel


class MediaTypeBase(BaseModel):
    type_name: str

    class Config:
        orm_mode = True


class GenreBase(BaseModel):
    genre_name: str

    class Config:
        orm_mode = True


class CreatorBase(BaseModel):
    creator_name: str

    class Config:
        orm_mode = True


class PublisherBase(BaseModel):
    publisher_name: str

    class Config:
        orm_mode = True


class FranchiseBase(BaseModel):
    franchise_name: str

    class Config:
        orm_mode = True


class RegionBase(BaseModel):
    region_name: str

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    name: str
    short_name: str | None = None
    long_description: str | None = None
    short_description: str | None = None
    created_at: datetime
    updated_at: datetime
    review_url: str
    review_score: float
    slug: str
    media_type: MediaTypeBase
    genres: list[GenreBase] = []
    creators: list[CreatorBase] = []
    publishers: list[PublisherBase] = []
    franchises: list[FranchiseBase] = []
    regions: list[RegionBase] = []

    class Config:
        orm_mode = True


class MediaTypeOverview(BaseModel):
    size: int = 0
    items: list[tuple[int, str]] = []


class ReviewForMediaType(MediaTypeBase):
    reviews: list[ReviewBase] = []


class PublisherOverview(BaseModel):
    size: int = 0
    items: list[tuple[int, str]] = []


class ReviewForPublisher(PublisherBase):
    reviews: list[ReviewBase] = []
