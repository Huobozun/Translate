import os
from io import StringIO
import pandas as pd
import json


class JsonSerializer:
    @classmethod
    def serialize_records(self, data: list) -> str:
        df = pd.DataFrame(data)
        return df.to_json(lines=True, orient="records", force_ascii=False)

    @classmethod
    def deserilize_records(self, records_str: str) -> pd.DataFrame:
        buffer = StringIO(records_str)
        # here we have a hard code to avoid parsing pmid as int
        df = pd.read_json(
            buffer,
            orient="records",
            lines=True,
            encoding="utf-8",
            convert_dates=False,
            dtype={"pmid": str},
        )
        return df

    @classmethod
    def serialize_records_to_file(self, file_path: str, data: list):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df = pd.DataFrame(data)
        return df.to_json(file_path, lines=True, orient="records", force_ascii=False)

    @classmethod
    def deserilize_records_from_file(self, file_path: str) -> pd.DataFrame:
        if os.path.isfile(file_path):
            # here we have a hard code to avoid parsing pmid as int
            df = pd.read_json(
                file_path,
                orient="records",
                lines=True,
                encoding="utf-8",
                convert_dates=False,
                dtype={"pmid": str},
            )
            return df
        return None

    @classmethod
    def serilize_one_record(self, data: dict) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4)

    @classmethod
    def deserilize_one_record(self, record_str: str) -> dict:
        return json.loads(record_str)

    @classmethod
    def serilize_one_record_to_file(self, file_path: str, data: dict):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    @classmethod
    def deserilize_one_record_from_file(self, file_path: str) -> dict:
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}
