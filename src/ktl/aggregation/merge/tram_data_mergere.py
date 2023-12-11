from typing import Tuple, List

import re

import pandas as pd
import json


def merge_xslx_data_to_from_ttss() -> None:
    vehicles_type = pd.read_pickle("./data/generated/pickle/vehicles_by_type.pkl")
    attributes = pd.read_excel("./data/Tramwaje_dane_modeli.xlsx")
    lines = pd.read_pickle("./data/generated/pickle/vehicles_in_ttss.pkl")
    departures = pd.read_pickle("./data/generated/pickle/departures.pkl")
    time_table = pd.read_pickle("./data/generated/pickle/time_table.pkl")

    result = prepare_tram_trains_data(vehicles_type, attributes, lines)

    out: dict[str, List[Tuple[str, int, int]]] = {}
    start_time: int = 7
    end_time: int = 19

    mode: str = 'START_END'
    reversed_mode: str = 'END_START'

    departures = departures.where(start_time <= departures['hour']).dropna()
    departures = departures.where(departures['hour'] <= end_time).dropna()
    departures['absolute'] = departures.apply(lambda x: x['hour'] * 60 + x['minute'], axis=1).astype(int)

    for _, row in result.iterrows():
        identifier: str = str(row['id'])
        line: str = str(row['line'])
        out[identifier] = []

        stops: pd.DataFrame = time_table[(time_table['line'] == line) & (time_table['direction'] == mode)]
        if len(stops) == 0:
            continue
        stops = stops.sort_values(by=['order'], ascending=True)

        first_stop: str = str(stops.iloc[0]['stop_name'])

        prev_absolute_time: int = \
            departures[(departures['name'] == first_stop) & (departures['line'] == line)].iloc[0]['absolute']

        while True:
            found = False
            for _, stop in stops.iterrows():
                stop_name: str = stop['stop_name']
                # print(stop_name)
                suitable_hours: pd.DataFrame = (departures[(departures['name'] == stop_name) &
                                                           (departures['line'] == line) &
                                                           (departures['direction'] == mode) &
                                                           (departures['absolute'] > prev_absolute_time)]
                                                .sort_values(by=['hour', 'minute'], ascending=True))
                if not len(suitable_hours) > 0:
                    found = False
                    break

                found = True
                prev_absolute_time = suitable_hours.iloc[0]['absolute']
                departures.drop(index=suitable_hours.index[0], axis=0, inplace=True)
                out[identifier].append((stop_name, suitable_hours.iloc[0]['hour'], suitable_hours.iloc[0]['minute']))

            if not found:
                break

            stops: pd.DataFrame = time_table[(time_table['line'] == line) & (time_table['direction'] == reversed_mode)]

            for _, stop in stops.sort_values(by=['order'], ascending=True).iterrows():
                stop_name: str = stop['stop_name']
                # print(stop_name)
                suitable_hours: pd.DataFrame = (departures[(departures['name'] == stop_name) &
                                                           (departures['line'] == line) &
                                                           (departures['direction'] == reversed_mode) &
                                                           (departures['absolute'] > prev_absolute_time)]
                                                .sort_values(by=['hour', 'minute'], ascending=True))
                if not len(suitable_hours) > 0:
                    found = False
                    break

                found = True
                prev_absolute_time = suitable_hours.iloc[0]['absolute']
                departures.drop(index=suitable_hours.index[0], axis=0, inplace=True)
                out[identifier].append((stop_name, suitable_hours.iloc[0]['hour'], suitable_hours.iloc[0]['minute']))

            if not found:
                break

    save_data(result, out)


def prepare_tram_trains_data(vehicles_type: pd.DataFrame,
                             attributes: pd.DataFrame,
                             lines: pd.DataFrame) -> pd.DataFrame:
    vehicles_type['merge'] = vehicles_type.apply(
        lambda x: str(x['tram_depo_code']) + str(x['tram_code']) + str(x['id']), axis=1)

    vehicles_type = vehicles_type[vehicles_type["name"].str.contains("NaN") == False]

    result = pd.merge(vehicles_type, attributes, how="inner", on="name")
    result = pd.merge(result, lines, how="inner", on="id")
    result.drop(['last_seen', 'latitude', 'longitude', 'direction'], axis=1, inplace=True)
    return result


def save_data(trains_data: pd.DataFrame, trains_schedule_data: dict[str, List[Tuple[str, int, int]]]) -> None:
    trains_data.to_json("./data/generated/json/vehicles_full_data.json", orient="records", force_ascii=False, indent=4)

    with open("./data/generated/json/vehicles_arrival_times.json", "w", encoding="utf-8") as output_file:
        json.dump(trains_schedule_data, output_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    merge_xslx_data_to_from_ttss()
