import os
from .omdb_provider import OMDbProvider
def get_provider():
    return OMDbProvider(api_key=os.getenv('OMDB_API_KEY'))
