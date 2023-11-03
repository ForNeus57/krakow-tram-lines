"""
Module for tram stops data acquisition for OSMNX API
"""

from __future__ import annotations
from dataclasses import dataclass

import geopandas as gpd
import osmnx as ox

from ktl.acquisition.osmnx.constants import LOCATION


@dataclass(init=True)
class TramStopsData:
    """
        #TODO: Docstring for TramTimeTableData
    """
    tram_stops: gpd.GeoDataFrame

    @classmethod
    def from_api(cls, location: str = LOCATION) -> TramStopsData:
        """
        Custom data constructor that uses OSMNX API to retrieve data about tram stops locations and characteristics.
        """
        stops = ox.features_from_place(location, tags={'railway': 'tram_stop'})

        return cls(stops)
