"""
Main module of the ktl package.
"""

from pathlib import Path

# from ktl.acquisition.acquire_data import acquire
from ktl.visualisation.images.osmnx import visualize_tram_stops


def main():
    """
    Main function of the ktl package.
    """
    # acquire(Path("../../data/generated/data/"))
    # visualize_osmnx_graph(tracks.tram_tracks, Path("./data/generated/images/tram_tracks.png"))
    # Path("./data/generated/images").mkdir(parents=True, exist_ok=True)
    visualize_tram_stops()


if __name__ == '__main__':
    main()
