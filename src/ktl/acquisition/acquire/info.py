from dataclasses import dataclass
from pathlib import Path
import json

from ktl.acquisition.data.excel.options import ExcelOptions
from ktl.acquisition.data.osmnx.options import OSMNXOptions
from ktl.acquisition.data.selenium.options import SeleniumOptions
from ktl.acquisition.data.web.options import WebscrapingOptions


@dataclass(frozen=True)
class Info:
    """
    Wrapper class for all the options used in the data acquisition.

    .. seealso:: :class:`Config`
    .. seealso:: :class:`InfoFileScanner`
    .. seealso:: :class:`OSMNXOptions`
    .. seealso:: :class:`SeleniumOptions`
    .. seealso:: :class:`WebscrapingOptions`
    .. seealso:: :class:`ExcelOptions`
    """
    osmnx_options: OSMNXOptions
    selenium_options: SeleniumOptions
    webscraping_options: WebscrapingOptions
    excel_options: ExcelOptions


class InfoFileScanner:
    """
    Class that parses the JSON file to the data acquisition options.

    Class hierarchy structure is identical to the one in correct json file.
    """
    def __init__(self, path: Path):
        self.path = path

    def _get_json(self) -> dict:
        with self.path.open('r', encoding='utf-8') as file:
            return json.load(file)

    def scan(self) -> Info:
        json_data = self._get_json()

        osmnx_options = OSMNXOptions(**json_data['osmnx'])
        selenium_options = SeleniumOptions(**json_data['selenium'])
        webscraping_options = WebscrapingOptions(**json_data['webscraping'])
        excel_options = ExcelOptions(**json_data['excel'])

        return Info(osmnx_options, selenium_options, webscraping_options, excel_options)
