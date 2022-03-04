# encoding: windows-1254

import os
import pandas as pd
import unidecode


df = pd.read_excel('../data/raw/Rakip&Vestel Bilgileri_20211210.xlsx')
drop_cities = os.listdir('../reports/cities')

# ----- Slicing ------
# latest_il = "Kilis"
# df = df.drop_duplicates(subset=["?l"]).set_index("?l").loc[latest_il:].reset_index()
# --------------------

ls = df['İl'].unique().tolist()
for ind, city in enumerate(ls):
    print(f"{ind + 1} / {len(ls)}")
    os.system(f'python main.py {city}')