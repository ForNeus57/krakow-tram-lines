"""
Module for tram stops data acquisition for OSMNX API
"""

from __future__ import annotations
from dataclasses import dataclass

import geopandas as gpd
import osmnx as ox

from ktl.acquisition.data.osmnx.options import OSMNXOptions


@dataclass(init=True)
class StopsData:
    """
        #TODO: Docstring for TramTimeTableData
    """
    tram_stops: gpd.GeoDataFrame

    @classmethod
    def from_api(cls, options: OSMNXOptions) -> StopsData:
        """
        Custom data constructor that uses OSMNX API to retrieve data about tram stops locations and characteristics.
        """
        stops = ox.features_from_place(options.get_location(), tags=options.tram_stop_tags)

        return cls(stops)
