from __future__ import annotations
from dataclasses import dataclass

import pandas as pd
import geopandas as gpd
import osmnx as ox

from src.acquisition.osmnx.constants import LOCATION


@dataclass(frozen=True)
class TramStopsData:
    """
        #TODO: Docstring for TramTimeTableData
    """
    tram_stops: gpd.GeoDataFrame

    @classmethod
    def from_api(cls) -> TramStopsData:
        stops = ox.features_from_place(LOCATION, tags={'railway': 'tram_stop'})

        return cls(stops)
