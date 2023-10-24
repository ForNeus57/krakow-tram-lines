import osmnx as ox
from networkx import MultiDiGraph

from src.acquisition.osmnx.constants import LOCATION


class TramTracksData:
    """
    Class that ..... # TODO docstring
    """


def get_train_track_graph() -> MultiDiGraph:
    return ox.graph_from_place(LOCATION, custom_filter=r'["railway"~"tram"]')

