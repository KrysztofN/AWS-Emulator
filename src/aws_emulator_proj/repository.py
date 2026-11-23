import boto3
from aws_emulator_proj.keys import EpisodeKey, MovieKey, SeasonKey, SeriesKey

class MediaRepository:
    def __init__(self, table_name:str):
        self.table = boto3.resource("dynamodb").Table(table_name)
    
    def put_series(self, series_id: int, metadata: dict) -> None:
        key = SeriesKey(series_id)
        extra = {"GSI1PK" : "TYPE#SERIES", "GSI1SK" : metadata["name"]}
        self._put(key, "SERIES", metadata, extra)

    def put_season(self, series_id: int, season_number: int, metadata: dict) -> None:
        key = SeasonKey(series_id, season_number)
        self._put(key, "SEASON", metadata, {})

    def put_episode(
        self, series_id: int, season_number: int, episode_number: int, metadata: dict) -> None:
        key = EpisodeKey(series_id, season_number, episode_number)
        self._put(key, "EPISODE", metadata, {})

    def put_movie(self, movie_id: int, metadata: dict) -> None:
        key = MovieKey(movie_id)
        extra = {"GSI1PK": "TYPE#MOVIE", "GSI1SK": metadata["title"]}
        self._put(key, "MOVIE", metadata, extra)
    
    def _put(self, key, entity_type: str, metadata: dict, extra: dict) -> None:
        item = {"PK" : key.pk(), "SK" : key.sk(), "entity_type" : entity_type}
        item.update(metadata)
        item.update(extra)
        self.table.put_item(Item = item)