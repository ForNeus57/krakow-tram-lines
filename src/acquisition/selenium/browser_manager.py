import os
from pathlib import Path

import wget
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from src.acquisition.selenium.constants import DRIVER_DOWNLOAD_PATH, URL_TO_DOWNLOAD_DRIVER


class BrowserManager:
    """

    """
    def __init__(self, driver_path: Path = DRIVER_DOWNLOAD_PATH, url: str = URL_TO_DOWNLOAD_DRIVER):
        self.driver_path: Path = driver_path
        self.url: str = url
        path_to_driver: Path = self.download_correct_driver()

        service = Service(str(path_to_driver.joinpath("chromedriver.exe")))

        self.browser: WebDriver = webdriver.Chrome(service=service)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def download_correct_driver(self) -> Path:
        # TODO:  Make better paths
        Path.mkdir(self.driver_path, parents=True, exist_ok=True)

        download_path: Path = self.driver_path.joinpath(r"chromedriver-win64.zip")

        if not os.path.exists(download_path):
            wget.download(self.url, out=str(self.driver_path))

        if not os.path.exists(self.driver_path.joinpath(r"chromedriver-win64")):
            with ZipFile(download_path, 'r') as zip_object:
                zip_object.extractall(self.driver_path)

        return self.driver_path.joinpath(r"chromedriver-win64")
