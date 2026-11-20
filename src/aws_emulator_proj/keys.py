class SeriesKey:
    def __init__(self, series_id: int):
        self.series_id = series_id

    def pk(self) -> str:
        return f"SERIES#{self.series_id}"

    def sk(self) -> str:
        return "METADATA"

class SeasonKey:
    def __init__(self, series_id: int, season_number: int):
        self.series_id = series_id
        self.season_number = season_number

    def pk(self) -> str:
        return f"SERIES#{self.series_id}"

    def sk(self) -> str:
        return f"SEASON#{self.season_number:02d}"


class EpisodeKey:
    def __init__(self, series_id: int, season_number: int, episode_number: int):
        self.series_id = series_id
        self.season_number = season_number
        self.episode_number = episode_number

    def pk(self) -> str:
        return f"SERIES#{self.series_id}"

    def sk(self) -> str:
        return f"SEASON#{self.season_number:02d}#EPISODE#{self.episode_number:03d}"

class MovieKey:
    def __init__(self, movie_id: int):
        self.movie_id = movie_id

    def pk(self) -> str:
        return f"MOVIE#{self.movie_id}"

    def sk(self) -> str:
        return "METADATA"