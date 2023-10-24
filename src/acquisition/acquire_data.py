from pathlib import Path

from src.acquisition.osmnx.tram_stops import TramStopsData
from src.acquisition.web.tram_models import TramModelsData
from src.acquisition.web.tram_time_table import TramTimeTableData
from src.acquisition.web.tram_model_attributes_data import TramModelsAttributesData
from src.acquisition.data_saver import DataSever

from src.acquisition.osmnx.tram_tracks import get_train_track_graph
from src.visualisation.images.osmnx import visualize_osmnx_graph

from src.acquisition.web.constants import TRAM_NAME_LENGTH


def acquire(caching_path: Path) -> None:
    """
    Function that gathers data from web (OSMNX API and from web-scrapers)
    :return:
    """
    models = TramModelsData.from_url()
    # time_table = TramTimeTableData.from_url(models)    DOESN'T WORK!
    models_data = TramModelsAttributesData.from_excel()

    graph = get_train_track_graph()
    stops = TramStopsData.from_api()

    # Saving data to pickle
    ds = DataSever(caching_path)
    ds.create_save_directories()
    ds.save_data(models, models_data, stops)

    Path("./data/generated/images").mkdir(parents=True, exist_ok=True)
    visualize_osmnx_graph(graph, Path("./data/generated/images/tram_tracks.png"))


def cash_data(path: Path) -> None:
    pass
