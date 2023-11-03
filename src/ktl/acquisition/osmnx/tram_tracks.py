"""
Module that retrieves data, about train stops from OSMNX API.
"""
from __future__ import annotations
from dataclasses import dataclass

import osmnx as ox
from networkx import MultiDiGraph

from ktl.acquisition.osmnx.constants import LOCATION


@dataclass(frozen=True)
class TramTracksData:
    """
    Class that ..... # TODO docstring
    """
    tram_tracks: MultiDiGraph

    @classmethod
    def from_api(cls, location: str = LOCATION) -> TramTracksData:
        """
        Custom constructor that retrieves data from OSMNX API and packs it into a MultiDiGraph object
        """
        tracks = ox.graph_from_place(location, custom_filter=r'["railway"~"tram"]')

        return cls(tracks)
