from dataclasses import dataclass, KW_ONLY


@dataclass(frozen=True)
class OSMNXOptions:
    """
    Class that represents the options for the OSMNX data acquisition.
    .. seealse:: ./res/config.json
    """
    _: KW_ONLY
    tram_stop_tags: dict[str, str]
    tram_tracks_custom_filter: str