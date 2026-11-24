import re
import shutil
import unicodedata
from pathlib import Path

import yaml
from pydantic import BaseModel

from aws_emulator_proj.tmdb import TmdbClient
from aws_emulator_proj.tmdb_mapper import TmdbMapper


class TmdbExporter:
    def __init__(self, client: TmdbClient, mapper: TmdbMapper, output_dir: Path):
        self.client = client
        self.mapper = mapper
        self.output_dir = output_dir

    def export_series(self, series_id: int) -> Path:
        data = self.client.get_series(series_id)
        series = self.mapper.to_series(data)
        name = f"series-{slugify(series.name)}"
        root = self.output_dir / "staging" / name

        self._write(root / "metadata.yaml", series)
        for season_summary in data["seasons"]:
            season_number = season_summary["season_number"]
            season_data = self.client.get_season(series_id, season_number)
            season_dir = root / f"season-{season_number:02d}"
            self._write(season_dir / "metadata.yaml", self.mapper.to_season(season_data))
            for episode_data in season_data["episodes"]:
                episode_file = season_dir / f"episode-{episode_data['episode_number']:03d}.yaml"
                self._write(episode_file, self.mapper.to_episode(episode_data))

        return self._zip(name)

    def export_movie(self, movie_id: int) -> Path:
        movie = self.mapper.to_movie(self.client.get_movie(movie_id))
        name = f"movie-{slugify(movie.title)}"
        self._write(self.output_dir / "staging" / f"{name}.yaml", movie)
        return self._zip(name)

    def _write(self, path: Path, model: BaseModel) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = model.model_dump(mode="json", exclude_none=True)
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))

    def _zip(self, name: str) -> Path:
        staging = self.output_dir / "staging"
        archive = shutil.make_archive(str(self.output_dir / name), "zip", root_dir=staging)
        shutil.rmtree(staging)
        return Path(archive)


def slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")