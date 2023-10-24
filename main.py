from pathlib import Path


from src.acquisition.acquire_data import acquire


def main():
    #   TODO: write script that make data/generated/data and data/generated/images
    acquire(Path("./data/generated/data/"))


if __name__ == '__main__':
    main()
