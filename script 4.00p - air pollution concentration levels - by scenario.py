# In[]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# These are maps of concentration levels of
# (1) top 8 developing countiries
# (2) selected regions: China, South Korea, UAE, Qatar, Bahrain, Brunei, Kuwait








# In[]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import geopandas as gpd










# In[]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# LOAD ENV FROM SCRIPT 4.00
# country & lat/lon concentration levels --- weighted and unweighted

# Load a world map from geopandas datasets
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))





# In[]: SELECT REGIONS
#####################################

# ---------
region_1 = ['IND', 'IDN', 'ZAF', 'MEX', 'VNM', 'IRN', 'THA', 'EGY']
region_2 = ['CHN', 'KOR', 'ARE', 'SAU', 'QAT', 'BHR', 'BRN', 'KWT']
region_combined = region_1 + region_2


# ---------
# run a loop to create country specific datasets
# using NET ZERO CARBON BUDGET ALIGNED scenario
for region in region_combined:
      
    # filter for selected region, select Lon,Lat, and concentration
    temp_df_countrty = df_concentration_nz.loc[df_concentration_nz['ISO_A3'] == region,
                                                               ['Lon', 'Lat', '2025', '2030', '2035']]
   
    # set it as a geo datafile
    globals()[f'geo_{region.lower()}'] = gpd.GeoDataFrame(temp_df_countrty, 
        geometry = gpd.points_from_xy(temp_df_countrty.Lon, temp_df_countrty.Lat))
    
    
        
    
    
    



# In[]

#####################################################################
#####################################################################
#####################################################################
#####################################################################
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################
#####################################################################
#####################################################################

# Style
plt.style.use(['science'])

# Disable LaTeX rendering to avoid LaTeX-related errors
plt.rcParams['text.usetex'] = False

# set regions for graphs
years = ['2025', '2030', '2035']

# set colors
country_cmaps = ['viridis_r', 'Blues', 'cividis_r','plasma_r', 'Reds','RdPu', 'GnBu','summer_r']









# In[]
##################################################################################################
##################### REGION 1 ###################################################################
##################################################################################################

# ---------
# set names and datasets
countries = ['India', 'Indonesia', 'South Africa', 'Mexico', 'Viet Nam', 'Iran', 'Thailan', 'Egypt']
dataframes = [geo_ind, geo_idn, geo_zaf, geo_mex, geo_vnm, geo_irn, geo_tha, geo_egy]

# Filter for the selected regions and years
region_1_concentration_pw = df_concentration_nz_country_pw[
    df_concentration_nz_country_pw['Country'].isin(region_1)
][['Country'] + years]

region_1_concentration_npw = df_concentration_nz_country_npw[
    df_concentration_nz_country_npw['Country'].isin(region_1)
][['Country'] + years]

# Define the min and max values for each country dynamically
# Set mean + 3std as max
for country, df_country in zip(countries, dataframes):
    globals()[f'min_{country}'] = df_country[['2025', '2030', '2035']].min().min()
    globals()[f'max_{country}'] = df_country[['2025', '2030', '2035']].mean().mean() + 3*df_country[['2025', '2030', '2035']].std().mean()


# ---------
# Create a figure with 8 rows and 3 columns (countries x years)
fig, axs = plt.subplots(8, 3, figsize=(24, 36))  # No constrained_layout

# Define the desired aspect ratio (height/width) for each subplot grid cell
aspect_ratio = fig.get_figheight() / fig.get_figwidth() * (3 / 8)  # Grid: 8 rows, 3 columns

