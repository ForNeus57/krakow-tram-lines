from ktl.acquisition.acquire.info import Info
from ktl.acquisition.data.package import Package
from ktl.acquisition.data.osmnx.tram_stops import TramStopsData
from ktl.acquisition.data.osmnx.tram_tracks import TramTracksData
from ktl.acquisition.data.selenium.browser_manager import BrowserManager
from ktl.acquisition.data.selenium.latency_data import LatencyData
from ktl.acquisition.data.web.tram_model_attributes_data import TramModelsAttributesData
from ktl.acquisition.data.web.tram_models import TramModelsData


class Receiver:

    def __init__(self, info: Info):
        self.info = info

    def receive(self) -> Package:
        models = TramModelsData.from_url()
        # time_table = TramTimeTableData.from_url(models)
        models_data = TramModelsAttributesData.from_excel()
        tracks = TramTracksData.from_api()
        stops = TramStopsData.from_api()

        with BrowserManager() as bm:
            latency = LatencyData.from_selenium(bm.browser, stops.tram_stops['name'])

        return None
