from dataclasses import dataclass


@dataclass(frozen=True)
class WebscrapingOptions:
    """
    Class that represents the options for the Web scrapping data acquisition.
    .. seealse:: ./res/config.json
    """
    ttss_data_source_url: str