# Iterate over each country and year
for i, (country, df_country, cmap, region) in enumerate(zip(countries, dataframes, country_cmaps, region_1)):
    for j, year in enumerate(years):
        ax = axs[i, j]

        # Plot the entire world map as background
        world.plot(ax=ax, color='lightgrey', edgecolor='black')

        # Retrieve min and max values for color scaling using globals()
        vmin = globals()[f'min_{country}']
        vmax = globals()[f'max_{country}']
        
        # Plot the data for the specific country and year
        if j == 2:  # Add a colorbar for the last column (e.g., 2035)
            # Define a new axes for the legend outside the grid
            cax = fig.add_axes([0.92, ax.get_position().y0, 0.02, ax.get_position().height])
            df_country.plot(column=year, ax=ax, legend=True, cmap=cmap, 
                            markersize=5, vmin=vmin, vmax=vmax,
                            legend_kwds={'shrink': 0.80, 'orientation': "vertical", 'cax': cax, 'format': "%.0f"})
        else:
            df_country.plot(column=year, ax=ax, legend=False, cmap=cmap, 
                            markersize=5, vmin=vmin, vmax=vmax)
            
        # Increase the font size of the colorbar numbers
        cax.tick_params(labelsize=12)

        # Set title only for the first row of each column
        if i == 0:
            ax.set_title(f"Year {year}", fontsize=20, fontweight='bold', pad=15)
        
        # Set ylabel for the first column (country name)
        if j == 0:
            ax.annotate(country, xy=(-0.1, 0.5), xycoords='axes fraction', fontsize=20, fontweight='bold',
                        ha='right', va='center', rotation=90)

        # Calculate the data's aspect ratio
        x_min, x_max = df_country['Lon'].min(), df_country['Lon'].max()
        y_min, y_max = df_country['Lat'].min(), df_country['Lat'].max()
        
        # Avoid division by zero --- for the next step --- aspect ration
        if x_max == x_min:
            x_min -= 0.01  # Add a small range
            x_max += 0.01
        if y_max == y_min:
            y_min -= 0.01  # Add a small range
            y_max += 0.01
            
        data_aspect_ratio = (y_max - y_min) / (x_max - x_min)

        # Adjust limits dynamically to match the subplot aspect ratio
        if data_aspect_ratio > aspect_ratio:  # Taller than the grid cell
            center_x = (x_min + x_max) / 2
            width = (y_max - y_min) / aspect_ratio
            ax.set_xlim(center_x - width / 2, center_x + width / 2)
            ax.set_ylim(y_min, y_max)
        else:  # Wider than the grid cell
            center_y = (y_min + y_max) / 2
            height = (x_max - x_min) * aspect_ratio
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(center_y - height / 2, center_y + height / 2)

        # Remove x and y axis labels and ticks for better visualization
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")


        # --- Add Annotation for PW and NPW Values ---
        # Get the respective values from both dataframes for the current year and country
        pw_value = region_1_concentration_pw.loc[region_1_concentration_pw['Country'] == region, str(year)].values[0]
        npw_value = region_1_concentration_npw.loc[region_1_concentration_npw['Country'] == region, str(year)].values[0]

        # Format the values as strings
        annotation_text = f"Weighted: {pw_value:.1f}\nUnweighted: {npw_value:.1f}"

        # Add the text annotation to the subplot
        ax.text(
            0.15, 0.15,  # Adjust to be inside the plot area (y=0.1 for above the bottom)
            annotation_text,
            transform=ax.transAxes,
            fontsize=12,
            ha='center',
            va='top',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))

# Adjust subplot spacing to avoid overlaps
plt.subplots_adjust(wspace=0.05, hspace=0.05)

# Show the plot
plt.show()










# In[]
##################################################################################################
##################### REGION 2 ###################################################################
##################################################################################################

# ---------
# set names and datasets
countries = ['China', 'South Korea', 'United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Bahrain', 'Brunei', 'Kuwait']
dataframes = [geo_chn, geo_kor, geo_are, geo_sau, geo_qat, geo_bhr, geo_brn, geo_kwt]

# Filter for the selected regions and years
region_2_concentration_pw = df_concentration_nz_country_pw[
    df_concentration_nz_country_pw['Country'].isin(region_2)
][['Country'] + years]

region_2_concentration_npw = df_concentration_nz_country_npw[
    df_concentration_nz_country_npw['Country'].isin(region_2)
][['Country'] + years]


# Define the min and max values for each country dynamically
# Set mean + 3std as max
for country, df_country in zip(countries, dataframes):
    globals()[f'min_{country}'] = df_country[['2025', '2030', '2035']].min().min()
    globals()[f'max_{country}'] = df_country[['2025', '2030', '2035']].mean().mean() + 3*df_country[['2025', '2030', '2035']].std().mean()


