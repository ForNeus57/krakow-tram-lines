from pathlib import Path


from web.tram_models import TramModelsData
from web.tram_time_table import TramTimeTableData

from web.tram_model_attributes_data import TramModelsAttributesData

from web.constants import  TRAM_NAME_LENGTH, DEFAULT_TRAM_MODELS_SAVE_PATH, TRAM_MODELS_ATTRIBUTES



def acquire(caching_path: Path) -> None:
    """
    Function that gathers data from web (OSMNX API and from web-scrapers)
    :return:
    """
    """ dominik kazał zakomentować #2
    models = TramModelsData.from_url(caching_path)
    # TramTimeTableData.from_url(models)    DOESN'T WORK!
    """

def cash_data(path: Path) -> None:
    pass

TramModelsAttributesData.from_excel(DEFAULT_TRAM_MODELS_SAVE_PATH, TRAM_MODELS_ATTRIBUTES)

