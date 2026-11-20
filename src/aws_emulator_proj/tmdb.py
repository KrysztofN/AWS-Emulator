import os


class TmdbConfig:
    def __init__(self):
        token = os.getenv("TMDB_READ_TOKEN")
        if not token:
            raise ValueError("TMDB_READ_TOKEN not set")
        self.read_token = token