"""
Module that gathers data from web (OSMNX API and from web-scrapers and from Excel)
"""

from pathlib import Path

from ktl.acquisition.osmnx.tram_stops import TramStopsData
from ktl.acquisition.data_saver import DataSaver
from ktl.acquisition.osmnx.tram_tracks import TramTracksData
from ktl.acquisition.selenium.latency_data import LatencyData
from ktl.acquisition.selenium.browser_manager import BrowserManager
from ktl.acquisition.web.tram_model_attributes_data import TramModelsAttributesData
from ktl.acquisition.web.tram_models import TramModelsData
from ktl.acquisition.web.tram_time_table import TramTimeTableData
from ktl.visualisation.images.osmnx import visualize_osmnx_graph


def acquire(caching_path: Path) -> None:
    """
    Function that gathers data from web (OSMNX API and from web-scrapers)
    :return:
    """
    models = TramModelsData.from_url()
    # time_table = TramTimeTableData.from_url(models)
    models_data = TramModelsAttributesData.from_excel()
    tracks = TramTracksData.from_api()
    stops = TramStopsData.from_api()

    with BrowserManager() as bm:
        latency = LatencyData.from_selenium(bm.browser, stops.tram_stops['name'])

    # Saving data to pickle
    ds = DataSaver(caching_path)
    ds.save_data(models, models_data, stops, latency)

    Path("./data/generated/images").mkdir(parents=True, exist_ok=True)
    visualize_osmnx_graph(tracks.tram_tracks, Path("./data/generated/images/tram_tracks.png"))
