import os
import xarray as xr
from datetime import datetime, timedelta
import getpass
from tqdm import tqdm
from glob import glob


from earthaccess import Auth, DataCollections, DataGranules, Store

import copernicusmarine

# this file is in .gitignore
# it basically has a dictionary like this
# credentials = dict(username = "username", password = "password")
from copernicus_credentials import credentials

from earthaccess import Auth, DataCollections, DataGranules, Store




# OSCAR Data Download
oscar_output_dir = "../data/OSCAR_L4_OC_NRT_V2.0"
os.makedirs(oscar_output_dir, exist_ok=True)
os.system(f"podaac-data-downloader -c OSCAR_L4_OC_NRT_V2.0 -d {oscar_output_dir} --start-date 2022-07-06T00:00:00Z --end-date 2022-09-05T00:00:00Z")

# HYCOM Data Processing

# HYCOM dataset URL
url = "https://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0/uv3z"

# Function to adjust longitude from 0-360 to -180 to 180
lon360to180 = lambda lon: (((lon + 180) % 360) - 180)

# Open dataset and adjust times and longitudes
ds = xr.open_dataset(url, decode_times=False)
ds = ds.assign(lon=lon360to180(ds.lon)).sortby("lon")
time = [datetime(2000,1,1) + timedelta(hours=ti) for ti in ds.time.values]
ds = ds.assign(time=time)

# Select relevant data dimensions and variables
ds = ds.sel(depth=0, lon=slice(-70,-30), lat=slice(-10,21), time=slice("2022-07-01","2022-10-01"))[["water_u","water_v"]]

# Save to a netCDF file
ds.to_netcdf("../data/HYCOM/GLBy008expt_93.nc")


# NEMO Data Processing

copernicusmarine.subset(
    dataset_id = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m",
    variables = ["thetao","so","uo","vo"],
    minimum_longitude = -69.34,
    maximum_longitude = -30.16,
    minimum_latitude = -10.27,
    maximum_latitude = 21.46,
    start_datetime = "2022-07-01T00:00:00",
    end_datetime = "2022-10-01T00:00:00",
    minimum_depth = 0,
    maximum_depth = 0.5,
    output_filename = "GLORYS.nc",
    output_directory = "../data/GLORYS",
    no_metadata_cache = True,
    overwrite_output_data = True,
    force_download = True,
    **credentials
)    

# SMAP Data Processing

# Initialize and attempt login
auth = Auth()
auth.login(strategy="environment")
# If the first strategy fails, try using the 'netrc' strategy
if not auth.authenticated:
    auth.login(strategy="netrc")

# Search for SMAP data using the earthaccess module
results = earthaccess.search_data(
    short_name = "SMAP_JPL_L3_SSS_CAP_8DAY-RUNNINGMEAN_V5",
    cloud_hosted = True, 
    bounding_box = (-65.5,-30,-5.5,15),
    temporal = ("2022-06", "2022-10-15"),
    count = 200
)

# Download SMAP data files
store = Store(auth)
files = store.get(results, "../data/SMAP/")

# IMERG Data Processing

# Search for IMERG data using the earthaccess module
results = earthaccess.search_data(
    short_name = "GPM_3IMERGDL",
    cloud_hosted = True, 
    bounding_box = (-65.5,-30,-5.5,15),
    temporal = ("2022-06", "2022-10-15"),
    count=200
)

# Check how many files are already present and download if more are available
nfiles = len(glob("../data/IMERG/*"))
print(f"{nfiles} files and {len(results)-nfiles} to be downloaded")
if len(results) > nfiles:
    store = Store(auth)
    files = store.get(results, "../data/IMERG/")
       