"""
Module used to parse the command line arguments and create a Config object for whole application.
"""

from dataclasses import dataclass
from pathlib import Path
import argparse

from ktl.acquisition.acquire.info import Info, InfoFileScanner
from ktl.acquisition.data.saver_info import SavingInfo


@dataclass(frozen=True)
class Config:
    """
    Helper class used to distinguish which data is used for what.

    .. seealso:: :class:`Info`
    .. seealso:: :class:`SavingInfo`
    """
    info: Info
    saving_info: SavingInfo


class ConfigParser:
    """

    .. seealso:: :class:`Config`
    .. seealso:: :class:`MainStreamConfigFileParser`
    """

    def __init__(self, argv: list[str]):
        self.argv = argv
        self.parser = argparse.ArgumentParser(prog='ProgramName',
                                              description='What the program does',
                                              epilog='Text at the bottom of help')

        # Configuration of the program cli arguments.
        self.parser.add_argument('-c', '--config',
                                 type=Path,
                                 help='Path to the file with configuration (JSON).',
                                 required=True,
                                 nargs=1)
        self.parser.add_argument('-s', '--save_path',
                                 type=Path,
                                 help='Path to save the generated data to.',
                                 required=True,
                                 nargs=1)
        self.parser.add_argument('-f', '--force_data_save',
                                 type=bool,
                                 help='Override data if it already exists.',
                                 required=False,
                                 nargs=1,
                                 default=False)
        self.parser.add_argument('-o', '--output_format',
                                 type=str,
                                 help='Output format of the data.',
                                 required=False,
                                 nargs=1,
                                 choices=['excel', 'pickle', 'both'],
                                 default='both')

    def parse(self) -> Config:
        """
        Method that parses the command line arguments and creates a Config object.
        :return: Config object filled with configuration.
        """
        args = self.parser.parse_args(self.argv[1:])

        info_file_scanner: InfoFileScanner = InfoFileScanner(*args.config)
        info: Info = info_file_scanner.scan()
        saving_info: SavingInfo = SavingInfo(*args.save_path, args.force_data_save, args.output_format)

        return Config(info, saving_info)
