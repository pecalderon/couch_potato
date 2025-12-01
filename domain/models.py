from dataclasses import dataclass
from typing import Optional
@dataclass
class WatchItem:
    id: Optional[int]
    title: str
    status: str = "to_watch"
    note: Optional[str] = None
    year: Optional[str] = None
    runtime: Optional[str] = None
    poster_url: Optional[str] = None
    plot: Optional[str] = None
    imdb_rating: Optional[float] = None
@dataclass
class TitleMetadata:
    title: str
    year: Optional[str] = None
    runtime: Optional[str] = None
    poster: Optional[str] = None
    plot: Optional[str] = None
    imdbRating: Optional[str] = None
