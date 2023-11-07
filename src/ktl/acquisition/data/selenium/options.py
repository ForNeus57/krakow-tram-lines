from dataclasses import dataclass

from ktl.acquisition.data.selenium.drivers.options import DriverOptions


@dataclass(frozen=True)
class SeleniumOptions:
    """
    Class that represents the options for the Selenium data acquisition.
    .. seealse:: ./res/config.json
    """
    driver_options: DriverOptions
    latency_data_source_url: str
    time_table_data_source_url: str
