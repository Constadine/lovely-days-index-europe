import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from plot_europe import plot_comfort_index
from tools import change_to_datetime
import metpy.calc as mpcalc
from  metpy.units import units 

P1 = ''
MODELS = ['GFDL-CM4', 'MIROC6']
PERIODS = ['1950-2010', '2040-2100']
PERIODNAMES = ['historical', 'future']
INTERVALS = ['daily', 'monthly']
AREAS = ['north', 'south']
MODEL, PERIOD, PERIODNAME, INTERVAL, AREA = MODELS[1], PERIODS[1], PERIODNAMES[1], INTERVALS[0], AREAS[0]

folder = f'../data/{MODEL}/to_use/long/winter/{AREA}/'

f_hum = folder+f'/humidity_{MODEL}_{PERIOD}_europe_winter_{AREA}{P1}.nc'
f_sfcWind = folder+f'/sfcWind_{MODEL}_{PERIOD}_europe_winter_{AREA}{P1}.nc'
f_tasmax = folder+f'/tasmax_{MODEL}_{PERIOD}_europe_winter_celc_{AREA}{P1}.nc'
f_tas = folder+f'/tas_{MODEL}_{PERIOD}_europe_winter_celc_{AREA}{P1}.nc'

# Load Datasets

ds_tasmax = xr.open_dataset(f_tasmax)
ds_relhum = xr.open_dataset(f_hum)
ds_wind = xr.open_dataset(f_sfcWind)
ds_tas = xr.open_dataset(f_tas)

"""
For some reason copying the dims,coords, and attrs gave this error:
    TypeError: Invalid value for attr 'time': <xarray.DataArray 'time' (time: 2852)>
    
Leaving it here so I can figure it some other time.
Workaround was to work immediately on top of the pre-existing dataset.


!!! 
This also made the datasets 2D instead of Geo 2D, so I couldn't plot with panoply. 
Using this very inefficient way for now....

!!!!!! I think I fixed it by ditching the var_attrs... Why though.
"""
# Copy DS structure
dims = ds_tasmax.tasmax.dims
coords = {dim: ds_tasmax[dim] for dim in dims}
attrs = ds_tasmax.attrs
var_coords = ['time','lat', 'lon']
meantemp = ds_tas.tas.values
relhum = ds_relhum.hurs.values
# HI = -8.7847 + 1.6114 * meantemp - 0.012308 * meantemp**2 + relhum * (2.3385 - 0.14612 * meantemp + 2.2117 * 10**-3 * meantemp**2) + relhum**2 * (-0.016425 + 7.2546 * 10**-4 * meantemp - 3.582 * 10**-6 * meantemp**2)
ds = xr.Dataset(coords=coords, attrs=attrs)

# Winter comfort calculations START----------------------------------------------------------------------------------------

# Max temperature --------
total_comfort = xr.where((ds_tasmax.tasmax < 23) & (ds_tasmax.tasmax > 11), 2, 0)
total_comfort = xr.where(ds_tasmax.tasmax < 21, total_comfort-1, total_comfort)

# Mean temperature --------
total_comfort = xr.where((ds_tas.tas > 13) & (ds_tas.tas < 20), total_comfort+1, total_comfort)

# Heat index --------
AT = mpcalc.apparent_temperature(ds_tasmax.tasmax.values * units.degC,
                                 ds_relhum.hurs.values*units.percent,
                                 ds_wind.sfcWind.values*units('m/s'),
                                 mask_undefined=False).magnitude
total_comfort = xr.where((AT > 13) & (AT < 20), total_comfort+5, total_comfort-1)
total_comfort = xr.where(AT < 12, total_comfort-2, total_comfort)


# Relative humidity --------
total_comfort = xr.where((ds_relhum.hurs > 30) & (ds_relhum.hurs < 40), total_comfort+2, total_comfort)
total_comfort = xr.where((ds_relhum.hurs > 65) & (ds_tas.tas < 13), total_comfort-1, total_comfort)

# Wind speed --------
total_comfort = xr.where((ds_wind.sfcWind > 0.5), total_comfort-1, total_comfort)
total_comfort = xr.where(((ds_wind.sfcWind > 4) & (ds_tasmax.tasmax < 10)), total_comfort-2, total_comfort)

# Total --------
total_comfort = xr.Variable(var_coords, 
                      10*total_comfort)


AT = xr.Variable(var_coords, AT)
dsat = xr.Dataset(coords=coords, attrs=attrs)

dsat['AT'] = AT
ds['total_comfort'] = total_comfort     
# Winter comfort calculations END----------------------------------------------------------------------------------------


# change_to_datetime(ds)

# plot_comfort_index(ds, "total_comfort", 'CI', '1999-01-10', 12)

ds.to_netcdf(f'../data/{MODEL}/output/from_{INTERVAL}_data_v2/{AREA}/{INTERVAL}_CI_{MODEL}_{PERIODNAME}_winter{AREA}.nc')

