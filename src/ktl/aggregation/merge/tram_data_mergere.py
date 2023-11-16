from typing import Tuple, List

import pandas as pd
import json


def merge_xslx_data_to_from_ttss() -> None:
    vehicles_type = pd.read_pickle("./data/generated/pickle/vehicles_by_type.pkl")
    attributes = pd.read_excel("./data/Tramwaje_dane_modeli.xlsx")
    lines = pd.read_pickle("./data/generated/pickle/vehicles_in_ttss.pkl")
    departures = pd.read_pickle("./data/generated/pickle/departures.pkl")
    time_table = pd.read_pickle("./data/generated/pickle/time_table.pkl")

    vehicles_type['merge'] = vehicles_type.apply(
        lambda x: str(x['tram_depo_code']) + str(x['tram_code']) + str(x['id']), axis=1)

    vehicles_type = vehicles_type[vehicles_type["name"].str.contains("NaN") == False]

    result = pd.merge(vehicles_type, attributes, how="inner", on="name")
    result = pd.merge(result, lines, how="inner", on="id")
    result.drop(['last_seen', 'latitude', 'longitude', 'direction'], axis=1, inplace=True)
    result.to_json("./data/generated/json/vehicles_full_data.json", orient="records", force_ascii=False)

    out: dict[str, List[Tuple[str, int, int]]] = {}
    start_time: int = 7
    end_time: int = 19

    departures = departures.where(start_time <= departures['hour']).dropna()
    departures = departures.where(departures['hour'] <= end_time).dropna()
    departures['absolute'] = departures.apply(lambda x: x['hour'] * 60 + x['minute'], axis=1)

    for idx, row in result.iterrows():
        id: str = str(row['id'])
        line: str = str(row['line'])
        out[id] = []
        stops: pd.DataFrame = time_table.where(time_table['line'] == line).dropna()
        if stops.size == 0:
            continue
        stops.sort_values(by=['order'], inplace=True, ascending=True)
        first_stop: str = str(stops.iloc[0]['name'])
        prev_absolute_time: float = departures.where(departures['name'] == first_stop).dropna().where(departures['line'] == line).dropna().iloc[0]['absolute']

        for _, stop in stops.iterrows():
            stop_name: str = str(stop['name'])
            suitable_hours = departures.where(departures['name'] == stop_name).dropna()
            suitable_hours = suitable_hours.where(suitable_hours['line'] == line).dropna()
            suitable_hours = suitable_hours.where(suitable_hours['direction'] == 'START_END').dropna()
            suitable_hours = suitable_hours.where(suitable_hours['absolute'] > prev_absolute_time).dropna()
            suitable_hours.sort_values(by=['hour', 'minute'], inplace=True)

            if suitable_hours.size == 0:
                break
            idx = suitable_hours.iloc[0].index
            prev_absolute_time = suitable_hours.iloc[0]['absolute']
            out[id].append((stop_name, suitable_hours.iloc[0]['hour'], suitable_hours.iloc[0]['minute']))
            departures.drop([idx], inplace=True)

        stops.sort_values(by=['order'], inplace=True, ascending=False)

        for _, stop in stops.iterrows():
            stop_name: str = str(stop['name'])
            suitable_hours = departures.where(departures['name'] == stop_name).dropna()
            print(suitable_hours.to_string())
            suitable_hours = suitable_hours.where(suitable_hours['line'] == line).dropna()
            suitable_hours = suitable_hours.where(suitable_hours['direction'] == 'END_START').dropna()
            suitable_hours = suitable_hours.where(suitable_hours['absolute'] > prev_absolute_time).dropna()
            suitable_hours.sort_values(by=['absolute'], inplace=True)
            if suitable_hours.size == 0:
                break
            idx = suitable_hours.index[0]
            prev_absolute_time = suitable_hours.iloc[0]['absolute']
            out[id].append((stop_name, suitable_hours.iloc[0]['hour'], suitable_hours.iloc[0]['minute']))
            departures.drop([idx], inplace=True)

    with open("./data/generated/json/vehicles_arrival_times.json", "w", encoding="utf-8") as output_file:
        json.dump(out, output_file, indent=4, ensure_ascii=False)
