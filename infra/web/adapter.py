from domain.models import TitleMetadata
def normalize(raw: dict) -> TitleMetadata:
    return TitleMetadata(
        title=raw.get('Title'), year=raw.get('Year'),
        runtime=raw.get('Runtime'), poster=raw.get('Poster'),
        plot=raw.get('Plot'), imdbRating=raw.get('imdbRating'))
