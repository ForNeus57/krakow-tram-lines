"""
Main module of the acquisition data later referred as a package.
"""

from sys import argv

from ktl.acquisition.acquire.receiver import Receiver
from ktl.acquisition.config import ConfigParser, Config
from ktl.acquisition.data.package import Package
from ktl.acquisition.data.saver import Saver


def main() -> None:
    """
    Main function of the acquisition data process.

    It parses the command line arguments and then creates a config object.
    Which is then used to create a package object (contains parameters specified like urls and so on).
    Then it creates a data saver object which is used to save the data to disk.
    """
    parser: ConfigParser = ConfigParser(argv)
    config: Config = parser.parse()

    package: Package = Receiver(config.info).receive()
    saver = Saver(package, config.saving_info)
    saver.save()


if __name__ == "__main__":
    main()
