

import pandas as pd


def merge_xslx_data_to_from_ttss() -> None:
    vehicles_type = pd.read_pickle("./data/generated/pickle/vehicles_by_type.pkl")
    attributes = pd.read_excel("./data/Tramwaje_dane_modeli.xlsx")
    lines = pd.read_pickle("./data/generated/pickle/vehicles_in_ttss.pkl")
    departures = pd.read_pickle("./data/generated/pickle/departures.pkl")

    vehicles_type['merge'] = vehicles_type.apply(lambda x: str(x['tram_depo_code']) + str(x['tram_code']) + str(x['id']), axis=1)

    vehicles_type = vehicles_type[vehicles_type["name"].str.contains("NaN") == False]

    result = pd.merge(vehicles_type, attributes, how="inner", on="name")
    result = pd.merge(result, lines, how="inner", on="id")
    result.drop(['last_seen', 'latitude', 'longitude', 'direction'], axis=1, inplace=True)
    print(result.head())
    print(len(result))

    result.to_json("./data/generated/json/vehicles_full_data.json", orient="records", force_ascii=False)

