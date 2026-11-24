import os

import httpx

BASE_URL = "https://api.themoviedb.org/3"


class TmdbConfig:
    def __init__(self):
        token = os.getenv("TMDB_READ_TOKEN")
        if not token:
            raise ValueError("Missing environment variable TMDB_READ_TOKEN")
        self.read_token = token


class TmdbClient:
    def __init__(self, config: TmdbConfig):
        self.http = httpx.Client(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {config.read_token}"},
            timeout=10,
        )

    def get_series(self, series_id: int) -> dict:
        return self._get(f"/tv/{series_id}")

    def get_season(self, series_id: int, season_number: int) -> dict:
        return self._get(f"/tv/{series_id}/season/{season_number}")

    def get_movie(self, movie_id: int) -> dict:
        return self._get(f"/movie/{movie_id}")

    def _get(self, path: str) -> dict:
        response = self.http.get(path)
        response.raise_for_status()
        return response.json()