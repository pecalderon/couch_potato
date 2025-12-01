from typing import List, Dict
from domain.models import WatchItem
from domain.ports import Repository, MetadataProvider
def _to_float_rating(r):
    if not r or r == 'N/A':
        return None
    try:
        return float(r)
    except ValueError:
        return None
class AppService:
    def __init__(self, repo: Repository, provider: MetadataProvider):
        self.repo = repo
        self.provider = provider
    def add_title(self, title: str) -> int:
        meta = self.provider.fetch(title)
        item = WatchItem(id=None, title=title, status="to_watch",
                         year=meta.year, runtime=meta.runtime,
                         poster_url=meta.poster, plot=meta.plot,
                         imdb_rating=_to_float_rating(meta.imdbRating))
        return self.repo.save(item, meta)
    def search(self, q: str) -> List[WatchItem]:
        return self.repo.find(q)
    def update_status(self, item_id: int, status: str) -> None:
        self.repo.update_status(item_id, status)
    def remove(self, item_id: int) -> None:
        self.repo.remove(item_id)
    def summary(self) -> Dict[str, float]:
        return self.repo.summary()
