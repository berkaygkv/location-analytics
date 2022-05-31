# encoding: windows-1254

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import geopandas as gpd
from sklearn.cluster import DBSCAN
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.ops import nearest_points
from geopy.distance import great_circle
import math
import plotly.express as px
import plotly.graph_objects as go
import ast
from src.data.string_fix import decoding_fix_dict
import openpyxl
from openpyxl.formatting.rule import IconSet, FormatObject
from openpyxl.formatting.rule import Rule
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
from copy import copy


def haversine(geo1, geo2):
    """
    Haversine distance hesaplama fonksiyonu.
    Args: geo1, geo2
    """

    lat1 = float(geo1.split(",")[0])
    lat2 = float(geo2.split(",")[0])

    lon1 = float(geo1.split(",")[1])
    lon2 = float(geo2.split(",")[1])

    d_lat = (lat2 - lat1) * math.pi / 180.0
    d_lon = (lon2 - lon1) * math.pi / 180.0
    lat1 = lat1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0
    a = pow(math.sin(d_lat / 2), 2) + pow(math.sin(d_lon / 2), 2) * math.cos(
        lat1
    ) * math.cos(lat2)
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


def get_epsilon(df_rakip, split=False):
    """
    DBScan'de kullanılacak epsilon parametresini hesaplama fonksiyonu. 
    
    -   Mağazaların birbirine olan uzaklıklarından bir distance matrix oluşturulur ve her satırdaki minimum değeri alınır. 
    -   Böylece minimum distance'lardan oluşan bir liste elde edilir.
    -   Çok büyük uzaklıklığa sahip sayıları listeden çıkarmak amacıyla %60'lık percentile değeri threshold olarak belirlenir.
    -   %60'lık percentile'ı sağlayan değerler üzerinden listenin Mean ve Std hesaplanır.
    -   Hesaplanan Mean ve Std üzerinden ise linear bir (custom) fonksiyon kurularak epsilon değeri bulunur.
    -   Epsilon için maksimum 0.75, minimum 0.18 değerleri makul kabul edilmiştir.

    """
    df1_filtered = df_rakip.copy().reset_index(drop=True).reset_index()
    df1_filtered["geo"] = df1_filtered.apply(
        lambda x: f"{x['latitude']},{x['longitude']}", axis=1
    )

    a = df1_filtered["geo"].to_numpy()
    b = df1_filtered["geo"].to_numpy()[:, None]

    vfunc = np.vectorize(haversine)
    distance_matrix = vfunc(a, b)
    flat_arr = distance_matrix.flatten()
    flat_arr = np.where(flat_arr == 0, np.nan, flat_arr)
    flat_arr = flat_arr[~np.isnan(flat_arr)]
    outlier_threshold = np.percentile(flat_arr, q=60)
    arr = np.where(
        (distance_matrix > outlier_threshold) | (distance_matrix == 0),
        np.nan,
        distance_matrix,
    )

    distance_mean = pd.DataFrame(arr).apply(np.min).mean()
    distance_median = pd.DataFrame(arr).apply(np.min).median()
    distance_std = pd.DataFrame(arr).apply(np.min).std()

    print("Mean: ", distance_mean)
    print("Std: ", distance_std)
    print("Median: ", distance_median)

    epsilon_value = distance_mean + (distance_std / 9)

    # Yamama için gerekli threshold
    centroid_distance_param = distance_mean * 1.6

    # Büyüme hesab? için kullan?lan threshold (minimum 2500 metre olarak kabul edilmi?tir.)
    distance_threshold = (
        round((distance_std * 0.6 + epsilon_value * 0.4) * 2.6, 1) * 1000
    )
    distance_threshold = min(distance_threshold, 2500)
    if not split:
        if epsilon_value >= 0.75:
            epsilon_value = 0.75
            centroid_distance_param = 0.75 * 1.4

        elif epsilon_value <= 0.18:
            epsilon_value = 0.18
            centroid_distance_param = 0.18 * 1.4

    return epsilon_value, centroid_distance_param, distance_threshold


