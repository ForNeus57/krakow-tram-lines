from pathlib import Path

from src.acquisition.web.tram_models import TramModelsData
from src.acquisition.web.tram_time_table import TramTimeTableData


def acquire(caching_path: Path) -> None:
    """
    Function that gathers data from web (OSMNX API and from web-scrapers)
    :return:
    """
    models = TramModelsData.from_url(caching_path)
    # TramTimeTableData.from_url(models)    DOESN'T WORK!


def cash_data(path: Path) -> None:
    pass
