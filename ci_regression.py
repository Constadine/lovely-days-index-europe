import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

P1 = ''
MODELS = ['GFDL-CM4', 'MIROC6']
PERIODS = ['1950-2010', '2040-2100']
PERIODNAMES = ['historical', 'future']
INTERVALS = ['daily', 'monthly']
AREAS = ['north', 'south']
SEASONS = ['summer', 'winter']
MODEL, PERIOD, PERIODNAME, INTERVAL, AREA, SEASON = MODELS[0], PERIODS[1], PERIODNAMES[1], INTERVALS[0], AREAS[1], SEASONS[0]
folder1 = f'../graphs/data/{MODELS[0]}/{AREAS[0]}/fldmeans/seasmeans'
folder2 = f'../graphs/data/{MODELS[0]}/{AREAS[1]}/fldmeans/seasmeans'

north_future_summer = xr.open_dataset(folder1+f'/daily_CI_GFDL-CM4_future_{SEASON}{AREAS[0]}_fldmean_seasmean.nc')
south_future_summer = xr.open_dataset(folder2+f'/daily_CI_GFDL-CM4_future_{SEASON}{AREAS[1]}_fldmean_seasmean.nc')

north_future_summer_ci = north_future_summer['total_comfort'].mean(dim=('lat', 'lon'))
north_future_summer_years = north_future_summer['time.year']
south_future_summer_ci = south_future_summer['total_comfort'].mean(dim=('lat', 'lon'))
south_future_summer_years = south_future_summer['time.year']

# Create a figure with 1 row and 1 column
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(north_future_summer_years, north_future_summer_ci, label=f'{MODEL} {AREAS[0].capitalize()} {SEASON.capitalize()} {PERIODNAME}', color='blue')
ax.plot(south_future_summer_years, south_future_summer_ci, label=f'{MODEL} {AREAS[1].capitalize()} {SEASON.capitalize()} {PERIODNAME}', color='red')

# Add a regression line
z1 = np.polyfit(north_future_summer_years, north_future_summer_ci, 1)
p1 = np.poly1d(z1)
ax.plot(north_future_summer_years, p1(north_future_summer_years), "b--", label=f'Regression line: {AREAS[0].capitalize()}')

z2 = np.polyfit(south_future_summer_years, south_future_summer_ci, 1)
p2 = np.poly1d(z2)
ax.plot(south_future_summer_years, p2(south_future_summer_years), "r--", label=f'Regression line: {AREAS[1].capitalize()}')

# Set the title, x-axis label, and y-axis label
ax.set_title(f'{SEASON.capitalize()} Mean Comfort Index in Europe (SSPS 8.5)')
ax.set_xlabel('Year')
ax.set_ylabel('Comfort Index')

ax.legend()
# plt.savefig('winter_mean_ci.png', dpi=200)

plt.show()