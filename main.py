import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from plot_europe import plot_europe
from index_calculation import calculate_comfort_index_summer

f_maxtemp = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/tmax/tasmax_1950-2014_europe_summer_celc.nc'
f_hum = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/hist/humidity_1950-2015_europe_summer.nc'
f_sfcWind = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/sfcWind_1950-2014_europe_summer.nc'
f_temp = '/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/to_use/tas_1950-2014_europe_winter_celc.nc'



ds_tempmax = xr.open_dataset(f_maxtemp)
ds_hum = xr.open_dataset(f_hum)
ds_wind = xr.open_dataset(f_sfcWind)
ds_temp = xr.open_dataset(f_temp)

# ds_tempmax = ds_tempmax.assign(above_thirty=xr.where(ds_tempmax.tasmax > 27, 1, 0))


datetimeindex = ds_tempmax.indexes['time'].to_datetimeindex()
ds_tempmax['time'] = datetimeindex
datetimeindex = ds_hum.indexes['time'].to_datetimeindex()
ds_hum['time'] = datetimeindex

# plot_europe(ds_hum, 'hurs', 'Humidity', '2016-09-01', 12)


# ds_tempmax.to_netcdf('/home/kon/Documents/Sweden/Master/Climate Modeling/Project/data/GFDL-CM4/ideal_vs_hot_areas2.nc')

