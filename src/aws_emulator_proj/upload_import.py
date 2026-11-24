import io
import json
import zipfile
import boto3
import yaml


class PutMessage:
    def __init__(self, entity_type: str, ids: dict, metadata: dict):
        self.entity_type = entity_type
        self.ids = ids
        self.metadata = metadata


class ArchiveParser:
    def parse(self, archive_bytes: bytes) -> list[PutMessage]:
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            files = {
                name: yaml.safe_load(archive.read(name))
                for name in archive.namelist()
                if name.endswith(".yaml")
            }

        series_ids = {}
        for name, data in files.items():
            parts = name.split("/")
            if len(parts) == 2 and parts[1] == "metadata.yaml":
                series_ids[parts[0]] = data.pop("id")

        messages = []
        for name, data in files.items():
            parts = name.split("/")
            if len(parts) == 1:
                movie_id = data.pop("id")
                messages.append(PutMessage("movie", {"movie_id": movie_id}, data))
            elif len(parts) == 2:
                series_id = series_ids[parts[0]]
                messages.append(PutMessage("series", {"series_id": series_id}, data))
            elif len(parts) == 3:
                series_id = series_ids[parts[0]]
                season_number = int(parts[1].removeprefix("season-"))
                if parts[2] == "metadata.yaml":
                    ids = {"series_id": series_id, "season_number": season_number}
                    messages.append(PutMessage("season", ids, data))
                else:
                    episode_number = int(parts[2].removeprefix("episode-").removesuffix(".yaml"))
                    ids = {
                        "series_id": series_id,
                        "season_number": season_number,
                        "episode_number": episode_number,
                    }
                    messages.append(PutMessage("episode", ids, data))
        return messages


class PutQueueSender:
    def __init__(self, queue_url: str):
        self.sqs = boto3.client("sqs")
        self.queue_url = queue_url

    def send(self, message: PutMessage) -> None:
        attributes = {"type": {"DataType": "String", "StringValue": message.entity_type}}
        for name, value in message.ids.items():
            attributes[name] = {"DataType": "String", "StringValue": str(value)}

        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message.metadata),
            MessageAttributes=attributes,
        )