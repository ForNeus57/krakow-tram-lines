from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd

from src.acquisition.web.constants import URL_TRAM_MODELS, TRAM_NAME_LENGTH, DEFAULT_TRAM_MODELS_SAVE_PATH


def change_column_names(x: str) -> str:
    value = re.sub(r'[^\w\s_]', '', x.lower())
    return re.sub(r'[_\s]+', '_', value).strip('_')


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
        vehicles_by_type = cls.preprocess_vehicles_by_type(data[1])
        vehicles_by_ttss, vehicles_by_line = cls.preprocess_vehicles_by_ttss(data[2])

        vehicles_by_type = pd.merge(vehicles_by_ttss, vehicles_by_type, on="id", how="left")
        vehicles_by_type = vehicles_by_type[["id", "tram_depo_code_x", "tram_code_x", "name"]]
        vehicles_by_type.columns = ["id", "tram_depo_code", "tram_code", "name"]
        vehicles_by_ttss.drop(columns=["tram_depo_code", "tram_code"], inplace=True)

        vehicles_by_line.to_pickle(f"{path}/vehicles_by_line.pkl")
        vehicles_by_type.to_pickle(f"{path}/vehicles_by_type.pkl")
        vehicles_by_ttss.to_pickle(f"{path}/vehicles_by_ttss.pkl")
        return cls(vehicles_by_line, vehicles_by_type, vehicles_by_ttss, path, url)

    @classmethod
    def from_disk(cls, path: Path = DEFAULT_TRAM_MODELS_SAVE_PATH) -> TramModelsData:
        vehicles_by_line: pd.DataFrame = pd.read_pickle(f"{path}/vehicles_by_line.pkl")
        vehicles_by_type: pd.DataFrame = pd.read_pickle(f"{path}/vehicles_by_type.pkl")
        vehicles_in_ttss: pd.DataFrame = pd.read_pickle(f"{path}/vehicles_by_ttss.pkl")
        return cls(vehicles_by_line, vehicles_by_type, vehicles_in_ttss, path)

    @staticmethod
    def split_tram_names(x):
        items = str(x).split(" ")
        new_items = []
        for tram_id in items:
            if len(tram_id) == TRAM_NAME_LENGTH and tram_id[0].isalpha():
                new_items.append(tram_id[0: TRAM_NAME_LENGTH])

        return new_items

    @classmethod
    def preprocess_vehicles_by_line(cls, vehicles_by_line: pd.DataFrame) -> pd.DataFrame:
        tram_id_column_name = "id"
        line_number_column_name = "line"
        new_data = pd.DataFrame(data=None, columns=[tram_id_column_name, line_number_column_name])

        for idx, row in vehicles_by_line.apply(TramModelsData.split_tram_names).items():
            if not idx.isnumeric():
                continue
            for item in row:
                new_data.loc[len(new_data)] = {tram_id_column_name: item, line_number_column_name: idx}

        return new_data

    @classmethod
    def preprocess_vehicles_by_type(cls, vehicles_by_type: pd.DataFrame) -> pd.DataFrame:
        """
        #TODO: change this to delete row 3....
        :param vehicles_by_type:
        :return:
        """
        vehicles_by_type.drop(1, inplace=True, axis=1)
        vehicles_by_type[2] = vehicles_by_type[2].apply(TramModelsData.split_tram_names)
        vehicles_by_type.set_index(vehicles_by_type[0], inplace=True)
        vehicles_by_type[0] = vehicles_by_type[2]
        vehicles_by_type.drop(2, inplace=True, axis=1)
        tram_id_column_name = "id"
        train_name_column_name = "name"
        new_data = pd.DataFrame(data=None, columns=[tram_id_column_name, train_name_column_name])
        for idx, row in vehicles_by_type[0].items():
            for item in row:
                new_data.loc[len(new_data)] = {tram_id_column_name: item, train_name_column_name: idx}

        new_data['tram_depo_code'] = new_data['id'].apply(lambda x: str(x)[0]).astype(str)
        new_data['tram_code'] = new_data['id'].apply(lambda x: str(x)[1]).astype(str)
        new_data['id'] = new_data['id'].apply(lambda x: str(x)[2:]).astype(int)
        return new_data

    @classmethod
    def preprocess_vehicles_by_ttss(cls, vehicles_by_ttss: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

        vehicles_by_ttss.columns = [change_column_names(col) for col in vehicles_by_ttss.columns]
        # TODO: merge into one
        vehicles_by_ttss.drop(vehicles_by_ttss[vehicles_by_ttss["line"].str.contains(r'\?') |
                                               vehicles_by_ttss["vehicle"].str.contains(r'\?')].index,
                              inplace=True, axis=0)
        vehicles_by_ttss['position'] = vehicles_by_ttss['position'].apply(lambda x: str(x).split(","))
        # TODO: Check if this precision is sufficient
        vehicles_by_ttss['latitude'] = vehicles_by_ttss['position'].apply(lambda x: x[0]).astype(float)
        vehicles_by_ttss['longitude'] = vehicles_by_ttss['position'].apply(lambda x: x[1]).astype(float)

        vehicles_by_ttss['line'] = vehicles_by_ttss['line'].apply(lambda x: str(x).split(" "))
        vehicles_by_ttss['direction'] = vehicles_by_ttss['line'].apply(lambda x: ' '.join(x[1:]))
        vehicles_by_ttss['line'] = vehicles_by_ttss['line'].apply(lambda x: x[0]).astype(int)
        vehicles_by_ttss.drop('position', axis=1, inplace=True)
        vehicles_by_ttss['id'] = vehicles_by_ttss['vehicle'].apply(lambda x: str(x)[2:]).astype(int)
        vehicles_by_ttss['tram_depo_code'] = vehicles_by_ttss['vehicle'].apply(lambda x: str(x)[0]).astype(str)
        vehicles_by_ttss['tram_code'] = vehicles_by_ttss['vehicle'].apply(lambda x: str(x)[1]).astype(str)
        vehicles_by_ttss.drop('vehicle', axis=1, inplace=True)

        lines = vehicles_by_ttss[['line']].drop_duplicates()
        lines.sort_values(axis=0, by=['line'], ascending=True, inplace=True)

        return vehicles_by_ttss, lines
