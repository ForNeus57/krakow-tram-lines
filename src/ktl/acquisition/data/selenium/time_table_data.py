from __future__ import annotations
from dataclasses import dataclass
from io import StringIO

import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from ktl.acquisition.data.selenium.drivers.browser_manager import BrowserManager
from ktl.acquisition.data.selenium.options import SeleniumOptions


@dataclass(frozen=True)
class TimeTableData:
    """
    Class that represents the latency data.
    One public attribute that is a pandas DataFrame with the latency data.
    """
    time_table: pd.DataFrame

    @classmethod
    def from_selenium(cls, browser: WebDriver, options: SeleniumOptions) -> TimeTableData:
        """
        """
        browser.get(options.time_table_data_source_url)

        time_table = cls.get_time_table_data(browser)

        return cls(time_table)

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

        parent: WebElement = browser.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td")

        links = parent.find_elements(by=By.TAG_NAME, value="*")

        size = len(links)

        for idx in range(size):
            element = browser.find_element(by=By.XPATH, value=f"/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[3]/td/a[{idx + 1}]")
            line_number = element.text.strip()
            element.click()
            BrowserManager.await_element_on_browser(browser, 10, "/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table")
            table = browser.find_element(by=By.XPATH, value="/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table")
            df = pd.read_html(StringIO(table.get_attribute('outerHTML')))[1]
            df.insert(0, 'order', range(len(df)))
            df['line'] = line_number
            df['name'] = df[0]
            df = df[['line', 'order', 'name']]
            time_table = pd.concat([time_table, df])

        return time_table

    @classmethod
    def set_start(cls, browser: WebDriver) -> None:
        xpath: str = r'/html/body/table/tbody/tr/td/table/tbody/tr[1]/td/table[1]/tbody/tr[3]/td/a[1]'
        browser.find_element(by=By.XPATH, value=xpath).click()

        xpath: str = r'/html/body/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/a'
        browser.find_element(by=By.XPATH, value=xpath).click()