# ---------
# Create a figure with 8 rows and 3 columns (countries x years)
fig, axs = plt.subplots(8, 3, figsize=(24, 36))  # No constrained_layout

# Define the desired aspect ratio (height/width) for each subplot grid cell
aspect_ratio = fig.get_figheight() / fig.get_figwidth() * (3 / 8)  # Grid: 8 rows, 3 columns

# Iterate over each country and year
for i, (country, df_country, cmap, region) in enumerate(zip(countries, dataframes, country_cmaps, region_1)):
    for j, year in enumerate(years):
        ax = axs[i, j]

        # Plot the entire world map as background
        world.plot(ax=ax, color='lightgrey', edgecolor='black')

        # Retrieve min and max values for color scaling using globals()
        vmin = globals()[f'min_{country}']
        vmax = globals()[f'max_{country}']
        
        # Plot the data for the specific country and year
        if j == 2:  # Add a colorbar for the last column (e.g., 2035)
            # Define a new axes for the legend outside the grid
            cax = fig.add_axes([0.92, ax.get_position().y0, 0.02, ax.get_position().height])
            df_country.plot(column=year, ax=ax, legend=True, cmap=cmap, 
                            markersize=5, vmin=vmin, vmax=vmax,
                            legend_kwds={'shrink': 0.80, 'orientation': "vertical", 'cax': cax, 'format': "%.0f"})
        else:
            df_country.plot(column=year, ax=ax, legend=False, cmap=cmap, 
                            markersize=5, vmin=vmin, vmax=vmax)
            
        # Increase the font size of the colorbar numbers
        cax.tick_params(labelsize=12)

        # Set title only for the first row of each column
        if i == 0:
            ax.set_title(f"Year {year}", fontsize=20, fontweight='bold', pad=15)
        
        # Set ylabel for the first column (country name)
        if j == 0:
            ax.annotate(country, xy=(-0.1, 0.5), xycoords='axes fraction', fontsize=20, fontweight='bold',
                        ha='right', va='center', rotation=90)

        # Calculate the data's aspect ratio
        x_min, x_max = df_country['Lon'].min(), df_country['Lon'].max()
        y_min, y_max = df_country['Lat'].min(), df_country['Lat'].max()
        
        # Avoid division by zero --- for the next step --- aspect ration
        if x_max == x_min:
            x_min -= 0.01  # Add a small range
            x_max += 0.01
        if y_max == y_min:
            y_min -= 0.01  # Add a small range
            y_max += 0.01
            
        data_aspect_ratio = (y_max - y_min) / (x_max - x_min)

        # Adjust limits dynamically to match the subplot aspect ratio
        if data_aspect_ratio > aspect_ratio:  # Taller than the grid cell
            center_x = (x_min + x_max) / 2
            width = (y_max - y_min) / aspect_ratio
            ax.set_xlim(center_x - width / 2, center_x + width / 2)
            ax.set_ylim(y_min, y_max)
        else:  # Wider than the grid cell
            center_y = (y_min + y_max) / 2
            height = (x_max - x_min) * aspect_ratio
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(center_y - height / 2, center_y + height / 2)

        # Remove x and y axis labels and ticks for better visualization
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("")
        ax.set_ylabel("")


        # --- Add Annotation for PW and NPW Values ---
        # Get the respective values from both dataframes for the current year and country
        pw_value = region_1_concentration_pw.loc[region_1_concentration_pw['Country'] == region, str(year)].values[0]
        npw_value = region_1_concentration_npw.loc[region_1_concentration_npw['Country'] == region, str(year)].values[0]

        # Format the values as strings
        annotation_text = f"Weighted: {pw_value:.1f}\nUnweighted: {npw_value:.1f}"

        # Add the text annotation to the subplot
        ax.text(
            0.15, 0.15,  # Adjust to be inside the plot area (y=0.1 for above the bottom)
            annotation_text,
            transform=ax.transAxes,
            fontsize=12,
            ha='center',
            va='top',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))

# Adjust subplot spacing to avoid overlaps
plt.subplots_adjust(wspace=0.05, hspace=0.05)

# Show the plot
plt.show()

