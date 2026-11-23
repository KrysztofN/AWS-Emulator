import boto3
from aws_emulator_proj.keys import EpisodeKey, MovieKey, SeasonKey, SeriesKey
from boto3.dynamodb.conditions import Key

INTERNAL_FIELDS = ["PK", "SK", "GSI1PK", "GSI1SK", "entity_type"]

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
    
    def get_movie(self, movie_id: int) -> dict | None:
        return self._get(MovieKey(movie_id))

    def _get(self, key) -> dict | None:
        item = self.table.get_item(Key={"PK": key.pk(), "SK": key.sk()}).get("Item")
        if item is None:
            return None
        return self._clean(item)

    def _clean(self, item: dict) -> dict:
        for field in INTERNAL_FIELDS:
            item.pop(field, None)
        return item
    
    def get_series(self, series_id: int) -> dict | None:
        return self._get(SeriesKey(series_id))

    def get_episode(self, series_id: int, season_number: int, episode_number: int) -> dict | None:
        return self._get(EpisodeKey(series_id, season_number, episode_number))
    
    def get_season(self, series_id: int, season_number: int) -> dict | None:
        key = SeasonKey(series_id, season_number)
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(key.pk()) & Key("SK").begins_with(key.sk())
        )

        season = None
        episodes = []
        for item in response["Items"]:
            sort_key = item["SK"]
            if sort_key == key.sk():
                season = self._clean(item)
            else:
                episode = self._clean(item)
                episode["episode_number"] = int(sort_key.split("#")[-1])
                episodes.append(episode)

        if season is None:
            return None
        season["episodes"] = episodes
        return season