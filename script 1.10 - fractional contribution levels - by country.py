# In[1]:
# Date: Oct 19, 2024
# Project: Identify grid level fractional contribution levels --- Country identified --- grouped to 2 decimal places
# Author: Farhad Panahov

# description:

# Steps: Map grid level 'fractional contribution' data onto countries. 
#   Source: script 100 output, which combined raw datafiles and grouped lon/lat by 2 decimal points
#   Source: Countries --- https://datacatalog.worldbank.org/search/dataset/0038272/World-Bank-Official-Boundaries




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

# Convert fractional contribution to polygons
df_fractional['geometry'] = df_fractional.apply(lambda row: Point(row['Lon'], row['Lat']), axis=1)
df_fractional = gpd.GeoDataFrame(df_fractional, geometry='geometry')

df_fractional = gpd.GeoDataFrame(
    df_fractional, 
    geometry=gpd.points_from_xy(df_fractional['Lon'], df_fractional['Lat']),
    crs="EPSG:4326"  # Set the CRS to WGS84
)



# load countries
df_world = gpd.read_file("1 - input/2 - global map/wb_countries_admin0_10m/WB_countries_Admin0_10m.shp")
print(df_world.crs) # EPSG:4326

# fix some items manually --- 3 countries dont have names / a few -99 values left to be removed too
df_world.loc[df_world['FORMAL_EN'] == "French Republic", 'ISO_A3'] = "FRA"
df_world.loc[df_world['FORMAL_EN'] == "Kingdom of Norway", 'ISO_A3'] = "NOR"
df_world.loc[df_world['FORMAL_EN'] == "Republic of Kosovo", 'ISO_A3'] = "KSV"
df_world = df_world.loc[df_world['ISO_A3'] != "-99"]

# there are some countries with multiple lines, combining them
df_world_combined = df_world.dissolve(by="ISO_A3").reset_index()


# get country lists
country_codes = list(df_world_combined['ISO_A3'].unique()) 
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
    temp_country = df_world[df_world['ISO_A3'] == country_code]
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
    temp_fractional_country = temp_fractional_country[['Lon', 'Lat', 'ENEcoal', 'ENEother', 'ISO_A3']].reset_index(drop=True)

    # Append the result to the list
    df_fractional_country.append(temp_fractional_country)


# Concatenate all country results into a single DataFrame
df_fractional_country = pd.concat(df_fractional_country, ignore_index=True)


# delete
del country_code, maxx, maxy, minx, miny, temp_country, temp_fractional_country, temp_fractional_filtered, temp_geom
del df_fractional


# Print the first 10 rows of the final DataFrame
print(df_fractional_country.head(10))

#      Lon    Lat  ENEcoal  ENEother ISO_A3
# 0 -70.05  12.55  0.00059   0.02476    ABW
# 1  60.55  33.65  0.01384   0.04461    AFG
# 2  60.55  33.75  0.01384   0.04461    AFG
# 3  60.55  33.85  0.01384   0.04461    AFG
# 4  60.55  33.95  0.01384   0.04461    AFG
# 5  60.55  34.05  0.01500   0.04820    AFG
# 6  60.55  34.15  0.01500   0.04820    AFG
# 7  60.65  32.85  0.01066   0.03688    AFG
# 8  60.65  32.95  0.01066   0.03688    AFG
# 9  60.65  33.05  0.01208   0.04033    AFG


# list of countries
df_country_codes['in_fractional_country'] = df_country_codes['country_code'].isin(df_fractional_country['ISO_A3'].unique())

# delete
del df_world, df_world_combined





# In[]

# export data

# Save the final aggregated DataFrame to a CSV file
df_fractional_country.to_csv('2 - output/script 1/s1.10 - 1 - frac dist - bycountry.csv', index=False)
df_country_codes.to_csv('2 - output/script 1/s1.10 - 2 - frac dist - country list.csv', index=False)



    


