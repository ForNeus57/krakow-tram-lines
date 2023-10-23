import osmnx as ox
from networkx import MultiDiGraph
from geopandas import GeoDataFrame

from src.acquisition.osmnx.constraints import LOCATION


class TramTracksData:
    """
    Class that ..... # TODO docstring
    """


def get_train_track_graph() -> MultiDiGraph:
    return ox.graph_from_place(LOCATION, custom_filter=r'["railway"~"tram"]')


def get_tram_stops() -> GeoDataFrame:
    return ox.features_from_place(LOCATION, tags={'railway': 'tram_stop'})
