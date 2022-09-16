import rasterio
from rasterio import plot as rasterplot
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import requests

def generateMap(date, hours, minutes, utc, mode):
  # color theme
  if(mode == "dark"):
    color = "white"
    bg_color = "black"
  else:
    color = "black"
    bg_color = "white"
  
  # formating time and date
  if (minutes < 10):
    minutes = f"0{minutes}"
  if (utc == 2):
    hours = hours-1

  # time for plot title and path
  utcHours = hours-1
  if (utcHours < 10):
    utcHours = f"0{utcHours}" 
  utcTimeString = f"{utcHours}-{minutes}"
  
  if (hours < 10):
    hours = f"0{hours}" 
  urlDate = f"{date}T{hours}:{minutes}:00.000+01:00"

  # fetching file from waterinfo
  response = requests.get(f"https://hydro.vmm.be/grid/kiwis/KiWIS?datasource=10&service=kisters&type=queryServices&request=getrasterfile&ts_path=COMP_VMM/Vlaanderen_VMM/Ni/5m.Cmd.Raster.O.SRI_1km_cappi&date={urlDate}&format=geotiff")
  open("temp/file.tif", "wb").write(response.content)

  fig, ax = plt.subplots()

  try:
    # opening raster and shapefile
    raster = rasterio.open("temp/file.tif", "r+")
    shapefile = gpd.read_file("shapefile/provinces_L08.shp")

    # transforming and cleaning raster
    array = raster.read(1)
    raster_extent = [360000, 810000, 510000, 910000]
    array[array == 0] = np.nan
    array[array == -2] = np.nan

    # defining colormap for colorbar
    shades = ["#2a35d1", "#2a67d1", "#2a89d1", "#2ac3d1", "#2ad189", "#35d12a", "#c3d12a", "#d1a22a", "#d1702a", "#d1382a", "#d12a7b", "#aa2ad1"]
    bins = [0.1, 0.2, 0.4, 0.8, 1.5, 3.0, 6.5, 13.0, 25.0, 50.0, 100.0, 1000.0]
    cmap = colors.ListedColormap(shades)
    norm = colors.BoundaryNorm(boundaries=bins, ncolors=len(cmap.colors)-1 )

    # plotting data
    shapefile.plot(facecolor="none", edgecolor=color, linewidth=0.5, ax=ax)
    rasterplot.show(array, extent=raster_extent, ax=ax, cmap=cmap, norm = norm)

    # colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ticks=bins)
    cb.set_label("precipitation rate (mm/h)", color=color)
    cb.ax.yaxis.set_tick_params(color=color)
    cb.outline.set_edgecolor(color)
    plt.setp(plt.getp(cb.ax.axes, "yticklabels"), color=color)

    # title and limits
    fig.patch.set_facecolor(bg_color)
    plt.title(f"{date} {utcTimeString}UTC", color=color, loc="left")
    plt.ylim(500000, 775000)
    plt.xlim(500000, 810000)


  except:
    fig.patch.set_facecolor(bg_color)
    plt.title("No Radar Image Available", color=color)

  plt.axis("off")
  plt.tight_layout()

  # save plot
  name = f"{mode}/plot-2022-09-14T{utcTimeString}.png"
  path = f"out/{name}"
  plt.savefig(path, dpi=200, facecolor=bg_color)
  plt.close()

  return [name, path]