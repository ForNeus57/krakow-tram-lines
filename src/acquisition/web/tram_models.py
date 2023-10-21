from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.acquisition.web.constraints import URL_TRAM_MODELS, TRAM_NAME_LENGTH, DEFAULT_TRAM_MODELS_SAVE_PATH


@dataclass(frozen=True)
class TramModelsData:
    """

    """
    vehicles_by_line: pd.DataFrame
    vehicles_by_type: pd.DataFrame
    vehicles_in_ttss: pd.DataFrame
    path: Path = DEFAULT_TRAM_MODELS_SAVE_PATH
    url: str = URL_TRAM_MODELS

    @classmethod
    def from_url(cls, path: Path = DEFAULT_TRAM_MODELS_SAVE_PATH, url: str = URL_TRAM_MODELS) -> TramModelsData:
        data = pd.read_html(url)
        vehicles_by_line = cls.preprocess_vehicles_by_line(data[0])
        vehicles_by_line.to_pickle(f"{path}/vehicles_by_line.pkl")
        vehicles_by_type = cls.preprocess_vehicles_by_type(data[1])
        vehicles_by_type.to_pickle(f"{path}/vehicles_by_type.pkl")
        vehicles_by_ttss = cls.preprocess_vehicles_by_ttss(data[2])
        vehicles_by_ttss.to_pickle(f"{path}/vehicles_by_ttss.pkl")
        return cls(vehicles_by_line, vehicles_by_type, vehicles_by_ttss, path, url)

    @classmethod
    def from_disk(cls, path: Path = DEFAULT_TRAM_MODELS_SAVE_PATH) -> TramModelsData:
        vehicles_by_line: pd.DataFrame = pd.read_pickle(f"{path}/vehicles_by_line.pkl")
        vehicles_by_type: pd.DataFrame = pd.read_pickle(f"{path}/vehicles_by_type.pkl")
        vehicles_in_ttss: pd.DataFrame = pd.read_pickle(f"{path}/vehicles_by_ttss.pkl")
        return cls(vehicles_by_line, vehicles_by_type, vehicles_in_ttss, path)

    @classmethod
    def preprocess_vehicles_by_line(cls, vehicles_by_line: pd.DataFrame) -> pd.DataFrame:
        def split_tram_names(x):
            items = str(x).split(" ")
            new_items = []
            for tram_id in items:
                if len(tram_id) == TRAM_NAME_LENGTH and tram_id[0].isalpha():
                    new_items.append(tram_id[0: TRAM_NAME_LENGTH])

            return new_items

        tram_id_column_name = "tram_id"
        line_number_column_name = "line_number"
        new_data = pd.DataFrame(data=None, columns=[tram_id_column_name, line_number_column_name])

        for idx, row in vehicles_by_line.apply(split_tram_names).items():
            if not idx.isnumeric():
                continue
            for item in row:
                new_data.loc[len(new_data)] = {tram_id_column_name: item, line_number_column_name: idx}

        return new_data

    @classmethod
    def preprocess_vehicles_by_type(cls, vehicles_by_type: pd.DataFrame) -> pd.DataFrame:
        return vehicles_by_type

    @classmethod
    def preprocess_vehicles_by_ttss(cls, vehicles_by_ttss: pd.DataFrame) -> pd.DataFrame:
        return vehicles_by_ttss
