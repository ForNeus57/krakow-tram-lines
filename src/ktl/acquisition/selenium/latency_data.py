from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    StaleElementReferenceException
import pandas as pd
import geopandas as gpd

from ktl.acquisition.selenium.constants import URL_TO_LATENCY_DATA


@dataclass(frozen=True)
class LatencyData:
    latency: pd.DataFrame

    @classmethod
    def from_selenium(cls, browser: WebDriver, stops: gpd.GeoSeries, url: str = URL_TO_LATENCY_DATA) -> LatencyData:
        browser.get(url)
        stops = cls.normalize_stops_data(stops)
        latency = pd.DataFrame(
            columns=['line', 'tram_direction', 'estimated_time_of_arrival', 'stop', 'measurement_time']
        )

        for _, stop in stops.items():  # The first element of the tuple is the index, which we don't need.
            for row in cls.get_stop_data(browser, stop):
                latency.loc[len(latency)] = row

        return cls(latency)

    @classmethod
    def normalize_stops_data(cls, stops: gpd.GeoSeries) -> gpd.GeoSeries:
        return stops.apply(lambda x: x[:len(x) - 3] if x[len(x) - 1].isdigit() else x).drop_duplicates()

    @classmethod
    def get_stop_data(cls, browser: WebDriver, stop: str) -> List[List[str]]:
        xpath: str = r'//*[@id="isg2_search_panel_container"]/div/form/div/input'
        elem = browser.find_element(by=By.XPATH, value=xpath)
        elem.send_keys(stop, Keys.RETURN)
        full_data: List[List[str]] = []

        timeout: int = 10

        xpath: str = r'//*[@id="autocomplete"]/li[2]/div/div/a'
        cls.await_element_on_browser(browser, timeout, xpath)
        browser.find_element(by=By.XPATH, value=xpath).click()

        table_body = browser.find_element(by=By.TAG_NAME, value="tbody")
        table_rows = table_body.find_elements(by=By.TAG_NAME, value="tr")

        for row in table_rows:
            try:
                table_data = row.find_elements(by=By.TAG_NAME, value="td")
                data = [x.text for x in table_data if x is not None and x.text == '']
                data.append(stop)
                data.append(str(datetime.datetime.now()))
                full_data.append(data)
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                continue

        xpath: str = r'//*[@id="isg2_search_panel_header"]/a'
        cls.await_element_on_browser(browser, timeout, xpath)
        browser.find_element(by=By.XPATH, value=xpath).click()

        elem.clear()

        return full_data if full_data is not None else []

    @classmethod
    def await_element_on_browser(cls, browser: WebDriver, timeout: int, xpath: str):
        driver_wait = WebDriverWait(browser,
                                    timeout,
                                    ignored_exceptions=[NoSuchElementException, ElementNotInteractableException,
                                                        StaleElementReferenceException])
        driver_wait.until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )
        driver_wait.until(
            ec.element_to_be_clickable((By.XPATH, xpath))
        )
