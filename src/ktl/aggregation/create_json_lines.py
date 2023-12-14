from pathlib import Path

import pandas as pd
import json
import re


def create_json():
    df_stops = pd.read_excel('data/generated/excel/tram_stops.xlsx')
    df_time = pd.read_excel('data/generated/excel/time_table.xlsx')
    merged = pd.merge(df_stops, df_time, right_on='stop_name', left_on='name', how='inner')

    merged = merged[['stop_name', 'geometry', 'line', 'order', 'direction']]
    # print(merged.to_string())
    tram_stops = {}

    for index, row in merged.iterrows():
        line = row['line']
        order = row['order']
        direction = row['direction']

        # if row['stop_name'][-2:].strip().isdigit():
        #     stop_name = row['stop_name'][:-3].strip()
        #     stop_nr = row['stop_name'][-2:].strip()
        # else:
        #     stop_name = row['stop_name'].strip()
        #     stop_nr = ''

        geometry = row['geometry']
        match = re.match(r"POINT \(([\d.]+) ([\d.]+)\)", geometry)
        if match:
            x = float(match.group(1))
            y = float(match.group(2))
            stop_position = (x, y)
        else:
            x = None
            y = None

        tram_stop = (line, order, row['stop_name'], stop_position, direction)

        if '' in tram_stops:
            tram_stops[''].append(tram_stop)
        else:
            tram_stops[''] = [tram_stop]

    # Use 'ensure_ascii=False' to avoid escaping non-ASCII characters
    json_string = json.dumps(tram_stops, ensure_ascii=False, indent=4)

    return json_string


def json_to_txt():
    # with open('data/generated/tram_stops.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    #
    # with open('data/generated/tram_stops.txt', 'w', encoding='utf-8') as f:
    #     f.write(f"line,\t order,\t stop_name,\t stop_nr,\t stop_position\n")
    #     for key, value in data.items():
    #         for item in value:
    #             line, order, stop_name, stop_nr, stop_position = item
    #             f.write(f"{line},\t {order},\t {stop_name},\t {stop_nr},\t {stop_position}\n")
    pass


# json_data = create_json()


def save_json_to_file():
    json_string = create_json()

    print(json_string)

    Path('./data/generated/json/').mkdir(exist_ok=True, parents=True)

    with open('./data/generated/json/tram_stops.json', 'w', encoding='utf-8') as f:
        # json.dump(json_string, f, ensure_ascii=False, indent=4)
        f.write(json_string)

    # json_to_txt()


if __name__ == '__main__':
    save_json_to_file()
