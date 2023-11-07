"""
Webscraper made with Selenium lib to get the latency data from the website of the public transport.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import geopandas as gpd

from ktl.acquisition.data.selenium.drivers.browser_manager import BrowserManager
from ktl.acquisition.data.selenium.options import SeleniumOptions


@dataclass(frozen=True)
class LatencyData:
    """
    Class that represents the latency data.
    One public attribute that is a pandas DataFrame with the latency data.
    """
    latency: pd.DataFrame

    @classmethod
    def from_selenium(cls, browser: WebDriver, stops: gpd.GeoSeries, options: SeleniumOptions) -> LatencyData:
        """
        Custom data constructor that uses Selenium to retrieve data about the latency of the trams.
        """
        browser.get(options.latency_data_source_url)
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
        """
        Class method that is used to normalize stops data.
        I.e. make it so that we do not have Lubicz 01, but instead we have Lubicz.
        Website used for web-scraping accepts that format.
        """
        return stops.apply(lambda x: x[:len(x) - 3] if x[len(x) - 1].isdigit() else x).drop_duplicates()

    @classmethod
    def get_stop_data(cls, browser: WebDriver, stop: str) -> List[List[str]]:
        """
        Method that is used to get data using selenium.
        """
        timeout: int = 10

        xpath: str = r'//*[@id="isg2_search_panel_container"]/div/form/div/input'
        BrowserManager.await_element_on_browser(browser, timeout, xpath)
        elem = browser.find_element(by=By.XPATH, value=xpath)
        elem.send_keys(stop, Keys.RETURN)

        xpath: str = r'//*[@id="autocomplete"]/li[2]/div/div/a'
        BrowserManager.await_element_on_browser(browser, timeout, xpath)
        browser.find_element(by=By.XPATH, value=xpath).click()

        table_body = browser.find_element(by=By.TAG_NAME, value="tbody")
        table_rows = table_body.find_elements(by=By.TAG_NAME, value="tr")

        full_data: List[List[str]] = []
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
        BrowserManager.await_element_on_browser(browser, timeout, xpath)
        browser.find_element(by=By.XPATH, value=xpath).click()

        elem.clear()

        return full_data if full_data is not None else []
