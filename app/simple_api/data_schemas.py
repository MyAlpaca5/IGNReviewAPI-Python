"""
Schema represents data structure used in the API service.
"""

from datetime import datetime
from typing import List, Optional, Tuple
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
    short_name: Optional[str] = None
    long_description: Optional[str] = None
    short_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    review_url: str
    review_score: float
    slug: str
    media_type: MediaTypeBase
    genres: List[GenreBase] = []
    creators: List[CreatorBase] = []
    publishers: List[PublisherBase] = []
    franchises: List[FranchiseBase] = []
    regions: List[RegionBase] = []

    class Config:
        orm_mode = True


class MediaTypeOverview(BaseModel):
    size: int = 0
    items: List[Tuple[int, str]] = []


class ReviewForMediaType(MediaTypeBase):
    reviews: List[ReviewBase] = []


class PublisherOverview(BaseModel):
    size: int = 0
    items: List[Tuple[int, str]] = []


class ReviewForPublisher(PublisherBase):
    reviews: List[ReviewBase] = []
