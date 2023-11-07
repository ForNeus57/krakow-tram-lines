from dataclasses import dataclass


@dataclass(frozen=True)
class ExcelOptions:
    """
    Class that represents the options for the Excel data acquisition.
    .. seealse:: ./res/config.json
    """
    tram_models_attributes_source_sheet_path: str
    tram_models_filling_missing_source_sheet_path: str
