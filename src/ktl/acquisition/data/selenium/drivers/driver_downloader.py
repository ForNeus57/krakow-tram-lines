from pathlib import Path
from zipfile import ZipFile
import os
import wget


class DriverDownloader:

    def __init__(self, download_url: str, download_path: Path, executable: str):
        self.download_url: str = download_url
        self.download_path: Path = Path(download_path)
        self.executable_name: str = executable
        self.driver_path: Path = Path(os.path.dirname(self.download_path)).joinpath(
            self.download_path.stem
        ).joinpath(
            self.executable_name
        )

    def download_driver(self):
        """
        Method that downloads drivers based on if the correct files exist in a directory.
        """
        Path.mkdir(Path(os.path.dirname(self.download_path)).joinpath(self.download_path.stem),
                   parents=True, exist_ok=True)

        #   Download drivers
        if not os.path.exists(self.download_path):
            wget.download(self.download_url, out=str(self.driver_path))

        #   Unzip the downloaded file into an executable.
        if not os.path.exists(Path(os.path.dirname(self.download_path)).joinpath(self.download_path.stem)):
            with ZipFile(self.download_path, 'r') as zip_object:
                zip_object.extractall(self.driver_path)
