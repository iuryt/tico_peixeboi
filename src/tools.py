import numpy as np
import cartopy.crs as ccrs

def plot_scale_bar(ax, length, x0, y0, linewidth=2, orientation=None, transform = ccrs.PlateCarree()):
    """
    Plot a scale bar on the map.

    Inputs:
    ax = the axes to draw the scalebar on
    length = length of the scalebar in km
    x0 = the map x location of the scale bar (in projected coordinates)
    y0 = the map y location of the scale bar (in projected coordinates)

    Keywords:
    linewidth: thickness of the scale bar (default is 3)
    orientation: vertical or horizontal (default is vertical)
    transform: ccrs transform used for the map (default is ccrs.PlateCarree())

    """

    km_per_deg_lat = 111.195 # 1 deg lat = 111.195 km
    km_per_deg_lon = km_per_deg_lat*np.cos(y0*np.pi/180) # 1 deg lon = 111.195*cos(lat) km

    bar_length_deg_lat=length/km_per_deg_lat
    bar_length_deg_lon=length/km_per_deg_lon

    if orientation == 'horizontal':
        x=[x0-bar_length_deg_lon/2, x0+bar_length_deg_lon/2]
        y=[y0, y0]
    else:
        x=[x0, x0]
        y=[y0-bar_length_deg_lat/2, y0+bar_length_deg_lat/2]
    
    ax.plot(x, y, markersize = linewidth*2, marker = "|", transform = transform, color = "0.1", linewidth = linewidth, solid_capstyle='butt')
    ax.text(x0, y0, f"{length} km\n\n", va = "center", fontsize = 8, ha = "center", transform = transform)