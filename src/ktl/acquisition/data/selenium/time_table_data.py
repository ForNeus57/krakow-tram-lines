from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from io import StringIO

import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ktl.acquisition.data.selenium.drivers.browser_manager import BrowserManager
from ktl.acquisition.data.selenium.options import SeleniumOptions


class Direction(Enum):
    START_END = 0
    END_START = auto()

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class TimeTableData:
    """
    Class that represents the latency data.
    One public attribute that is a pandas DataFrame with the latency data.
    """
    time_table: pd.DataFrame
    departures: pd.DataFrame

    @classmethod
    def from_selenium(cls, browser: WebDriver, options: SeleniumOptions) -> TimeTableData:
        """
        """
        browser.get(options.time_table_data_source_url)

        time_table = cls.get_time_table_data(browser)

        departures = cls.get_time_table_departures(browser, time_table)

        return cls(time_table, departures)

    @classmethod
    def get_time_table_data(cls, browser: WebDriver) -> pd.DataFrame:
        """

        :param browser:
        :return:
        """

        time_table = pd.DataFrame(columns=[
            'line',
            'name',
        ])

        cls.set_start(browser)

        parent: WebElement = browser.find_element(by=By.XPATH,
                                                  value="/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td")

        links = parent.find_elements(by=By.TAG_NAME, value="*")

        size = len(links)

        for idx in range(size):
            element = browser.find_element(by=By.XPATH,
                                           value=f"/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/a[{idx + 1}]")
            line_number = element.text.strip()
            element.click()
            BrowserManager.await_element_on_browser(browser, 10,
                                                    "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table")
            table = browser.find_element(by=By.XPATH,
                                         value="/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table")
            df = pd.read_html(StringIO(table.get_attribute('outerHTML')))[1]
            df.insert(0, 'order', range(len(df)))
            df['line'] = line_number
            df['name'] = df[0]
            df = df[['line', 'order', 'name']]
            time_table = pd.concat([time_table, df])

        return time_table

    @classmethod
    def get_time_table_departures(cls, browser: WebDriver, time_table: pd.DataFrame) -> pd.DataFrame:
        hours = pd.DataFrame(columns=[
            'line',
            'name',
            'direction',
            'hour',
            'minute',
        ])

        parent: WebElement = browser.find_element(by=By.XPATH,
                                                  value="/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td")

        links = parent.find_elements(by=By.TAG_NAME, value="*")

        size = len(links)

        for idx in range(size):
            element = browser.find_element(by=By.XPATH,
                                           value=f"/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/a[{idx + 1}]")
            line_number = element.text.strip()
            element.click()
            BrowserManager.await_element_on_browser(browser, 10,
                                                    "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]")

            direction_links_parent: WebElement = browser.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]")

            directions = direction_links_parent.find_elements(by=By.TAG_NAME, value="a")

            for direction_index in range(len(directions)):
                direction_link = browser.find_element(by=By.XPATH,
                                               value=f"/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a[{direction_index + 1}]")
                direction_link.click()
                BrowserManager.await_element_on_browser(browser, 10,
                                                    "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table")

                stop_parent: WebElement = browser.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody")

                stops = stop_parent.find_elements(by=By.TAG_NAME, value="tr")

                for stop_index in range(len(stops) - 1):
                    stop: WebElement = browser.find_element(by=By.XPATH,
                                                            value=f"/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[{stop_index + 1}]/td[1]/a")

                    stop_text = stop.text.strip()
                    stop.click()
                    BrowserManager.await_element_on_browser(browser, 10,
                                                            f"/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[{stop_index + 1}]/td[1]/a")

                    table: WebElement = browser.find_element(by=By.XPATH,
                                                             value="/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table")

                    df = pd.read_html(StringIO(table.get_attribute('outerHTML')))[0]
                    for i, row in df.iterrows():
                        if i not in (0, len(df[1]) - 2, len(df[1]) - 1) and str(row[1]) != 'nan':
                            for minute in str(row[1]).split(' '):
                                hours.loc[len(hours)] = [line_number, stop_text, str(Direction(direction_index)), int(row[0]), int(minute[:2])]

        return hours

    @classmethod
    def set_start(cls, browser: WebDriver) -> None:
        xpath: str = r'/html/body/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[3]/td/a[1]'
        browser.find_element(by=By.XPATH, value=xpath).click()

        xpath: str = r'/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/a'
        browser.find_element(by=By.XPATH, value=xpath).click()
