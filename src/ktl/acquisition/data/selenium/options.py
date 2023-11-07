from dataclasses import dataclass, KW_ONLY
from pathlib import Path


@dataclass(frozen=True)
class SeleniumOptions:
    """
    Class that represents the options for the Selenium data acquisition.
    .. seealse:: ./res/config.json
    """
    _: KW_ONLY
    driver_download_url: str
    driver_download_path: Path
    driver_executable: str
    latency_data_source_url: str
    time_table_data_source_url: str
