from ktl.aggregation.create_json_lines import save_json_to_file
<<<<<<< HEAD
from ktl.aggregation.aggregate_tracks import aggregate_tracks


def main() -> None:
    #save_json_to_file()
    aggregate_tracks()
=======
from ktl.aggregation.merge.tram_data_mergere import merge_xslx_data_to_from_ttss


def main() -> None:
    # save_json_to_file()
    merge_xslx_data_to_from_ttss()
>>>>>>> f45d0aca1f7b9bb41a75aeeb01e42622ac2e7020


if __name__ == "__main__":
    main()
