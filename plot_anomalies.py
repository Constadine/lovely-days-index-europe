import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mtlb

file_names = ['/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/CI_anomaly_GFDL_summer.nc',
              '/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/CI_anomaly_MIROC_summer.nc']

countries = cfeature.NaturalEarthFeature(category='cultural',
                                         name='admin_0_countries',
                                         scale='50m',
                                         facecolor='none')
seasons = ['Summer'] * 2
models = ['GFDL-CM4', 'MIROC6']

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
family='serif'
# Set the distance between subplots
fig.subplots_adjust(wspace=0.1, hspace=0.2)

# Loop over the files and plot the data
for i, file_name in enumerate(file_names):
    ds = xr.open_dataset(file_name)
    data = ds["total_comfort"].isel(time=0)
    lats = data.lat.values
    lons = data.lon.values
    img = axs[i].pcolormesh(lons, lats, data.values,
                                    cmap='RdYlGn',
                                    norm = mtlb.colors.TwoSlopeNorm(0),
                                    shading='gouraud',
                                    transform=ccrs.PlateCarree())
    axs[i].set_title(f'{models[i]}',family=family)
    axs[i].coastlines()

    axs[i].add_feature(countries, edgecolor='black', linewidth=0.5)
    # Add minimum and maximum prec labels
    min_prec = round(float(data.min()), 1)
    max_prec = round(float(data.max()), 1)
    axs[i].text(0.01, -0.07, f'Min: {min_prec}, Max: {max_prec}', transform=axs[i].transAxes,
                fontsize=10,
                family=family)
    
cbar = fig.colorbar(img, ax=axs, orientation='horizontal', fraction=0.05, pad=0.06,)
cbar.ax.set_xscale('linear')

cbar.set_label('Comfort Index Anomaly',family=family)

fig.suptitle('Summer Comfort Index Anomaly for the period 2040-2100 against 1950-2010 mean',
             family=family)
# plt.savefig('comfort_anomaly_2models.png', dpi=200)
plt.show()