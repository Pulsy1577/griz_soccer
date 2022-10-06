import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
from os.path import join as pjoin
from gspread_pandas import Spread, Client

import acwr_calc

BASE_DIR = Path(__file__).resolve().parent.parent

spread = Spread("Griz Soccer Analytics")
spt_data = spread.sheet_to_df(index=0, header_rows=1, sheet="SPT FULL")
print(spt_data.columns)
base_df = pd.read_csv(pjoin(BASE_DIR, "test_data", "base_col.csv"))
base_df["Zone_5_Distance"] = base_df["Zone_5_Distance"].astype(float)

# TODO fix the columns so that the types can be copied over
spt_data = spt_data.astype(base_df.dtypes.to_dict())

fixed_data = acwr_calc.get_data(spt_data)

conn = sqlite3.connect(pjoin(str(BASE_DIR), "db.sqlite3"))
c = conn.cursor()

create_query = "CREATE TABLE IF NOT EXISTS sdata (Date text ,Name text,Performance_Duration number,Total_Distance number,Walk_Distance number,Jog_Distance number,Run_Distance number,Sprint_Distance number,Sprint_Efforts number,Zone_1_Distance number,Zone_2_Distance number,Zone_3_Distance  number,Zone_4_Distance  number,Zone_5_Distance  number,Zone_6_Distance  number,Zone_7_Distance  number,Zone_8_Distance number,Hard_Running number,Hard_Running_Efforts number,Work_Rate number,Top_Speed number,Intensity number,Impact_Light number,Impact_Medium number,Impact_Heavy number,Load_2D number,Load_3D number,L1 number,L2 number,L1_aewma number,L1_cewma number,L2_aewma number,L2_cewma number,aEWMAspt number,cEWMAspt number,acwr_spt number,acwr_l1 number,acwr_l2 number,ACWR_AVG number)"
c.execute(create_query)
conn.commit()

fixed_data.to_sql("sdata", conn, if_exists="replace", index=False)

conn.commit()
conn.close()
