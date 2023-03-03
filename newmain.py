import xarray as xr
import matplotlib.pyplot as plt
from plot_europe import plot_europe
from tools import change_to_datetime

f_tastemp = '../data/GFDL-CM4/to_use/tasmax_1980-2010_europe_summer_celc.nc'
f_hum = '../data/GFDL-CM4/to_use/humidity_1980-2010_europe_summer.nc'
f_sfcWind = '../data/GFDL-CM4/to_use/sfcWind_1980-2010_europe_summer.nc'
f_temp = '../data/GFDL-CM4/to_use/tas_1980-2010_europe_summer_celc.nc'

# Load Datasets
ds_tasmax = xr.open_dataset(f_tastemp)
ds_relhum = xr.open_dataset(f_hum)
ds_wind = xr.open_dataset(f_sfcWind)
ds_tas = xr.open_dataset(f_temp)

# change_to_datetime(ds_tasmax, ds_relhum, ds_wind, ds_tas)

# Copy DS structure
dims = ds_tasmax.tasmax.dims
coords = {dim: ds_tasmax[dim] for dim in dims}
attrs = ds_tasmax.attrs
var_attrs = {'time':ds_tasmax.tasmax.time,'latitude':ds_tasmax.tasmax.lat,'longitude':ds_tasmax.tasmax.lon}
var_coords = ['time','lat', 'lon']
ds_indexes = xr.Dataset(coords=coords, attrs=attrs)


# Summer comfort calculations START----------------------------------------------------------------------------------------
maxtemp_comfort = xr.Variable(var_coords,
                      xr.where(ds_tasmax.tasmax < 31, 3, -2), 
                      attrs = var_attrs)
temp_comfort = xr.Variable(var_coords, 
                      xr.where(ds_tas.tas < 27, 2, 0), 
                      attrs = var_attrs)
heatindex_comfort = xr.Variable(var_coords, 
                      xr.where((ds_relhum.hurs < 60) & (ds_tasmax.tasmax < 27), 2, -1), 
                      attrs = var_attrs)
hum_comfort = xr.Variable(var_coords, 
                      xr.where((ds_relhum.hurs < 65), 2, 0), 
                      attrs = var_attrs)
hum_comfort = xr.Variable(var_coords, 
                      xr.where(((ds_relhum.hurs > 65) & (ds_tas.tas > 27)), -2, hum_comfort), 
                      attrs = var_attrs)
wind_comfort = xr.Variable(var_coords, 
                      xr.where((ds_wind.sfcWind < 4), 1, 0), 
                      attrs = var_attrs)
wind_comfort = xr.Variable(var_coords, 
                      xr.where(((ds_wind.sfcWind == 0) & (ds_tasmax.tasmax > 25)), wind_comfort - 2, wind_comfort), 
                      attrs = var_attrs)
total_comfort = xr.Variable(var_coords,
                      10*(maxtemp_comfort + temp_comfort + heatindex_comfort + hum_comfort + wind_comfort), 
                      attrs = var_attrs)

vars_to_assign = {'maxtemp_comfort':maxtemp_comfort,
                  'temp_comfort':temp_comfort,
                  'heatindex_comfort':hum_comfort,
                  'wind_comfort':wind_comfort,
                  'hum_comfort':hum_comfort,
                  'total_comfort':total_comfort}

ds_indexes = ds_tasmax.assign(vars_to_assign)
# Summer comfort calculations END----------------------------------------------------------------------------------------

# change_to_datetime(ds_indexes)

# plot_europe(ds_indexes, "total_comfort", 'total_comfort', '2010-08-01', 12)

ds_indexes.to_netcdf('../data/GFDL-CM4/to_use/comfort_index.nc')

