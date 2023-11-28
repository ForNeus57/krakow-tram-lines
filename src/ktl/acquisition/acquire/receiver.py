from ktl.acquisition.acquire.info import Info
from ktl.acquisition.data.package import Package
from ktl.acquisition.data.osmnx.tram_stops import StopsData
from ktl.acquisition.data.osmnx.tram_tracks import TracksData
from ktl.acquisition.data.selenium.drivers.browser_manager import BrowserManager
from ktl.acquisition.data.selenium.latency_data import LatencyData
from ktl.acquisition.data.selenium.time_table_data import TimeTableData
from ktl.acquisition.data.excel.tram_model_attributes_data import ModelsAttributesData
from ktl.acquisition.data.web.tram_models import ModelsData


class Receiver:

    def __init__(self, info: Info):
        self.info = info

    def receive(self) -> Package:
        # Data from OSMNX
        tracks = TracksData.from_api(self.info.osmnx_options)
        stops = StopsData.from_api(self.info.osmnx_options)

        # Data from webscraping
        models = ModelsData.from_url(self.info.webscraping_options)

        # Data from excel
        # models_attributes = ModelsAttributesData.from_excel(self.info.excel_options)

        # Data from Selenium
        with BrowserManager(self.info.selenium_options) as bm:
            time_table = TimeTableData.from_selenium(bm.browser, self.info.selenium_options)
            # Temporarily doesn't work
            # latency = LatencyData.from_selenium(bm.browser, stops.tram_stops['name'], self.info.selenium_options)

            return Package(tracks, stops, models, ModelsAttributesData(None), time_table, LatencyData(None))
