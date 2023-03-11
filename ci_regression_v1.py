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
MODEL, PERIOD, PERIODNAME, INTERVAL, AREA, SEASON = MODELS[0], PERIODS[1], PERIODNAMES[1], INTERVALS[0], AREAS[1], SEASONS[1]
folder1 = f'../graphs/data/{MODELS[0]}/{AREAS[0]}/fldmeans/seasmeans'
folder2 = f'../graphs/data/{MODELS[0]}/{AREAS[1]}/fldmeans/seasmeans'

north_future_winter = xr.open_dataset(folder1+f'/daily_CI_{MODEL}_{PERIODNAME}_{SEASON}{AREAS[0]}_fldmean_seasmean.nc')
south_future_winter = xr.open_dataset(folder2+f'/daily_CI_{MODEL}_{PERIODNAME}_{SEASON}{AREAS[1]}_fldmean_seasmean.nc')

north_future_winter_ci = north_future_winter['total_comfort'].mean(dim=('lat', 'lon'))
north_future_winter_years = north_future_winter['time.year']
south_future_winter_ci = south_future_winter['total_comfort'].mean(dim=('lat', 'lon'))
south_future_winter_years = south_future_winter['time.year']

# Create a figure with 1 row and 1 column
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(north_future_winter_years, north_future_winter_ci, label=f'{MODEL} {AREAS[0].capitalize()} Europe', color='blue')
ax.plot(south_future_winter_years, south_future_winter_ci, label=f'{MODEL} {AREAS[1].capitalize()} Europe', color='red')

# Add a regression line
z1 = np.polyfit(north_future_winter_years, north_future_winter_ci, 1)
p1 = np.poly1d(z1)
ax.plot(north_future_winter_years, p1(north_future_winter_years), "b--", label=f'Regression line: {AREAS[0].capitalize()}')

z2 = np.polyfit(south_future_winter_years, south_future_winter_ci, 1)
p2 = np.poly1d(z2)
ax.plot(south_future_winter_years, p2(south_future_winter_years), "r--", label=f'Regression line: {AREAS[1].capitalize()}')

# Set the title, x-axis label, and y-axis label
ax.set_title(f'{SEASON.capitalize()} Mean Comfort Index in South and North Europe (SSPS 8.5)')
ax.set_xlabel('Year')
ax.set_ylabel('Comfort Index')

ax.legend()
# plt.savefig('../graphs//winter/winter_mean_ci_SvsN_future.png', dpi=200)

plt.show()