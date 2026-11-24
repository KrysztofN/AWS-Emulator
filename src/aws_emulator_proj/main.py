import sys
from pathlib import Path
from dotenv import load_dotenv
from aws_emulator_proj.tmdb import TmdbClient, TmdbConfig
from aws_emulator_proj.tmdb_exporter import TmdbExporter
from aws_emulator_proj.tmdb_mapper import TmdbMapper


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("series", "movie"):
        print("usage: aws-emulator-proj series|movie TMDB_ID")
        sys.exit(1)

    load_dotenv()
    exporter = TmdbExporter(TmdbClient(TmdbConfig()), TmdbMapper(), Path("exports"))
    kind, tmdb_id = sys.argv[1], int(sys.argv[2])

    if kind == "series":
        archive = exporter.export_series(tmdb_id)
    else:
        archive = exporter.export_movie(tmdb_id)
    print(f"Created {archive}")