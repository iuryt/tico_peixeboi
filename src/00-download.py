import os
import xarray as xr
from datetime import datetime, timedelta
import getpass
from tqdm import tqdm
from glob import glob

import motuclient
from earthaccess import Auth, DataCollections, DataGranules, Store


# Class to manage Motu Options as an object
class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None
        

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

# Get user credentials for NEMO data access
USERNAME = input('Enter your username: ')
PASSWORD = getpass.getpass('Enter your password: ')

# Request and download NEMO data for each month (July, August, September)
for mo in tqdm([7,8,9]):
    data_request_options_dict_manual = {
        "service_id": "GLOBAL_ANALYSISFORECAST_PHY_001_024-TDS",
        "product_id": "cmems_mod_glo_phy_anfc_merged-uv_PT1H-i",
        "date_min": f"2022-{mo:02.0f}-01 00:00:00",
        "date_max": f"2022-{mo+1:02.0f}-01 00:00:00",
        "longitude_min": -69.34961519949772,
        "longitude_max": -30.162162074497736,
        "latitude_min": -10.27691380440848,
        "latitude_max": 21.4641223563058,
        "depth_min": 0.49402499198913574,
        "depth_max": 0.49402499198913574,
        "variable": ["utotal","vtotal"],
        "motu": "https://nrt.cmems-du.eu/motu-web/Motu",
        "out_dir": ".",
        "out_name": f"../data/GLORYS/GLOBAL_ANALYSISFORECAST_PHY_001_024-TDS_2022_{mo:02.0f}.nc",
        "auth_mode": "cas",
        "user": USERNAME,
        "pwd": PASSWORD
    }
    motuclient.motu_api.execute_request(MotuOptions(data_request_options_dict_manual))

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
       