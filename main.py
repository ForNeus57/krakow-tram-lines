import pandas as pd

from pathlib import Path

from src.acquisition.osmnx.tram_tracks import get_train_track_graph, get_tram_stops
from src.acquisition.acquire_data import acquire
from src.visualisation.images.osmnx import visualize_osmnx_graph


def main():
    acquire(Path("./data/generated/data/"))
    graph = get_train_track_graph()
    stops = get_tram_stops()
    # print(stops.to_string())
    stops.to_pickle("./data/generated/data/tram_stops.pkl")

    visualize_osmnx_graph(graph, Path("./data/generated/images/tram_tracks.png"))


if __name__ == '__main__':
    main()

