import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import matplotlib.pyplot as plt

def plot_europe(ds, variable:str, label:str, date:str, time_step:int):

    if label=="Temperature":
        unit = '°C'
    elif label == "Humidity":
        unit = '%'
    elif label == 'Surface Wind Speed':
        unit = 'm/s'
    else:
        unit = ""
    # Set the date and time step to plot
    date = pd.Timestamp(date)
    time_step = time_step  # 12:00 hours
    
    # Extract the temperature data for the given date and time 
    
    ds_sel = ds.sel(time=date+pd.to_timedelta(time_step, unit='h'), method='nearest')
    
    
    # Set up the plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # Add map features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    
    # Set the map extent to Europe
    ax.set_extent([-25, 40, 34, 73], crs=ccrs.PlateCarree())
    
    # Plot the temperature data
    im = ax.pcolormesh(ds_sel.lon, ds_sel.lat, eval("ds_sel."+f"{variable}"), cmap='RdYlBu_r', transform=ccrs.PlateCarree())
    
    # Add a colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', shrink=0.8)
    cbar.set_label(f'{label} {unit}')
    
    # Add a title
    plt.title(f'{label} in Europe on {ds_sel.time.values.astype("datetime64[D]")}')
    
    # Show the plot
    plt.show()