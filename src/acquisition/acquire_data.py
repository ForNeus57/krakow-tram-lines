from pathlib import Path

from src.acquisition.web.tram_models import TramModelsData


def acquire(caching_path: Path) -> None:
    """
    Function that gathers data from web (OSMNX API and from web-scrapers)
    :return:
    """
    models = TramModelsData.from_url(caching_path)
    print(models.vehicles_by_line.to_string())


def cash_data(path: Path) -> None:
    pass
