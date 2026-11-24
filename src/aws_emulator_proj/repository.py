import boto3
from boto3.dynamodb.conditions import Key

from aws_emulator_proj.keys import EpisodeKey, MovieKey, SeasonKey, SeriesKey

INTERNAL_FIELDS = ["PK", "SK", "GSI1PK", "GSI1SK", "entity_type"]


class MediaRepository:
    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def put_series(self, series_id: int, metadata: dict) -> None:
        key = SeriesKey(series_id)
        extra = {"GSI1PK": "TYPE#SERIES", "GSI1SK": metadata["name"]}
        self._put(key, "SERIES", metadata, extra)

    def put_season(self, series_id: int, season_number: int, metadata: dict) -> None:
        self._put(SeasonKey(series_id, season_number), "SEASON", metadata, {})

    def put_episode(self, series_id: int, season_number: int, episode_number: int, metadata: dict) -> None:
        self._put(EpisodeKey(series_id, season_number, episode_number), "EPISODE", metadata, {})

    def put_movie(self, movie_id: int, metadata: dict) -> None:
        extra = {"GSI1PK": "TYPE#MOVIE", "GSI1SK": metadata["title"]}
        self._put(MovieKey(movie_id), "MOVIE", metadata, extra)

    def _put(self, key, entity_type: str, metadata: dict, extra: dict) -> None:
        item = {}
        item.update(metadata)
        item.update(extra)
        item["PK"] = key.pk()
        item["SK"] = key.sk()
        item["entity_type"] = entity_type
        self.table.put_item(Item=item)

    def get_movie(self, movie_id: int) -> dict | None:
        return self._get(MovieKey(movie_id))

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

    def delete_movie(self, movie_id: int) -> bool:
        return self._delete(MovieKey(movie_id))

    def delete_episode(self, series_id: int, season_number: int, episode_number: int) -> bool:
        return self._delete(EpisodeKey(series_id, season_number, episode_number))

    def delete_season(self, series_id: int, season_number: int) -> bool:
        key = SeasonKey(series_id, season_number)
        return self._delete_matching(Key("PK").eq(key.pk()) & Key("SK").begins_with(key.sk()))

    def delete_series(self, series_id: int) -> bool:
        key = SeriesKey(series_id)
        return self._delete_matching(Key("PK").eq(key.pk()))

    def _delete(self, key) -> bool:
        response = self.table.delete_item(
            Key={"PK": key.pk(), "SK": key.sk()}, ReturnValues="ALL_OLD"
        )
        return "Attributes" in response

    def _delete_matching(self, condition) -> bool:
        items = self.table.query(KeyConditionExpression=condition)["Items"]
        with self.table.batch_writer() as batch:
            for item in items:
                batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})
        return len(items) > 0

    def _get(self, key) -> dict | None:
        item = self.table.get_item(Key={"PK": key.pk(), "SK": key.sk()}).get("Item")
        if item is None:
            return None
        return self._clean(item)

    def _clean(self, item: dict) -> dict:
        for field in INTERNAL_FIELDS:
            item.pop(field, None)
        return item