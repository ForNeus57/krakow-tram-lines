import osmnx as ox
from networkx import MultiDiGraph
import geopandas as gpd

from src.acquisition.osmnx.constants import LOCATION
from dataclasses import dataclass


@dataclass(frozen=True)
class TramTracksData:
    """
    Class that ..... # TODO docstring
    """
    tram_tracks: gpd.GeoDataFrame


def get_train_track_graph() -> MultiDiGraph:
    return ox.graph_from_place(LOCATION, custom_filter=r'["railway"~"tram"]')