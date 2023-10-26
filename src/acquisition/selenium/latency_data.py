from __future__ import annotations

import datetime
import time
from pathlib import Path
from dataclasses import dataclass
from typing import List

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import geopandas as gpd

from src.acquisition.selenium.constants import URL_TO_LATENCY_DATA


@dataclass(frozen=True)
class LatencyData:
    latency: pd.DataFrame

    @classmethod
    def from_selenium(cls, browser: WebDriver, stops: gpd.GeoSeries, url: str = URL_TO_LATENCY_DATA) -> LatencyData:
        browser.get(url)

        stops = stops.apply(lambda x: x[:len(x) - 3] if x[len(x) - 1].isdigit() else x)

        stops.drop_duplicates(inplace=True)

        latency = pd.DataFrame(
            columns=['line', 'tram_direction', 'estimated_time_of_arrival', 'stop', 'measurement_time'])

        for idx, stop in stops.items():
            for row in cls.get_stop_data(browser, stop):
                latency.loc[len(latency)] = row

        time.sleep(3000)

        return cls(latency)

    @classmethod
    def get_stop_data(cls, browser: WebDriver, stop: str) -> List[List[str]]:
        elem = browser.find_element(by=By.XPATH, value=r'//*[@id="isg2_search_panel_container"]/div/form/div/input')
        elem.send_keys(stop)
        elem.send_keys(Keys.RETURN)

        full_data: List[List[str]] = []

        # TODO: remove ; use WebDriverWait
        try:
            time.sleep(2)
            browser.find_element(by=By.XPATH, value=r'//*[@id="autocomplete"]/li[2]/div/div/a').click()
            time.sleep(2)

            table_body = browser.find_element(by=By.TAG_NAME, value="tbody")
            table_rows = table_body.find_elements(by=By.TAG_NAME, value="tr")

            for row in table_rows:
                table_data = row.find_elements(by=By.TAG_NAME, value="td")
                data = [x.text for x in table_data if not x.text == '']
                data.append(stop)
                data.append(str(datetime.datetime.now()))
                full_data.append(data)

            # TODO: remove ; use WebDriverWait
            time.sleep(2)
            browser.find_element(by=By.XPATH, value=r'//*[@id="isg2_search_panel_header"]/a').click()
            time.sleep(2)

        except NoSuchElementException as err:
            print(err.msg)

        elem.clear()

        return full_data if full_data is not None else []