def read_rakip_df(city_name, data_path):
    rename_cols = ["ID", "Marka", "İl", "İlçe", "Mahalle", "Latitude", "Longitude"]
    use_cols = [
        "Nokta ID",
        "Kategori 5",
        "İl",
        "İlçe",
        "Mahalle",
        "Latitude - Enlem - Y",
        "Longitude - Boylam - X",
    ]
    rename_fix = dict(zip(use_cols, rename_cols))
    df_rakip = pd.read_excel(data_path, usecols=use_cols)
    df_rakip.rename(columns=rename_fix, inplace=True)
    df_rakip.columns = [k.strip() for k in df_rakip.columns]
    df_rakip = df_rakip.loc[df_rakip["İl"] == city_name]
    df_rakip = df_rakip.copy().rename(
        columns={
            "Mahalle": "mahalle",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Marka": "isim",
            "İl": "il",
            "İlçe": "ilce",
        }
    )
    df_rakip["latitude"] = df_rakip["latitude"].astype(float)
    df_rakip["longitude"] = df_rakip["longitude"].astype(float)

    return df_rakip


def filter_mahalle(city_name, data_path, raw_data_directory):
    _df = read_and_convert_mahalle_polygon(raw_data_directory)
    initial = _df.il.str.strip().unique()[:, None]
    df_rakip = pd.read_excel(data_path, usecols=["İl"])
    target = df_rakip.İl.unique()
    fix_dict = decoding_fix_dict(initial, target)
    _df.il = _df.il.replace(fix_dict)
    _df = _df.loc[_df["il"] == city_name]
    df_area = (
        gpd.GeoDataFrame(_df, geometry="geometry")
        .drop(columns=["polygons", "url", "mahalle", "status", "il", "ilce"])
        .rename(columns={"mahalle_key": "key"})
    )
    return df_area


def read_and_convert_mahalle_polygon(raw_data_directory):
    _df = (
        pd.read_excel(raw_data_directory + "TR_mahalle_geodf.xlsx")
        .dropna(subset=["geometry"])
        .query('status == "OK"')
    )
    _df = _df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    _df["polygons"] = _df["polygons"].map(listing)
    _df["geometry"] = _df.apply(
        lambda x: Polygon(x["polygons"]) if isinstance(x["polygons"], list) else np.nan,
        axis=1,
    )
    return _df


def listing(x):
    try:
        if len(ast.literal_eval(x)) > 0:
            result = ast.literal_eval(x)
        else:
            result = ast.literal_eval(x)
        return result
    except Exception as ee:
        print("---", ee)
        return np.nan


def excel_saving(
    sheet_name,
    output_data_directory,
    raw_data_directory,
    city_name,
    wb_1,
    wb_2,
    latest_row,
):
    ws_1 = wb_1[sheet_name]
    ws_2 = wb_2[sheet_name]
    ws_2.title = sheet_name
    ws_2.sheet_format = ws_1.sheet_format
    prev_col = ""

    sample_size = 82
    for (row, col), source_cell in ws_1._cells.items():
        if row == 1 or row == sample_size or row == sample_size - 1:

            if row != 1:
                if row != sample_size:
                    row = latest_row - 1

                else:
                    row = latest_row

            cell = ws_2.cell(column=col, row=row)
            cell.font = copy(source_cell.font)
            cell.fill = copy(source_cell.fill)
            cell.border = copy(source_cell.border)
            cell.alignment = copy(source_cell.alignment)
            cell.comment = source_cell.comment
            if row == latest_row or (
                row == latest_row - 1 and cell.column_letter == "X"
            ):
                if sheet_name == "Rekabet":
                    try:
                        # with two decimal places. Will output 3.14%
                        cell.number_format = FORMAT_PERCENTAGE_00
                    except Exception as ee:
                        pass

        if col != prev_col:
            ws_2.column_dimensions[cell.column_letter].width = ws_1.column_dimensions[
                cell.column_letter
            ].width
        prev_col = col

    first = FormatObject(type="percent", val=0)
    second = FormatObject(type="percent", val=33)
    third = FormatObject(type="percent", val=67)
    iconset = IconSet(
        iconSet="3Arrows",
        cfvo=[first, second, third],
        showValue=None,
        percent=True,
        reverse=None,
    )
    # assign the icon set to a rule

    rule = Rule(type="iconSet", iconSet=iconset)
    # rule = IconSetRule('5Arrows', 'percent', [10, 20, 30, 40, 50], showValue=None, percent=None, reverse=None)
    if sheet_name == "Rekabet":
        ws_2.conditional_formatting.add(f"F{latest_row}:K{latest_row}", rule)

    excel_path = (
        output_data_directory + f"{city_name}/{city_name} " + "Yayilim Modellemesi.xlsx"
    )
    print(excel_path)
    wb_2.save(excel_path)
    print(sheet_name, " saved!")
