from ktl.aggregation.create_json_lines import save_json_to_file
from ktl.aggregation.aggregate_tracks import aggregate_tracks
from ktl.aggregation.merge.tram_data_mergere import merge_xslx_data_to_from_ttss


def main() -> None:
    save_json_to_file()
    aggregate_tracks()
    merge_xslx_data_to_from_ttss()



if __name__ == "__main__":
    main()