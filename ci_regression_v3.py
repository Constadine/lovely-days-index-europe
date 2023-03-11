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
PERIOD, PERIODNAME, INTERVAL, AREA, SEASON = PERIODS[0], PERIODNAMES[0], INTERVALS[0], AREAS[1], SEASONS[0]
folder1 = f'../graphs/data/{MODEL1}/{AREAS[0]}/fldmeans/seasmeans'
folder2 = f'../graphs/data/{MODEL1}/{AREAS[1]}/fldmeans/seasmeans'

nds = xr.open_dataset(folder1+f'/daily_CI_{MODEL1}_{PERIODNAME}_{SEASON}{AREAS[0]}_fldmean_seasmean.nc')
sds = xr.open_dataset(folder2+f'/daily_CI_{MODEL1}_{PERIODNAME}_{SEASON}{AREAS[1]}_fldmean_seasmean.nc')

nds_ci1 = nds['total_comfort'].mean(dim=('lat', 'lon'))
nds_yrs1 = nds['time.year']
sds_ci1 = sds['total_comfort'].mean(dim=('lat', 'lon'))
sds_yrs1 = sds['time.year']

# Repeat the above lines for the second model
folder1 = f'../graphs/data/{MODEL2}/{AREAS[0]}/fldmeans/seasmeans'
folder2 = f'../graphs/data/{MODEL2}/{AREAS[1]}/fldmeans/seasmeans'

nds2 = xr.open_dataset(folder1+f'/daily_CI_{MODEL2}_{PERIODNAME}_{SEASON}{AREAS[0]}_fldmean_seasmean.nc')
sds2 = xr.open_dataset(folder2+f'/daily_CI_{MODEL2}_{PERIODNAME}_{SEASON}{AREAS[1]}_fldmean_seasmean.nc')


nds_ci2 = nds2['total_comfort'].mean(dim=('lat', 'lon'))
nds_yrs2 = nds2['time.year']
sds_ci2 = sds2['total_comfort'].mean(dim=('lat', 'lon'))
sds_yrs2 = sds2['time.year']

# Create a figure with 1 row and 1 column
# Future GFDL-CM4
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(nds_yrs1, nds_ci1, label=f'{MODEL1} {AREAS[0].capitalize()} Europe', color='blue')

z1 = np.polyfit(nds_yrs1, nds_ci1, 1)
p1 = np.poly1d(z1)
ax.plot(nds_yrs1, p1(nds_yrs1), "b--")

ax.plot(sds_yrs1, sds_ci1, label=f'{MODEL1} {AREAS[1].capitalize()} Europe', color='red')

z2 = np.polyfit(sds_yrs1, sds_ci1, 1)
p2 = np.poly1d(z2)
ax.plot(sds_yrs1, p2(sds_yrs1), "r--",)

# Historical GFDL-CM4
fig, ax = plt.subplots(figsize=(10, 8))

ax.plot(nds_yrs1, nds_ci1, label=f'{MODEL1} {AREAS[0].capitalize()} Europe', color='blue')

z1 = np.polyfit(nds_yrs1, nds_ci1, 1)
p1 = np.poly1d(z1)
ax.plot(nds_yrs1, p1(nds_yrs1), "b--")

ax.plot(sds_yrs1, sds_ci1, label=f'{MODEL1} {AREAS[1].capitalize()} Europe', color='red')

z2 = np.polyfit(sds_yrs1, sds_ci1, 1)
p2 = np.poly1d(z2)
ax.plot(sds_yrs1, p2(sds_yrs1), "r--",)

# Add the second model to the plot
# Future MIROC6
ax.plot(nds_yrs2, nds_ci2, label=f'{MODEL2} {AREAS[0].capitalize()} Europe', color='violet')

z3 = np.polyfit(nds_yrs2, nds_ci2, 1)
p3 = np.poly1d(z3)
ax.plot(nds_yrs2, p3(nds_yrs2), "m--")


ax.plot(sds_yrs2, sds_ci2, label=f'{MODEL2} {AREAS[1].capitalize()} Europe', color='orange')

z4 = np.polyfit(sds_yrs2, sds_ci2, 1)
p4 = np.poly1d(z4)
ax.plot(sds_yrs2, p4(sds_yrs2), "y--")

# Add x and y axis labels and title
ax.set_title(f'{SEASON.capitalize()} Mean Comfort Index in South and North Europe {"SSP5 8.5" if PERIODNAME=="future" else "Historical"}')
ax.set_xlabel('Year')
ax.set_ylabel('Comfort Index')

# Add legend
ax.legend()

plt.savefig(F'../graphs/{SEASON}/{SEASON}_ci_{PERIODNAME}_regression_both_models.png', dpi=200)