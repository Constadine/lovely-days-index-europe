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
MODEL1, MODEL2 = MODELS[0], MODELS[1] # Assign the model you want to plot to the variable
PERIOD, PERIODNAME, INTERVAL, AREA, SEASON = PERIODS[1], PERIODNAMES[1], INTERVALS[0], AREAS[1], SEASONS[1]
folder1 = f'../graphs/data/{MODEL1}/{AREAS[0]}/fldmeans/seasmeans'
folder2 = f'../graphs/data/{MODEL1}/{AREAS[1]}/fldmeans/seasmeans'

north_future_winter1 = xr.open_dataset(folder1+f'/daily_CI_{MODEL1}_future_{SEASON}{AREAS[0]}_fldmean_seasmean.nc')
south_future_winter1 = xr.open_dataset(folder2+f'/daily_CI_{MODEL1}_future_{SEASON}{AREAS[1]}_fldmean_seasmean.nc')

north_future_winter_ci1 = north_future_winter1['total_comfort'].mean(dim=('lat', 'lon'))
north_future_winter_years1 = north_future_winter1['time.year']
south_future_winter_ci1 = south_future_winter1['total_comfort'].mean(dim=('lat', 'lon'))
south_future_winter_years1 = south_future_winter1['time.year']

# Repeat the above lines for the second model
folder1 = f'../graphs/data/{MODEL2}/{AREAS[0]}/fldmeans/seasmeans'
folder2 = f'../graphs/data/{MODEL2}/{AREAS[1]}/fldmeans/seasmeans'

north_future_winter2 = xr.open_dataset(folder1+f'/daily_CI_{MODEL2}_future_{SEASON}{AREAS[0]}_fldmean_seasmean.nc')
south_future_winter2 = xr.open_dataset(folder2+f'/daily_CI_{MODEL2}_future_{SEASON}{AREAS[1]}_fldmean_seasmean.nc')

north_future_winter_ci2 = north_future_winter2['total_comfort'].mean(dim=('lat', 'lon'))
north_future_winter_years2 = north_future_winter2['time.year']
south_future_winter_ci2 = south_future_winter2['total_comfort'].mean(dim=('lat', 'lon'))
south_future_winter_years2 = south_future_winter2['time.year']

# Create a figure with 1 row and 1 column
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(north_future_winter_years1, north_future_winter_ci1, label=f'{MODEL1} {AREAS[0].capitalize()} Europe', color='blue')

z1 = np.polyfit(north_future_winter_years1, north_future_winter_ci1, 1)
p1 = np.poly1d(z1)
ax.plot(north_future_winter_years1, p1(north_future_winter_years1), "b--")

ax.plot(south_future_winter_years1, south_future_winter_ci1, label=f'{MODEL1} {AREAS[1].capitalize()} Europe', color='red')

z2 = np.polyfit(south_future_winter_years1, south_future_winter_ci1, 1)
p2 = np.poly1d(z2)
ax.plot(south_future_winter_years1, p2(south_future_winter_years1), "r--",)

# Add the second model to the plot

ax.plot(north_future_winter_years2, north_future_winter_ci2, label=f'{MODEL2} {AREAS[0].capitalize()} Europe', color='violet')

z3 = np.polyfit(north_future_winter_years2, north_future_winter_ci2, 1)
p3 = np.poly1d(z3)
ax.plot(north_future_winter_years2, p3(north_future_winter_years2), "m--")


ax.plot(south_future_winter_years2, south_future_winter_ci2, label=f'{MODEL2} {AREAS[1].capitalize()} Europe', color='orange')

z4 = np.polyfit(south_future_winter_years2, south_future_winter_ci2, 1)
p4 = np.poly1d(z4)
ax.plot(south_future_winter_years2, p4(south_future_winter_years2), "y--")

# Add x and y axis labels and title
ax.set_title(f'{SEASON.capitalize()} Mean Comfort Index in South and North Europe (SSPS 8.5)')
ax.set_xlabel('Year')
ax.set_ylabel('Comfort Index')

# Add legend
ax.legend()

plt.savefig('../graphs//winter/winter_ci_future_regression_both_models.png', dpi=200)