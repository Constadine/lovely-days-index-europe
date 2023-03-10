import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from plot_europe import plot_europe
from tools import change_to_datetime

folder = '../data/miroc6/to_use/winter'
f_tasmax = folder+'/tasmax_MIROC6_1980-2010_europe_winter_celc.nc'
f_tas = folder+'/tas_MIROC6_1980-2010_europe_winter_celc.nc'
f_hum = folder+'/humidity_MIROC6_1980-2010_europe_winter.nc'
f_sfcWind = folder+'/sfcWind_MIROC6_1980-2010_europe_winter.nc'


# Load Datasets

ds_tasmax = xr.open_dataset(f_tasmax)
ds_relhum = xr.open_dataset(f_hum)
ds_wind = xr.open_dataset(f_sfcWind)
ds_tas = xr.open_dataset(f_tas)

# change_to_datetime(ds_tasmax, ds_relhum, ds_wind, ds_tas)
"""
For some reason copying the dims,coords, and attrs gave this error:
    TypeError: Invalid value for attr 'time': <xarray.DataArray 'time' (time: 2852)>
    
Leaving it here so I can figure it some other time.
Workaround was to work immediately on top of the pre-existing dataset.
"""
# Copy DS structure
# dims = ds_tasmax.tasmax.dims
# coords = {dim: ds_tasmax[dim] for dim in dims}
# attrs = ds_tasmax.attrs
# var_attrs = {'time':ds_tasmax.tasmax.time,'latitude':ds_tasmax.tasmax.lat,'longitude':ds_tasmax.tasmax.lon}
# var_coords = ['time','lat', 'lon']
# ds_indexes = xr.Dataset(coords=coords, attrs=attrs)


# Summer comfort calculations START----------------------------------------------------------------------------------------
maxtemp_conf = np.where(ds_tasmax.tasmax < 31, 3, -2)
temp_comfort = np.where(ds_tas.tas < 27, 2, 0)

ds1 = ds_tasmax.assign(maxtemp_comfort=xr.where(ds_tasmax.tasmax < 31, 3, -2))

ds2 = ds1.assign(temp_comfort=xr.where(ds_tas.tas < 27, 2, 0))

ds3 = ds2.assign(heatindex_comfort=xr.where((ds_relhum.hurs < 60) & (ds_tasmax.tasmax < 27), 2, -1))

ds4 = ds3.assign(hum_comfort=xr.where(ds_relhum.hurs < 65, 2, 0))

ds5 = ds4.assign(hum_comfort=xr.where((ds_relhum.hurs > 65) & (ds_tas.tas > 27), ds4.hum_comfort-2, ds4.hum_comfort))

ds6 = ds5.assign(wind_comfort=xr.where((ds_wind.sfcWind < 4), 1, 0))

ds7 = ds6.assign(wind_comfort=xr.where(((ds_wind.sfcWind == 0) & (ds_tasmax.tasmax > 25)), ds6.wind_comfort - 2, ds6.wind_comfort))

ds8 = ds7.assign(total_comfort = 10*(ds1.maxtemp_comfort + ds2.temp_comfort + ds3.heatindex_comfort + ds5.hum_comfort + ds6.wind_comfort))
     
ds8 = ds8.drop(['tasmax',
'maxtemp_comfort',
'temp_comfort',
'heatindex_comfort',
'hum_comfort',
'wind_comfort',])          
# vars_to_assign = {'maxtemp_comfort':maxtemp_comfort,
#                   'temp_comfort':temp_comfort,
#                   'heatindex_comfort':hum_comfort,
#                   'wind_comfort':wind_comfort,
#                   'hum_comfort':hum_comfort,
#                   'total_comfort':total_comfort}

# ds_indexes = ds_indexes.assign(vars_to_assign)
# Summer comfort calculations END----------------------------------------------------------------------------------------

# change_to_datetime(ds8)

# plot_europe(ds8, "total_comfort", 'total_comfort', '2000-08-01', 12)

ds8.to_netcdf('../data//miroc6/output/comfort_index_2020-2050_winter.nc')

