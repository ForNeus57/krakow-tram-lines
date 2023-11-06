from sys import argv

from ktl.acquisition.acquire.receiver import Receiver
from ktl.acquisition.config import ConfigParser, Config
from ktl.acquisition.data.package import Package
from ktl.acquisition.data.saver import Saver


def main() -> None:
    parser: ConfigParser = ConfigParser(argv)
    config: Config = parser.parse()

    package: Package = Receiver(config.info).receive()
    ds = Saver(package, config.saving_path)
    ds.save()


if __name__ == "__main__":
    main()
