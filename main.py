import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from plot_europe import plot_europe
from tools import change_to_datetime
from index_calculation import calculate_comfort_index_summer

f_tastemp = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/tasmax_1980-2010_europe_summer_celc.nc'
f_hum = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/humidity_1980-2010_europe_summer.nc'
f_sfcWind = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/sfcWind_1980-2010_europe_summer.nc'
f_temp = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/tas_1980-2010_europe_summer_celc.nc'


ds_tasmax = xr.open_dataset(f_tastemp)
ds_hum = xr.open_dataset(f_hum)
ds_wind = xr.open_dataset(f_sfcWind)
ds_tas = xr.open_dataset(f_temp)

# ds_tempmax = ds_tempmax.assign(above_thirty=xr.where(ds_tempmax.tasmax > 27, 1, 0))

change_to_datetime(ds_tasmax, ds_hum, ds_wind, ds_tas)

# plot_europe(ds_hum, 'hurs', 'Humidity', '2016-09-01', 12)

# ds_tempmax.to_netcdf('/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/ideal_vs_hot_areas2.nc')
# index_points = []
# for i in range(2):
#     for j in range(len(ds_tasmax.lat)):
#         for z in range(len(ds_tasmax.lon)):
#             lovely_day_index = calculate_comfort_index_summer(ds_tasmax.tasmax[i][j][z].values,
#                                                               ds_tas.tas[i][j][z].values,
#                                                               ds_hum.hurs[i][j][z].values,
#                                                               ds_wind.sfcWind[i][j][z].values)
#             index_points.append(lovely_day_index)

# index_points = np.array(index_points)
# print(index_points)

tasmax = ds_tasmax.tasmax.values
rel_hum = ds_hum.hurs.values
sfc_wind = ds_wind.sfcWind.values
tas = ds_tas.tas.values

"""
Basically what I want is to create a data array or dataset that contains the 
lovely_day_index. So I need to apply the 'calculate_comfort_index_summer' 
function using thevalues from these four datasets above.
I need to keep the coordinates so I can plot afterwards as well.
"""

index_points_ds = xr.Dataset(coords=ds_hum.coords, attrs=ds_hum.attrs)
# This is roughly how I imagined it but feel free to bully me. I don't care if you manage to salvage my soul.
index_points_ds = index_points_ds.assign(lovely_day_index = index_points_ds.where(
    lambda row: calculate_comfort_index_summer(row[tasmax], row[tas], row[rel_hum], row[sfc_wind])))

# new_var= xr.Variable(['latitude', 'longitude'], 
#                      temp_mean, attrs= {'latitude':ds_temp.tas.lat,'longitude':ds_temp.tas.lon})

# index_points_ds = index_points_ds.assign({'tasmean': new_var})