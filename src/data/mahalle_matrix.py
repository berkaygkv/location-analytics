import json
import requests
import pandas as pd
import numpy as np
import yaml
import time
import os
from src.data.load_cfg import load_config


def next_geo_matrix_service(points):
    configs = load_config()
    url = configs["APIs"]["DISTRICT_MATRIX_SERVICE"]["API_KEY"]
    payload = json.dumps({"points": points, "distance": 2500})
    headers = {
        "Authorization": configs["APIs"]["DISTRICT_MATRIX_SERVICE"]["TOKEN"],
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def convert_matrix_data(response):
    df_matrix = pd.DataFrame().from_dict(response.json()["info"]).explode("districts")
    df_matrix["val"] = df_matrix["districts"].map(lambda x: [k for k in x.values()])
    df_matrix["keys"] = df_matrix["districts"].map(lambda x: [k for k in x.keys()])
    df_matrix = df_matrix.explode(["val", "keys"]).drop(columns=["districts"])
    df_matrix = df_matrix.query(
        'keys == "city_name" or keys == "county_name" or keys == "district_name" or keys == "distance"'
    )
    distance = df_matrix.query('keys == "distance"')
    district = df_matrix.query('keys == "district_name"')
    city_name = df_matrix.query('keys == "city_name"')
    county_name = df_matrix.query('keys == "county_name"')
    df_concat = pd.concat(
        [
            distance[["id", "val"]],
            city_name[["val"]],
            county_name[["val"]],
            district[["val"]],
        ],
        axis=1,
    )
    df_concat.columns = ["id", "distance", "city_name", "county_name", "district"]
    df_concat["key"] = (
        df_concat["city_name"]
        + " - "
        + df_concat["county_name"]
        + " - "
        + df_concat["district"]
    )
    df_concat.drop(columns=["city_name", "county_name", "district"], inplace=True)
    df_unstack = (
        df_concat.reset_index(drop=True)
        .set_index(["id", "key"], append=True)
        .unstack(level=-1)["distance"]
    )
    df_unstack = df_unstack.reset_index().drop(columns="level_0")
    df_distance_matrix = df_unstack.groupby("id").agg(lambda x: list(x.dropna()))
    df_distance_matrix = df_distance_matrix.applymap(
        lambda x: np.nan if not len(x) else x[0]
    )
    return df_distance_matrix


def extract_closest_districts(df_distance_matrix):
    df_distance_matrix = df_distance_matrix.reset_index()
    df_distance_matrix.columns.name = None
    df_distance_matrix.rename(columns={"id": "isim"}, inplace=True)
    df_matrix_melt = (
        df_distance_matrix.melt(
            id_vars=["isim"], value_vars=df_distance_matrix.columns.drop("isim")
        )
        .dropna(subset=["value"])
        .sort_values(["isim", "value"])
    )
    df_matrix_groupby = (
        df_matrix_melt.groupby("isim")
        .agg({"variable": [lambda x: list(x)[:5], "count"]})
        .droplevel(0, axis=1)
        .rename(
            columns={"<lambda_0>": "list_of_districts", "count": "count_of_districts"}
        )
    )
    df_matrix_explode = df_matrix_groupby.explode("list_of_districts").reset_index()
    df_matrix_explode["order"] = 1
    df_matrix_explode["order"] = df_matrix_explode.groupby("isim").order.transform(
        "cumsum"
    )
    df_matrix_explode["order"] = df_matrix_explode["order"].map(
        lambda x: f"En yakin {x}. Mahalle"
    )
    df_matrix_pivot = df_matrix_explode.pivot(
        index="isim", columns="order", values="list_of_districts"
    )
    return df_matrix_pivot
