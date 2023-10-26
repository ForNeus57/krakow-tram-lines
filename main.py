from pathlib import Path

from src.visualisation.images.osmnx import visualize_tram_stops
from src.acquisition.acquire_data import acquire


def main():
    acquire(Path("./data/generated/data/"))
    visualize_tram_stops()


if __name__ == '__main__':
    main()
