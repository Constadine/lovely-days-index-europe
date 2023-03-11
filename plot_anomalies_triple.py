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
PERIOD, PERIODNAME, INTERVAL, AREA, SEASON = PERIODS[0], PERIODNAMES[0], INTERVALS[0], AREAS[1], SEASONS[0]

file_names = [F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/GFDL-CM4/{SEASON}/CI_mean_GFDL-CM4_historical_{SEASON}.nc',
              F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/GFDL-CM4/{SEASON}/CI_mean_GFDL-CM4_future_{SEASON}.nc',
              F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/GFDL-CM4//{SEASON}/CI_anomaly_GFDL-CM4_{SEASON}.nc',
              F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/MIROC6/{SEASON}/CI_mean_MIROC6_historical_{SEASON}.nc',
              F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/MIROC6/{SEASON}/CI_mean_MIROC6_future_{SEASON}.nc',
              F'/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/MIROC6/{SEASON}/CI_anomaly_MIROC6_{SEASON}.nc']

countries = cfeature.NaturalEarthFeature(category='cultural',
                                         name='admin_0_countries',
                                         scale='50m',
                                         facecolor='none')
seasons = ['Historical', 'SSP5 8.5', 'Comfort Index Anomaly'] * 2
models = ['GFDL-CM4', 'MIROC6']

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
family='serif'

# Set the distance between subplots
fig.subplots_adjust(wspace=0.1, hspace=0.3)

# Loop over the files and plot the data
for i, file_name in enumerate(file_names):
    ds = xr.open_dataset(file_name, engine='netcdf4')
    data = ds["total_comfort"].isel(time=0)
    lats = data.lat.values
    lons = data.lon.values
    img = axs[i//3, i%3].pcolormesh(lons, lats, data.values,
                                    cmap='RdYlGn',
                                    norm = mtlb.colors.TwoSlopeNorm(0),
                                    shading='gouraud',
                                    transform=ccrs.PlateCarree())
    axs[i//3, i%3].set_title(f'{seasons[i]}',family=family)
    axs[i//3, i%3].coastlines()

    countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='50m',
        facecolor='none')
    axs[i//3, i%3].add_feature(countries, edgecolor='black', linewidth=0.5)
    
    # Add minimum and maximum prec labels
    min_prec = round(float(data.min()), 1)
    max_prec = round(float(data.max()), 1)
    axs[i//3, i%3].text(0.02, -0.12, f'Min: {min_prec}, Max: {max_prec}', transform=axs[i//3, i%3].transAxes,
                fontsize=10,
                family=family)
fig.text(0.51, 0.9, f'{models[0]}', ha='center', family=family)
fig.text(0.51, 0.502, f'{models[1]}', ha='center', family=family)    
        
cbar = fig.colorbar(img, ax=axs, orientation='horizontal', fraction=0.05, pad=0.06,)
cbar.ax.set_xscale('linear')

cbar.set_label('Comfort Index',family=family)

fig.suptitle(f'{SEASON.capitalize()} Comfort Index Anomaly for the period 2040-2100 against 1950-2010 seasonal mean',
             family=family)

plt.savefig(f'../graphs/{SEASON}/comfort_anomaly_{SEASON}_2models.png', dpi=200)

plt.show()
