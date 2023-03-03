"""
Everything was wrong. Move on.
"""


import numpy as np
import xarray as xr
import pandas as pd
import metpy.calc as mpcalc
from  metpy.units import units 
import matplotlib.pyplot as plt
from plot_europe import plot_europe
from tools import change_to_datetime
from index_calculation import calculate_comfort_index_summer

f_tastemp = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/tasmax_1980-2010_europe_summer_celc.nc'
f_hum = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/humidity_1980-2010_europe_summer.nc'
f_sfcWind = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/sfcWind_1980-2010_europe_summer.nc'
f_temp = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/tas_1980-2010_europe_summer_celc.nc'


ds_tasmax = xr.open_dataset(f_tastemp)
ds_relhum = xr.open_dataset(f_hum)
ds_wind = xr.open_dataset(f_sfcWind)
ds_tas = xr.open_dataset(f_temp)

# ds_tempmax = ds_tempmax.assign(above_thirty=xr.where(ds_tempmax.tasmax > 27, 1, 0))

change_to_datetime(ds_tasmax, ds_relhum, ds_wind, ds_tas)

# plot_europe(ds_relhum, 'hurs', 'Humidity', '2016-09-01', 12)


# ds_tempmax.to_netcdf('/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/ideal_vs_hot_areas2.nc')


# index_points = []
# for i in range(ds_tasmax.shape[0]):
#     for j in range(len(ds_tasmax.lat)):
#         for z in range(len(ds_tasmax.lon)):
#             lovely_day_index = calculate_comfort_index_summer(ds_tasmax.tasmax[i][j][z].values,
#                                                               ds_tas.tas[i][j][z].values,
#                                                               ds_relhum.hurs[i][j][z].values,
#                                                               ds_wind.sfcWind[i][j][z].values)
#             index_points.append(lovely_day_index)

# index_points = np.array(index_points)
# print(index_points)

# tasmax = ds_tasmax.tasmax.values
# rel_hum = ds_relhum.hurs.values
# sfc_wind = ds_wind.sfcWind.values
# tas = ds_tas.tas.values

"""
Basically what I want is to create a data array or dataset that contains the 
lovely_day_index. So I need to apply the 'calculate_comfort_index_summer' 
function using thevalues from these four datasets above.
I need to keep the coordinates so I can plot afterwards as well.
"""

# ds_comfort_index = xr.Dataset(coords=ds_relhum.coords, attrs=ds_relhum.attrs)


# index_points_ds['comfort_index'] = index_points_ds.assign({"comfort_index": lambda row: [calculate_comfort_index_summer(tasmax[row], tas[row], rel_hum[row], sfc_wind[row]])})
# pleasant_index_values = calculate_comfort_index_summer(tasmax, tas, rel_hum, sfc_wind)


# ------------------------------------- Dad approach

# dims = ds_tasmax.tasmax.dims
# coords = {dim: ds_tasmax[dim] for dim in dims}
# attrs = ds_tasmax.attrs

# ds_comfort_index = xr.Dataset(coords=coords, attrs=attrs)

# # Add a new variable for the comfort index with the same dimensions and coordinates
# ds_comfort_index['comfort_index'] = xr.DataArray(np.zeros(ds_tasmax.tasmax.shape), dims=dims, coords=coords)

# vfunc = np.vectorize(calculate_comfort_index_summer)

# tasmax_values = ds_tasmax.tasmax.values
# tas_values = ds_tas.tas.values
# rel_hum_values = ds_relhum.hurs.values
# sfc_wind_values = ds_wind.sfcWind.values

# # Create an iterator to loop through all the values
# it = np.nditer([tasmax_values, tas_values, rel_hum_values, sfc_wind_values],
#                 flags=['multi_index'])

# while not it.finished:
#     tasmax_val = it[0]
#     tas_val = it[1]
#     rel_hum_val = it[2]
#     sfc_wind_val = it[3]
    
#     comfort_index_val = vfunc(tasmax_val, tas_val, rel_hum_val, sfc_wind_val)
#     print(comfort_index_val)
#     # Assign the computed value to a new variable or modify the original variable
#     # For example:
#     ds_comfort_index.comfort_index[it.multi_index] = comfort_index_val
    
#     # Move to the next value
#     it.iternext()
    
# ds_comfort_index.to_netcdf('/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/indexes.nc')

# ----------------------------------------------------------

# Calculate HEAT INDEX
# -----------------------------------------------------------


# dims = ds_tas.tas.dims
# coords = {dim: ds_tas[dim] for dim in dims}
# attrs = ds_tasmax.attrs

# # Create the new empty Dataset
# ds_heat_index = xr.Dataset(coords=coords, attrs=attrs)

# # Add a new variable for the comfort index with the same dimensions and coordinates
# ds_heat_index['heat_index'] = xr.DataArray(np.zeros(ds_tas.tas.shape), dims=dims, coords=coords)

# heat_index_vals = mpcalc.heat_index(ds_tas.tas.values * units.degC, ds_relhum.hurs.values * units.percent,mask_undefined=False)


# heat_index = xr.Variable(['time','latitude', 'longitude'], 
#                        heat_index_vals, attrs= {'time':ds_tas.tas.time,'latitude':ds_tas.tas.lat,'longitude':ds_tas.tas.lon})

# ds_heat_index = ds_heat_index.assign({'heat_index': heat_index_vals})


# new_var= xr.Variable(['latitude', 'longitude'], 
#                      temp_mean, attrs= {'latitude':ds_temp.tas.lat,'longitude':ds_temp.tas.lon})

# index_points_ds = index_points_ds.assign({'tasmean': new_var})