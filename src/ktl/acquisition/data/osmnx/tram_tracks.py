"""
Module that retrieves data, about train stops from OSMNX API.
"""
from __future__ import annotations
from dataclasses import dataclass

import osmnx as ox
from networkx import MultiDiGraph

from ktl.acquisition.data.osmnx.options import OSMNXOptions


@dataclass(frozen=True)
class TracksData:
    """
    """
    tram_tracks: MultiDiGraph

    @classmethod
    def from_api(cls, options: OSMNXOptions) -> TracksData:
        """
        Custom constructor that retrieves data from OSMNX API and packs it into a MultiDiGraph object
        """
        tracks = ox.graph_from_place(options.get_location(), custom_filter=options.tram_tracks_custom_filter)

        return cls(tracks)
