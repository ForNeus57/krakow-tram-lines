from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path

import pandas as pd
import geopandas as gpd
from src.acquisition.constants import DEFAULT_SAVE_PATH


@dataclass(frozen=True)
class DataSever:
    """

    """
    save_path: Path = DEFAULT_SAVE_PATH
    pickle_extension: ClassVar[str] = ".pkl"

    def create_save_directories(self):
        Path(self.save_path).mkdir(parents=True, exist_ok=True)

    def save_data(self, *args):
        for arg in args:
            for attribute, value in arg.__dict__.items():
                # Make match case for performance
                if isinstance(value, pd.DataFrame) or isinstance(value, gpd.GeoDataFrame):
                    value.to_pickle(self.save_path.joinpath(attribute + DataSever.pickle_extension))
