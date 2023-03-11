import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mtlb


P1 = ''
MODELS = ['GFDL-CM4', 'MIROC6']
PERIODS = ['1950-2010', '2040-2100']
PERIODNAMES = ['historical', 'future']
INTERVALS = ['daily', 'monthly']
AREAS = ['north', 'south']
SEASONS = ['summer', 'winter']
MODEL1, MODEL2 = MODELS[0], MODELS[1] # Assign the model you want to plot to the variable
PERIOD, PERIODNAME, INTERVAL, AREA, SEASON = PERIODS[0], PERIODNAMES[0], INTERVALS[0], AREAS[1], SEASONS[1]
folder = F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/mean_both_models/days20/timmeans/'

file_names = [folder+F'daily_CI_GFDL-CM4_historical_{SEASON}_timmean.nc',
              folder+F'daily_CI_GFDL-CM4_future_{SEASON}_timmean.nc',
              folder+F'daily_CI_MIROC6_historical_{SEASON}_timmean.nc',
              folder+F'daily_CI_MIROC6_future_{SEASON}_timmean.nc']

countries = cfeature.NaturalEarthFeature(category='cultural',
                                         name='admin_0_countries',
                                         scale='50m',
                                         facecolor='none')

seasons = ['Historical', 'SSP 8.5'] * 2
models = ['GFDL-CM4', 'MIROC6']

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
family='serif'

# Set the distance between subplots
fig.subplots_adjust(wspace=0.1, hspace=0.3)

# Loop over the files and plot the data
for i, file_name in enumerate(file_names):
    ds = xr.open_dataset(file_name, engine='netcdf4')
    data = ds["total_comfort"].isel(time=0)
    lats = data.lat.values
    lons = data.lon.values
    img = axs[i//2, i%2].pcolormesh(lons, lats, data.values,
                                    cmap='YlGn',
                                    
                                    # norm = mtlb.colors.TwoSlopeNorm(0),
                                    shading='gouraud',
                                    transform=ccrs.PlateCarree())
    axs[i//2, i%2].set_title(f'{seasons[i]}',family=family)
    axs[i//2, i%2].coastlines()

    countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='50m',
        facecolor='none')
    axs[i//2, i%2].add_feature(countries, edgecolor='black', linewidth=0.5)
    
    # Add minimum and maximum prec labels
    min_prec = round(float(data.min()), 1)
    max_prec = round(float(data.max()), 1)
    axs[i//2, i%2].text(0.02, -0.12, f'Max: {max_prec}', transform=axs[i//2, i%2].transAxes,
                fontsize=10,
                family=family)
fig.text(0.51, 0.9, f'{models[0]}', ha='center', family=family)
fig.text(0.51, 0.502, f'{models[1]}', ha='center', family=family)    
        
cbar = fig.colorbar(img, ax=axs, orientation='horizontal', fraction=0.05, pad=0.06,)
cbar.ax.set_xscale('linear')

cbar.set_label('Days > 20 CI',family=family)

fig.suptitle(f'{SEASON.capitalize()} Number of days over 20 Comfort Index for the period 2040-2100 against 1950-2010 mean',
             family=family)

plt.savefig(f'../graphs/{SEASON}/days_over_20.png', dpi=200)

plt.show()
