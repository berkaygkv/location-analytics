# encoding: windows-1254
import requests
import pandas as pd
import datetime
import sys
import yaml
import os

config_file_path = "config.yaml"
if not os.path.exists(config_file_path):
    config_file_path = "../config.yaml"

with open(config_file_path, "r") as f:
    configs = yaml.safe_load(f)


def get_all():
    url = configs["APIs"]["GET_POI_SERVICE"]["API_KEY"]
    headers = {
        "Authorization": configs["APIs"]["GET_POI_SERVICE"]["TOKEN"],
        "Content-Type": "application/json",
    }

    response = requests.request("GET", url, headers=headers)
    df = pd.DataFrame(response.json())
    return df


def save_df(df, filtering=True):
    brands = ["Siemens", "Arçelik", "Samsung", "Bosch", "Beko", "Vestel"]
    rename_dict = {
        "id": "Nokta ID",
        "name": "Nokta Adı",
        "address": "Adres",
        "cat1": "Kategori 1",
        "cat2": "Kategori 2",
        "cat3": "Kategori 3",
        "cat4": "Kategori 4",
        "cat5": "Kategori 5",
        "city_name": "İl",
        "city_code": "İl Kodu",
        "county_name": "İlçe",
        "county_code": "İlçe Kodu",
        "district_name": "Mahalle",
        "district_code": "Mahalle Kodu",
        "lat": "Latitude - Enlem - Y",
        "lon": "Longitude - Boylam - X",
    }
    use_cols = rename_dict.values()
    time_var = datetime.datetime.now()
    formatted_time = time_var.strftime("%d_%b_%Y")

    if filtering:
        df = df.rename(columns=rename_dict)[use_cols]
        df = df.loc[df["Kategori 5"].isin(brands)]
        file_name = f"Rakip_Vestel_NextGeo_{formatted_time}.xlsx"

    else:
        file_name = f"Rakip_Vestel_NextGeo_{formatted_time}_unfiltered.xlsx"

    df.to_excel(file_name, index=False)
