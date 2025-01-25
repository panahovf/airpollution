# In[1]:
# Date: Sep 26, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Steps: Get grid level 'air pollution exposure estimates' i.e. current concentration levels.
#   Here is the source: https://ghdx.healthdata.org/record/ihme-data/gbd-2021-air-pollution-exposure-estimates-1990-2021
#   Use PM2.5 mean values
#   Note: data is given in .tif format (IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19)





# In[2]:
# load packages

import polars as pl
import numpy as np
import pandas as pd
import rasterio
import os





# In[3]:
# directory

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory





# In[3]: LOAD AND EDIT ALL DATASETS
#####################################################


# --------------
# LOAD CURRENT CONCENTRATION LEVELS DATA
with rasterio.open('1 - input/3 - concentration levels/IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19.tif') as dataset:
    # Read the image data
    image_data = dataset.read(1)  # Reading the first band (1 for grayscale or multi-band data can be handled separately)

    # Get the coordinate transform from the dataset
    transform = dataset.transform

    # Create arrays for lon/lat
    rows, cols = np.indices(image_data.shape)
    lon, lat = rasterio.transform.xy(transform, rows, cols, offset='center')


# Flatten the arrays if needed
lon_flat = np.array(lon).flatten()
lat_flat = np.array(lat).flatten()
pixel_values = image_data.flatten()

# Create a Polars DataFrame with lon, lat, and pixel values
df_concentration_baseline = pl.DataFrame({
    'Lon': lon_flat,
    'Lat': lat_flat,
    'concentration': pixel_values
})


# delete
del cols, dataset, image_data, lat, lat_flat, lon, lon_flat, pixel_values, rows, transform


# remove extreme values that represent 'no data'
df_concentration_baseline = df_concentration_baseline.filter(pl.col('concentration') >= 0)


# this data is already given in 0.1 increment for 2 decimal level Lon/Lat starting at 0.05 level
# i.e. 0.05, 0.15, 0.25 etc.
# Step 1: Enforce the format of 0.05 + 0.1 start and increments for Lon and Lat
df_concentration_baseline = df_concentration_baseline.with_columns([
    (((pl.col("Lon") - 0.05) / 0.1).round(0) * 0.1 + 0.05).alias("Lon"),
    (((pl.col("Lat") - 0.05) / 0.1).round(0) * 0.1 + 0.05).alias("Lat")
])

# Step 2: Round Lon and Lat to two decimal places
df_concentration_baseline = df_concentration_baseline.with_columns([
    pl.col("Lon").round(2).alias("Lon"),
    pl.col("Lat").round(2).alias("Lat")
])

# print
print(df_concentration_baseline.head(10))

# shape: (10, 3)
# ┌─────────┬───────┬───────────────┐
# │ Lon     ┆ Lat   ┆ concentration │
# │ ---     ┆ ---   ┆ ---           │
# │ f64     ┆ f64   ┆ f32           │
# ╞═════════╪═══════╪═══════════════╡
# │ -162.65 ┆ 69.95 ┆ 1.403364      │
# │ -162.55 ┆ 69.95 ┆ 1.403014      │
# │ -162.45 ┆ 69.95 ┆ 1.403001      │
# │ -162.35 ┆ 69.95 ┆ 1.403157      │
# │ -162.25 ┆ 69.95 ┆ 1.403211      │
# │ -162.15 ┆ 69.95 ┆ 1.403182      │
# │ -162.05 ┆ 69.95 ┆ 1.403155      │
# │ -161.95 ┆ 69.95 ┆ 1.403179      │
# │ -161.85 ┆ 69.95 ┆ 1.403131      │
# │ -161.75 ┆ 69.95 ┆ 1.403195      │
# └─────────┴───────┴───────────────┘


# convert to panda DF
df_pandas = df_concentration_baseline.to_pandas()
del df_concentration_baseline









# In[]

# export data

# Save the final aggregated DataFrame to a CSV file
df_pandas.to_csv('2 - output/script 2/s2.00 - 1 - pm concentration - global.csv', index=False)


