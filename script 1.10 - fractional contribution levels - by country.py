# In[1]:
# Date: Oct 19, 2024
# Project: Identify grid level fractional contribution levels --- Country identified --- grouped to 2 decimal places
# Author: Farhad Panahov

# description:

# Steps: Map grid level 'fractional contribution' data onto countries. 
#   Source: script 100 output, which combined raw datafiles and grouped lon/lat by 2 decimal points
#   Source: Global share data: 




# In[2]:
# load packages

import numpy as np
import pandas as pd
import time
import os
import geopandas as gpd
from shapely.geometry import Point





# In[3]:
# directory

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory





# In[3]: LOAD AND EDIT ALL DATASETS
#####################################################

# Here we load and map data to global country shapes

# load fractional cotribution data
df_fractional = pd.read_csv('2 - output/script 1/s1.00 - 1 - frac dist - global.csv')


# load countries
df_world = gpd.read_file("1 - input/2 - global map/ne_110m_admin_0_countries.shp")
print(df_world.crs) # EPSG:4326


# Convert fractional contribution to polygons
df_fractional['geometry'] = df_fractional.apply(lambda row: Point(row['Lon'], row['Lat']), axis=1)
df_fractional = gpd.GeoDataFrame(df_fractional, geometry='geometry')

df_fractional = gpd.GeoDataFrame(
    df_fractional, 
    geometry=gpd.points_from_xy(df_fractional['Lon'], df_fractional['Lat']),
    crs="EPSG:4326"  # Set the CRS to WGS84
)


# get country lists
country_codes = list(df_world['GU_A3'].unique()) # using GU_A3 for country classification --- there are some errors (-99) in ISO_A3
df_country_codes = pd.DataFrame(country_codes, columns = ["country_code"])









# In[3]: RUN THE LOOP TO ADD COUNTRIES
#####################################################

# Initialize an empty list to collect filtered DataFrames for each country
df_fractional_country = []


# Loop over each country in _countries
for country_code in country_codes:
       
    # print
    print("Start: ", country_code)
    
    # Get the country's geometry (polygon or multipolygon)
    temp_country = df_world[df_world['GU_A3'] == country_code]
    temp_geom = temp_country['geometry'].iloc[0]
    
    # Get the bounds (min and max longitude and latitude)
    minx, miny, maxx, maxy = temp_geom.bounds
    
    # Filter the df_fractional data based on the bounding box of the country
    temp_fractional_filtered = df_fractional[
        (df_fractional['Lon'] >= minx) & (df_fractional['Lon'] <= maxx) &
        (df_fractional['Lat'] >= miny) & (df_fractional['Lat'] <= maxy)
    ]  
    
    # Now further filter to include only points that are within the actual geometry (not just the bounding box)
    temp_fractional_country = gpd.sjoin(temp_fractional_filtered, temp_country, how='inner', predicate='within')

    # keep only required columns
    temp_fractional_country = temp_fractional_country[['Lon', 'Lat', 'ENEcoal', 'ENEother', 'GU_A3']].reset_index(drop=True)

    # Append the result to the list
    df_fractional_country.append(temp_fractional_country)


# Concatenate all country results into a single DataFrame
df_fractional_country = pd.concat(df_fractional_country, ignore_index=True)


# delete
del country_code, maxx, maxy, minx, miny, temp_country, temp_fractional_country, temp_fractional_filtered, temp_geom
del df_fractional


# Print the first 10 rows of the final DataFrame
print(df_fractional_country.head(10))

#       Lon    Lat   ENEcoal  ENEother ISO_A3
# 0 -179.95 -16.45  0.000910  0.004700    FJI
# 1 -179.95 -16.35  0.000910  0.004700    FJI
# 2 -179.95 -16.25  0.000910  0.004700    FJI
# 3 -179.95 -16.15  0.000910  0.004700    FJI
# 4 -179.85 -16.15  0.000910  0.004700    FJI
# 5 -179.85 -16.05  0.000910  0.004700    FJI
# 6  177.35 -17.95  0.002158  0.022856    FJI
# 7  177.35 -17.85  0.002130  0.023120    FJI
# 8  177.35 -17.75  0.002130  0.023120    FJI
# 9  177.45 -18.15  0.002270  0.021800    FJI










# In[]

# export data

# Save the final aggregated DataFrame to a CSV file
df_fractional_country.to_csv('2 - output/script 1/s1.10 - 1 - frac dist - bycountry.csv', index=False)
df_country_codes.to_csv('2 - output/script 1/s1.10 - 2 - frac dist - country list.csv', index=False)



    


