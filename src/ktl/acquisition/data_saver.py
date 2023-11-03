"""
DataSaver class for saving data to disk.
"""

from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path

import pandas as pd
import geopandas as gpd
from ktl.acquisition.constants import DEFAULT_SAVE_PATH


@dataclass(frozen=True)
class DataSaver:
    """
    Class that saves data to disk.
    """
    save_path: Path = DEFAULT_SAVE_PATH
    pickle_extension: ClassVar[str] = ".pkl"
    excel_extension: ClassVar[str] = ".xlsx"

    def create_save_directories(self):
        """
        Method that creates necessary paths so that it will be able to save data.
        """
        Path(self.save_path).mkdir(parents=True, exist_ok=True)

    def save_data(self, *args):
        """
        Method that accepts data objects and iterates over their object attributes.
        Then if it is a pandas dataframe or geopandas dataframe it saves all the files to pickle of specified path.
        """
        self.create_save_directories()

        for arg in args:
            for attribute, value in arg.__dict__.items():
                # Make match case for performance
                if isinstance(value, (pd.DataFrame, gpd.GeoDataFrame)):
                    value.to_pickle(self.save_path.joinpath(attribute + DataSaver.excel_extension))
