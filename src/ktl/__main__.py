"""
Main module of the ktl package.
"""

from pathlib import Path

from ktl.acquisition.acquire_data import acquire
from ktl.visualisation.images.osmnx import visualize_tram_stops


def main():
    """
    Main function of the ktl package.
    """
    acquire(Path("../../data/generated/data/"))
    visualize_tram_stops()


if __name__ == '__main__':
    main()
