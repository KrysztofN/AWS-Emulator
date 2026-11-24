from aws_emulator_proj.models import EpisodeMetadata, MovieMetadata, SeasonMetadata, SeriesMetadata


class TmdbMapper:
    def to_series(self, data: dict) -> SeriesMetadata:
        return SeriesMetadata(
            id=data["id"],
            name=data["name"],
            overview=data.get("overview") or None,
            first_air_date=data.get("first_air_date") or None,
            genres=[genre["name"] for genre in data.get("genres", [])],
            vote_average=data.get("vote_average"),
        )

    def to_season(self, data: dict) -> SeasonMetadata:
        return SeasonMetadata(
            name=data["name"],
            overview=data.get("overview") or None,
            air_date=data.get("air_date") or None,
        )

    def to_episode(self, data: dict) -> EpisodeMetadata:
        return EpisodeMetadata(
            name=data["name"],
            overview=data.get("overview") or None,
            air_date=data.get("air_date") or None,
            runtime=data.get("runtime"),
            vote_average=data.get("vote_average"),
        )

    def to_movie(self, data: dict) -> MovieMetadata:
        return MovieMetadata(
            id=data["id"],
            title=data["title"],
            overview=data.get("overview") or None,
            release_date=data.get("release_date") or None,
            runtime=data.get("runtime"),
            genres=[genre["name"] for genre in data.get("genres", [])],
            vote_average=data.get("vote_average"),
        )