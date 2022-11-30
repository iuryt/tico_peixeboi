import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dateparser import parse

# load data
df = pd.read_csv("../data/planilhaSateliteTicoR4.csv", delimiter=";")

# parse timestamps
time = (df["Data"]+" "+df["Hora"]).apply(parse)

# set index
df = df[["Longitude","Latitude"]]
df.index = time
df.index.name = "time"

ds = df.to_xarray()
ds = ds.assign(x = 111.32e3 * np.cos(np.deg2rad(ds.Latitude)) * ds.Longitude,y = 110.574e3 * ds.Latitude)
ds = ds.assign(x = ds.x-ds.x.isel(time=0), y = ds.y-ds.y.isel(time=0))
