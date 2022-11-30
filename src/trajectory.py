import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("../data/planilhaSateliteTicoR4.csv", delimiter=";", parse_dates=["Data"], index_col="Data")
df = df[["Longitude","Latitude"]]
df.index.name = "time"

ds = df.to_xarray()
ds = ds.assign(x = 111.32e3 * np.cos(np.deg2rad(ds.Latitude)),y = 110.574e3 * ds.Latitude)
