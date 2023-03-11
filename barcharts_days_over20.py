import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# Define the file paths for each model, season, and period
folder = '/home/kon/Documents/Sweden/Master/Climate_Modeling/Project/graphs/data/mean_both_models/days20/timmeans/'
file_paths = {
    'GFDL-CM4_summer_historical': folder+'daily_CI_GFDL-CM4_historical_summer_timmean.nc',
    'GFDL-CM4_summer_future': folder+'daily_CI_GFDL-CM4_future_summer_timmean.nc',
    'GFDL-CM4_winter_historical': folder+'daily_CI_GFDL-CM4_historical_winter_timmean.nc',
    'GFDL-CM4_winter_future': folder+'daily_CI_GFDL-CM4_future_winter_timmean.nc',
    'MIROC6_summer_historical': folder+'daily_CI_MIROC6_historical_summer_timmean.nc',
    'MIROC6_summer_future': folder+'daily_CI_MIROC6_future_summer_timmean.nc',
    'MIROC6_winter_historical': folder+'daily_CI_MIROC6_historical_winter_timmean.nc',
    'MIROC6_winter_future': folder+'daily_CI_MIROC6_future_winter_timmean.nc'
}

x = np.arange(2)  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
mean_values = {}

fig, ax = plt.subplots(layout='constrained')

for key, file_path in file_paths.items():
    ds = xr.open_dataset(file_path)
    model, season, period = key.split('_')
    mean_val = np.mean(ds['total_comfort'].values) # compute the mean of the array
    mean_values[key] = mean_val
    offset = width * multiplier
    multiplier += 1
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    
    
# Create a bar chart to visualize the mean values
fig, ax = plt.subplots(figsize=(8, 6))
x_pos = np.arange(len(mean_values))
ax.bar(x_pos, list(mean_values.values()), align='center')
ax.set_xticklabels(list(mean_values.keys()), rotation=45, ha='right')
plt.show()


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Mean days where Comfort Index > 20')
ax.set_title('Total Comfort for GFDL-CM4 and MIROC6 Models')
ax.set_xticks(x_pos)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 250)

plt.show()