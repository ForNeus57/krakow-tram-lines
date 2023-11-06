"""
Class that is required to download necessary drivers for chrome in order for selenium to do it's magic.
"""

from pathlib import Path
from zipfile import ZipFile
import os
import wget

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from ktl.acquisition.data.selenium.constants import DRIVER_DOWNLOAD_PATH, URL_TO_DOWNLOAD_DRIVER


class BrowserManager:
    """
    Class that manages access to browser, by making sure to only create one browser window on whole aplication.
    It also is responsible for downloading correct browser drivers.
    """
    def __init__(self, driver_path: Path = DRIVER_DOWNLOAD_PATH, url: str = URL_TO_DOWNLOAD_DRIVER):
        self.driver_path: Path = driver_path
        self.url: str = url
        path_to_driver: Path = self.download_correct_driver()

        service = Service(str(path_to_driver))

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

    def download_correct_driver(self) -> Path:
        """
        Method that downloads drivers based on if the correct files exist in a directory.
        #TODO: Make so that this class does not break solid.
        """
        Path.mkdir(self.driver_path, parents=True, exist_ok=True)

        download_path: Path = self.driver_path.joinpath(r"chromedriver-win64.zip")
        executable_folder_path: Path = self.driver_path.joinpath(r"chromedriver-win64")

        #   Download drivers
        if not os.path.exists(download_path):
            wget.download(self.url, out=str(self.driver_path))

        #   Unzip the downloaded file into an executable.
        if not os.path.exists(executable_folder_path):
            with ZipFile(download_path, 'r') as zip_object:
                zip_object.extractall(self.driver_path)

        return executable_folder_path.joinpath("chromedriver.exe")
