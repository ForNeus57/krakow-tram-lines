"""
DataSaver class for saving data to disk.
"""
import shutil
from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path
import os

import pandas as pd
import geopandas as gpd

from ktl.acquisition.data.package import Package
from ktl.acquisition.data.saver_info import SavingInfo


@dataclass(frozen=True)
class Saver:
    """
    Class that saves data to disk.
    """
    data: Package
    save_info: SavingInfo
    pickle_extension: ClassVar[str] = ".pkl"
    excel_extension: ClassVar[str] = ".xlsx"

    def create_save_directories(self) -> None:
        """
        Method that creates necessary paths so that it will be able to save data.
        """
        match self.save_info.format:
            case 'both':
                self.save_info.save_path.joinpath('pickle').mkdir(parents=True, exist_ok=True)
                self.save_info.save_path.joinpath('excel').mkdir(parents=True, exist_ok=True)

            case 'excel':
                self.save_info.save_path.joinpath('excel').mkdir(parents=True, exist_ok=True)

            case 'pickle':
                self.save_info.save_path.joinpath('pickle').mkdir(parents=True, exist_ok=True)

    def save(self) -> None:
        """
        Method that accepts data objects and iterates over their object attributes.
        Then if it is a pandas dataframe or geopandas dataframe it saves all the files to pickle of specified path.
        """
        if self.save_info.force_save:
            shutil.rmtree(self.save_info.save_path, ignore_errors=True)
        elif os.path.exists(self.save_info.save_path):
            return

        self.create_save_directories()

        for _, package_element in self.data.__dict__.items():
            for attribute, value in package_element.__dict__.items():
                # Make match case for performance
                if isinstance(value, (pd.DataFrame, gpd.GeoDataFrame)):
                    match self.save_info.format:
                        case 'both':
                            value.to_pickle(self.save_info.save_path
                                            .joinpath("pickle")
                                            .joinpath(attribute + Saver.pickle_extension))
                            value.to_excel(self.save_info.save_path
                                           .joinpath("excel")
                                           .joinpath(attribute + Saver.excel_extension))

                        case 'excel':
                            value.to_excel(self.save_info.save_path
                                           .joinpath("excel")
                                           .joinpath(attribute + Saver.excel_extension))

                        case 'pickle':
                            value.to_pickle(self.save_info.save_path
                                            .joinpath("pickle")
                                            .joinpath(attribute + Saver.pickle_extension))

