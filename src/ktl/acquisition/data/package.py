from dataclasses import dataclass

from ktl.acquisition.data.excel.tram_model_attributes_data import ModelsAttributesData
from ktl.acquisition.data.osmnx.tram_stops import StopsData
from ktl.acquisition.data.osmnx.tram_tracks import TracksData
from ktl.acquisition.data.selenium.latency_data import LatencyData
from ktl.acquisition.data.selenium.time_table_data import TimeTableData
from ktl.acquisition.data.web.tram_models import ModelsData


@dataclass(frozen=True)
class Package:
    tracks: TracksData
    stops: StopsData
    models: ModelsData
    model_attributes: ModelsAttributesData
    time_table: TimeTableData
    latencyData: LatencyData
