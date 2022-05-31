# encoding: windows-1254
import requests
import pandas as pd
import datetime
import sys
from pathlib import Path
import os

from src.data.load_cfg import load_config


def get_all():
    configs = load_config()
    url = configs["APIs"]["GET_POI_SERVICE"]["API_KEY"]
    headers = {
        "Authorization": configs["APIs"]["GET_POI_SERVICE"]["TOKEN"],
        "Content-Type": "application/json",
    }

    response = requests.request("GET", url, headers=headers)
    df = pd.DataFrame(response.json())
    return df


def save_df(df, filtering=True):

    # Directory configs
    configs = load_config()
    path = configs["PATHS"]["PROCESSED"]
    ROOT_STRING = os.getcwd().split("geo-clustering-project")[0] + "geo-clustering-project"
    ROOT_DIR = Path(ROOT_STRING)

    # Data Manipulation
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
        df = df.loc[(df.cat2 == "Vestel Lokasyonlar") | (df.cat2 == "Aktif Rakipler")]
        df = df.loc[(df.cat3 == "Vestel Rakipler") | (df.cat3 == "Aktif Mağazalar")]
        df = df.loc[(df["cat4"] != "Regal") & (df["cat5"] != "Vestel Outlet")]
        df = df.rename(columns={"cat4": "Kategori 5"})
        df["Kategori 4"] = df["cat5"].str[7:]
        df["Kategori 4"] = df["Kategori 4"].replace({"Kurumsal express": "Kurumsal Express"})
        df.drop(columns="cat5", inplace=True)
        df["Kategori 4"] = df.apply(lambda x: "Öncelikli Rakipler" if x["Kategori 5"] != "Vestel" else x["Kategori 4"], axis=1)
        df = df.rename(columns=rename_dict)[use_cols]
        df = df.loc[df["Kategori 5"].isin(brands)]
        file_name = f"Rakip_Vestel_NextGeo_{formatted_time}.xlsx"

    else:
        file_name = f"Rakip_Vestel_NextGeo_{formatted_time}_unfiltered.xlsx"

    target_path = Path(ROOT_DIR, path, file_name)
    file_name = Path(target_path)
    df.to_excel(file_name, index=False)
