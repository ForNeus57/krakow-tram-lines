"""
Set of constants used in selenium module.
"""

from pathlib import Path

URL_TO_DOWNLOAD_DRIVER: str = (r'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/win64'
                               r'/chromedriver-win64.zip')

URL_TO_LATENCY_DATA: str = r'http://www.ttss.krakow.pl/'

DRIVER_DOWNLOAD_PATH: Path = Path(r'./cache/')
