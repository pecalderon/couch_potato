import os, requests
from dotenv import load_dotenv
from domain.ports import MetadataProvider
from .adapter import normalize
load_dotenv()
class OMDbProvider(MetadataProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv('OMDB_API_KEY', '')
    def fetch(self, title: str):
        if not self.api_key:
            raise RuntimeError('OMDB_API_KEY is missing')
        r = requests.get('https://www.omdbapi.com/',
                         params={'apikey': self.api_key, 't': title, 'plot': 'short', 'r': 'json'},
                         timeout=15)
        r.raise_for_status()
        return normalize(r.json())
