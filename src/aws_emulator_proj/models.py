from pydantic import BaseModel
from datetime import date

class EpisodeMetadata(BaseModel):
    name: str
    overview: str | None = None
    air_date: date | None = None
    runtime: int | None = None
    vote_average: float | None = None

class SeasonMetadata(BaseModel):
    name: str
    overview: str | None = None
    air_date: date | None = None

class SeriesMetadata(BaseModel):
    id: int
    name: str
    overview: str | None = None
    first_air_date: date | None = None
    genres: list[str] = []
    vote_average: float | None = None

class MovieMetadata(BaseModel):
    id: int
    title: str
    overview: str | None = None
    release_date: date | None = None
    runtime: int | None = None
    genres: list[str] = []
    vote_average: float | None = None