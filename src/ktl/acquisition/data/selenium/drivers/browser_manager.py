"""
Class that is required to download necessary drivers for chrome in order for selenium to do it's magic.
"""

from pathlib import Path

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from ktl.acquisition.data.selenium.drivers.driver_downloader import DriverDownloader
from ktl.acquisition.data.selenium.options import SeleniumOptions


class BrowserManager:
    """
    Class that manages access to browser, by making sure to only create one browser window on whole application.
    It also is responsible for downloading correct browser drivers.
    """

    def __init__(self, options: SeleniumOptions):
        self.driver_downloader = DriverDownloader(options.driver_download_url,
                                                  options.driver_download_path,
                                                  options.driver_executable)

        self.driver_downloader.download_driver()
        self.path_to_driver: Path = self.driver_downloader.driver_path

        service = Service(str(self.path_to_driver))

        self.browser: WebDriver = webdriver.Chrome(service=service)

    def __enter__(self):
        """
        Give access to browser window.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the access to browser window.
        """
        self.browser.quit()

    @staticmethod
    def await_element_on_browser(browser: WebDriver, timeout: int, xpath: str) -> None:
        """
        Method that is used to wait for an element to appear on the browser.
        :param browser: Webdriver that is used to browse the web.
        :param timeout: Timeout in seconds after which the method will throw an exception.
        :param xpath:   Xpath of the element that we are waiting for.
        """
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
