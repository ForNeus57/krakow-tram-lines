from __future__ import annotations
from dataclasses import dataclass

import pandas as pd

from ktl.acquisition.web.tram_models import TramModelsData
from ktl.acquisition.web.constants import URL_TRAM_TIME_TABLE


@dataclass(frozen=True)
class TramTimeTableData:
    """
        #TODO: Docstring for TramTimeTableData
    """
    tram_stops_on_lines: pd.DataFrame

    @classmethod
    def from_url(cls, tram_models: TramModelsData, url: str = URL_TRAM_TIME_TABLE) -> TramTimeTableData:
        lines = tram_models.vehicles_by_line

        train_stops = pd.read_html(url)
        for train in train_stops:
            print(train.to_string())

        return cls(lines)
