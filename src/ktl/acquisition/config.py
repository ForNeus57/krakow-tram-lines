from pathlib import Path

from ktl.acquisition.acquire.info import Info


class Config:
    def __init__(self, info: Info, saving_path: Path) -> None:
        self.info = info
        self.saving_path = saving_path


class ConfigParser:
    def __init__(self, argv: list[str]) -> None:
        pass

    def parse(self) -> Config:
        pass
