from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DriverOptions:
    """
    Class that represents the options for the Selenium data acquisition.
    .. seealse:: ./res/config.json
    """
    download_url: str
    download_file: Path
    executable: Path


