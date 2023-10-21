from pathlib import Path

import osmnx as ox
from networkx import MultiDiGraph

from src.visualisation.images.constraints import TRAM_TRACKS_IMAGE_SIZE, LINE_COLOR


def visualize_osmnx_graph(g: MultiDiGraph, path: Path) -> None:
    ox.plot_graph(g, filepath=str(path), figsize=TRAM_TRACKS_IMAGE_SIZE, node_size=0, edge_linewidth=1,
                  edge_color=LINE_COLOR, save=True)
