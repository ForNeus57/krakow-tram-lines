from pathlib import Path

from src.acquisition.web.tram_models import TramModelsData
from src.acquisition.web.tram_time_table import TramTimeTableData
from src.acquisition.web.tram_model_attributes_data import TramModelsAttributesData

from src.acquisition.web.constants import TRAM_NAME_LENGTH, DEFAULT_TRAM_MODELS_SAVE_PATH


def acquire(caching_path: Path) -> None:
    """
    Function that gathers data from web (OSMNX API and from web-scrapers)
    :return:
    """
    models = TramModelsData.from_url(caching_path)
    # TramTimeTableData.from_url(models)    DOESN'T WORK!
    TramModelsAttributesData.from_excel(caching_path)


def cash_data(path: Path) -> None:
    pass


