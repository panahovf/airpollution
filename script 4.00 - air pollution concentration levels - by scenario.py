# In[1]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Step 1: Get grid level 'fractional contribution source' from each type of fossil fuels. 
#   Here is the source: https://zenodo.org/records/4739100
#   Sources included: Coal and Other (oil & gas)
#   Note: this data has been sampled for the time being for Poland as a case study
#           based on max/min lat and long of Poland
#           for simplification, it is now in rectangular shape

# Step 2: Get grid level 'air pollution exposure estimates' i.e. current concentration levels.
#   Here is the source: https://ghdx.healthdata.org/record/ihme-data/gbd-2021-air-pollution-exposure-estimates-1990-2021
#   Use PM2.5 mean values
#   Note: data is given in .tif format (IHME_GBD_2021_AIR_POLLUTION_1990_2021_PM_MEAN_2020_Y2023M04D19)


# Step 3: Get grid level 'population estimates' i.e. current concentration levels.
#   Here is the source: https://human-settlement.emergency.copernicus.eu/download.php?ds=pop
#   Product: GHS-POP, epoch: 2020, resolution: 30 arcsec, coordinate system: WGS84
#   Note: Get following squares: r4 c20, r4 c21, r5 c20, r5 c21
#           using QGIC software, convert .tif file to a .csv with Long/Lat and grid values.
#           This data has been sampled for the time being for Poland as a case study same as above
   









# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# --------------
# FRACTIONAL CONTRIBUTION DATA
df_frac_contribution = pd.read_csv('2 - output/script 1/s1.10 - 1 - frac dist - bycountry.csv')
df_frac_contribution['Lat'] = df_frac_contribution['Lat'].round(2)
df_frac_contribution['Lat'] = df_frac_contribution['Lat'].round(2)


# --------------
# CONCENTRATION LEVELS
df_concentration_baseline = pd.read_csv('2 - output/script 2/s2.00 - 1 - pm concentration - global.csv')
df_concentration_baseline['Lat'] = df_concentration_baseline['Lat'].round(2)
df_concentration_baseline['Lat'] = df_concentration_baseline['Lat'].round(2)


# --------------
# POPULATION DATA
df_population = pd.read_csv('2 - output/script 3/s3.00 - 1 - population - global.csv')
df_population['Lat'] = df_population['Lat'].round(2)
df_population['Lon'] = df_population['Lon'].round(2)


# --------------
# EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\9.1 - Current policy - Secondary - annual.xlsx')
df_nz_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')









# In[4]: COMBINE FRACTION CONTRUBITIONS AND CONCENTRATION
#####################################

# --------------
# filter fraction data to match concentration data
df_frac_contribution = df_frac_contribution[df_frac_contribution['Lat'].isin(df_concentration_baseline['Lat'])]
df_frac_contribution = df_frac_contribution[df_frac_contribution['Lon'].isin(df_concentration_baseline['Lon'])]


# --------------
# merge these 2 dataframes
# NZ
df_concentration_nz = pd.merge(df_frac_contribution, df_concentration_baseline[['Lat', 'Lon', 'concentration']],
                     left_on=['Lat', 'Lon'], right_on=['Lat', 'Lon'], how='left')
df_concentration_nz.rename(columns={'concentration': 'Current_level'}, inplace=True)
df_concentration_nz = df_concentration_nz[~df_concentration_nz['Current_level'].isna()]

# CP
df_concentration_cp = pd.merge(df_frac_contribution, df_concentration_baseline[['Lat', 'Lon', 'concentration']],
                     left_on=['Lat', 'Lon'], right_on=['Lat', 'Lon'], how='left')
df_concentration_cp.rename(columns={'concentration': 'Current_level'}, inplace=True)
df_concentration_cp = df_concentration_cp[~df_concentration_cp['Current_level'].isna()]


# # MAX
df_concentration_max = pd.merge(df_frac_contribution, df_concentration_baseline[['Lat', 'Lon', 'concentration']],
                      left_on=['Lat', 'Lon'], right_on=['Lat', 'Lon'], how='left')
df_concentration_max.rename(columns={'concentration': 'Current_level'}, inplace=True)
df_concentration_max = df_concentration_max[~df_concentration_max['Current_level'].isna()]


# delete
del df_concentration_baseline, df_frac_contribution





# In[4]: GET EMISSIONS REDUCTION SHARE UNDER NZ SCENARIO
########################################################

# set year
year_columns = [str(year) for year in range(2024, 2051)]

# create a full shut down scenario
df_max_power = df_cp_power.copy() ### create full shot down scenario
df_max_power[year_columns[1:]] = 0 ### set 2025-2050 to zero


# --------------
# STEP 1:
# Combine Oil and Gas emissions for both power and extraction to match fraction contribution data

# scenarios and countries
scenarios = ["CP", "NZ", "MAX"]
countries = list(df_cp_power['Region'].unique())


# Dictionary to store results by scenario and country
results = {sc: [] for sc in scenarios}


# loop through each country within each scenario
for sc in scenarios:
    # Copy the scenario-specific DataFrame
    original_df = globals()[f"df_{sc.lower()}_power"].copy()
    
    for country in countries:
        # Filter the DataFrame for the specific country
        country_df = original_df[original_df['Region'] == country].copy()

        # Create O&G category and add the sum of OIL and GAS values
        temp = country_df[country_df['fuel_type'] == "Oil"].copy()  # Filter to oil
        temp['fuel_type'] = 'O&G'  # Change the 'fuel_type' column value to 'O&G'
        temp[year_columns] = country_df[country_df['fuel_type'].isin(['Oil', 'Gas'])][year_columns].sum()  # Add oil and gas values

        # Update the country-specific DataFrame
        country_df = pd.concat([country_df, temp], ignore_index=True)  # Append the new row to the DataFrame
        country_df = country_df[~country_df['fuel_type'].isin(['Oil', 'Gas'])]  # Remove the original 'Oil' and 'Gas' rows

        # Append the processed DataFrame for this country to the results dictionary
        results[sc].append(country_df)

# Combine results for each scenario into a single DataFrame
final_dfs = {sc: pd.concat(results[sc], ignore_index=True) for sc in scenarios}


# Update original dataframes
globals()['df_cp_power'] = final_dfs['CP']
globals()['df_nz_power'] = final_dfs['NZ']
globals()['df_max_power'] = final_dfs['MAX']


# delete
del results, sc, country, original_df, country_df, temp, final_dfs
del countries





# --------------
# STEP 2: Get CP vs NZ difference: (1-NZ)/Current levels
# i.e. emissions reduction under NZ as a share of current level

# Dictionary to store results
reductions = {}

for sc in scenarios:
    # Access the relevant DataFrame using `globals`
    df_power = globals()[f"df_{sc.lower()}_power"].copy()

    # Calculate the reduction
    df_power_reduction = df_power.copy()
    df_power_reduction[year_columns] = (1 - df_power[year_columns].div(df_power['2024'], axis=0)).fillna(0)

    # Store the result in a dictionary for later use
    reductions[f"{sc}_power_reduction"] = df_power_reduction

# Assign the results back to globals
globals()['df_cp_power_reduction'] = reductions['CP_power_reduction']
globals()['df_nz_power_reduction'] = reductions['NZ_power_reduction']
globals()['df_max_power_reduction'] = reductions['MAX_power_reduction']


# CHECK
# There are some 'inf' results
print(df_cp_power.loc[df_cp_power_reduction['2050'] == -np.inf, '2024'].sum())
print(df_nz_power.loc[df_cp_power_reduction['2050'] == -np.inf, '2024'].sum())
print(df_cp_power['2024'].sum())
# Prints:
# 0.0
# 0.0
# 14136

print(df_cp_power.loc[df_cp_power_reduction['2050'] == -np.inf, '2050'].sum())
print(df_cp_power['2050'].sum())
print(df_nz_power.loc[df_cp_power_reduction['2050'] == -np.inf, '2050'].sum())
print(df_nz_power['2050'].sum())
# Prints:
# 26.024707055475528
# 17316.42354241102
# 0.9196950806983045
# 181.7161457879662

# these are very small values --- hence setting them to zero
df_cp_power_reduction[year_columns] = df_cp_power_reduction[year_columns].replace(-np.inf, 0)
df_nz_power_reduction[year_columns] = df_nz_power_reduction[year_columns].replace(-np.inf, 0)


# delete
del reductions, sc, df_power, df_power_reduction
del df_cp_power, df_nz_power, df_max_power










# In[4]: GET NET ZERO ADJUSTED AIR POLLUTION CONCENTRATION STATS
#################################################################

# iterate over each year to get concentration statistics


# --------------
# remove extreme values that represent 'no data'
df_concentration_nz = df_concentration_nz[df_concentration_nz['Current_level'] > 0]
df_concentration_cp = df_concentration_cp[df_concentration_cp['Current_level'] > 0]
df_concentration_max = df_concentration_max[df_concentration_max['Current_level'] > 0]

         
# create dataframes with reduction for each fuel type individually
df_concentration_nz_total = df_concentration_nz.copy()
df_concentration_nz_total = df_concentration_nz_total[df_concentration_nz_total['GU_A3'].isin(df_nz_power_reduction['Region'])]

df_concentration_cp_total = df_concentration_cp.copy()
df_concentration_cp_total = df_concentration_cp_total[df_concentration_cp_total['GU_A3'].isin(df_cp_power_reduction['Region'])]

df_concentration_max_total = df_concentration_max.copy()
df_concentration_max_total = df_concentration_max_total[df_concentration_max_total['GU_A3'].isin(df_max_power_reduction['Region'])]



# Loop
# NZ
# Initialize an empty list to store the results for each country
results = []

# Get unique countries in GU_A3
countries = df_concentration_nz_total['GU_A3'].unique()

# Loop over each country
for country in countries:
    # Filter the concentration DataFrame and reduction DataFrame for the current country
    df_country = df_concentration_nz_total[df_concentration_nz_total['GU_A3'] == country].copy()
    
    coal_reduction = df_nz_power_reduction[
        (df_nz_power_reduction['fuel_type'] == 'Coal') & 
        (df_nz_power_reduction['Region'] == country)
    ]
    
    oilgas_reduction = df_nz_power_reduction[
        (df_nz_power_reduction['fuel_type'] == 'O&G') & 
        (df_nz_power_reduction['Region'] == country)
    ]

    # Perform calculations for all years
    for year in year_columns:
        
        # If no reduction data for the country, default to 0
        coal_factor = coal_reduction[year].values[0] if not coal_reduction.empty else 0
        oilgas_factor = oilgas_reduction[year].values[0] if not oilgas_reduction.empty else 0
        
        # Calculate reductions
        df_country[year] = df_country['Current_level'] - (df_country['ENEcoal'] * coal_factor + df_country['ENEother'] * oilgas_factor)

    # Append the processed country DataFrame to the results list
    results.append(df_country)

# Combine all the country results into a single DataFrame
df_concentration_nz_total = pd.concat(results, ignore_index=True)



# --------------
# CP
# Initialize an empty list to store the results for each country
results = []

# Get unique countries in GU_A3
countries = df_concentration_cp_total['GU_A3'].unique()

# Loop over each country
for country in countries:
    # Filter the concentration DataFrame and reduction DataFrame for the current country
    df_country = df_concentration_cp_total[df_concentration_cp_total['GU_A3'] == country].copy()
    
    coal_reduction = df_cp_power_reduction[
        (df_cp_power_reduction['fuel_type'] == 'Coal') & 
        (df_cp_power_reduction['Region'] == country)
    ]
    
    oilgas_reduction = df_cp_power_reduction[
        (df_cp_power_reduction['fuel_type'] == 'O&G') & 
        (df_cp_power_reduction['Region'] == country)
    ]

    # Perform calculations for all years
    for year in year_columns:
        
        # If no reduction data for the country, default to 0
        coal_factor = coal_reduction[year].values[0] if not coal_reduction.empty else 0
        oilgas_factor = oilgas_reduction[year].values[0] if not oilgas_reduction.empty else 0
        
        # Calculate reductions
        df_country[year] = df_country['Current_level'] - (df_country['ENEcoal'] * coal_factor + df_country['ENEother'] * oilgas_factor)

    # Append the processed country DataFrame to the results list
    results.append(df_country)

# Combine all the country results into a single DataFrame
df_concentration_cp_total = pd.concat(results, ignore_index=True)





# --------------
# MAX
# Initialize an empty list to store the results for each country
results = []

# Get unique countries in GU_A3
countries = df_concentration_max_total['GU_A3'].unique()

# Loop over each country
for country in countries:
    # Filter the concentration DataFrame and reduction DataFrame for the current country
    df_country = df_concentration_max_total[df_concentration_max_total['GU_A3'] == country].copy()
    
    coal_reduction = df_max_power_reduction[
        (df_max_power_reduction['fuel_type'] == 'Coal') & 
        (df_max_power_reduction['Region'] == country)
    ]
    
    oilgas_reduction = df_max_power_reduction[
        (df_max_power_reduction['fuel_type'] == 'O&G') & 
        (df_max_power_reduction['Region'] == country)
    ]

    # Perform calculations for all years
    for year in year_columns:
        
        # If no reduction data for the country, default to 0
        coal_factor = coal_reduction[year].values[0] if not coal_reduction.empty else 0
        oilgas_factor = oilgas_reduction[year].values[0] if not oilgas_reduction.empty else 0
        
        # Calculate reductions
        df_country[year] = df_country['Current_level'] - (df_country['ENEcoal'] * coal_factor + df_country['ENEother'] * oilgas_factor)

    # Append the processed country DataFrame to the results list
    results.append(df_country)

# Combine all the country results into a single DataFrame
df_concentration_max_total = pd.concat(results, ignore_index=True)




# delete
del coal_factor, oilgas_factor, df_country, results, year, country, countries, coal_reduction, oilgas_reduction
del df_concentration_cp, df_concentration_nz, df_concentration_max








# In[4]: GET POPULATION WEIGHTED CONCENTRATION VALUES
#####################################################

# --------------
# keep only common pairs of lat long
df_concentration_nz_total = pd.merge(df_concentration_nz_total, df_population, left_on=['Lat', 'Lon'], right_on=['Lat', 'Lon'], how='inner')
df_concentration_cp_total = pd.merge(df_concentration_cp_total, df_population, left_on=['Lat', 'Lon'], right_on=['Lat', 'Lon'], how='inner')
df_concentration_max_total = pd.merge(df_concentration_max_total, df_population, left_on=['Lat', 'Lon'], right_on=['Lat', 'Lon'], how='inner')


# check sum total of missing population due to match
print((df_population['population'].sum() - df_concentration_nz_total['population'].sum())/10**9, "billion")
# 1.651021165900095 billion



# -------------
# CP
# Initialize an empty dictionary to store results for each country
country_results = {}

# Get the unique countries in the dataset
countries = df_concentration_cp_total['GU_A3'].unique()

# Loop over each country
for country in countries:
    # Filter the dataset for the current country
    df_country = df_concentration_cp_total[df_concentration_cp_total['GU_A3'] == country].copy()
    
    # Total population for the current country
    total_population = df_country['population'].sum()
    
    # Create a temporary DataFrame to store weighted values
    temp = df_country.copy()
    
    # Compute the weighted values for each year
    for year in year_columns:
        temp[year] = temp[year].multiply(temp['population'], axis=0).div(total_population)
    
    # Sum across all grid cells for each year
    temp_sum = temp[year_columns].sum(axis=0)
    
    # Store the result in the dictionary with the country as the key
    country_results[country] = temp_sum

# Convert the dictionary to a DataFrame
df_concentration_cp_country = pd.DataFrame.from_dict(country_results, orient='index', columns=year_columns)

# Add the country names as a column (optional, since they will already be in the index)
df_concentration_cp_country.index.name = 'Country'
df_concentration_cp_country.reset_index(inplace=True)




# ------------------
# NZ
# Initialize an empty dictionary to store results for each country
country_results = {}

# Get the unique countries in the dataset
countries = df_concentration_nz_total['GU_A3'].unique()

# Loop over each country
for country in countries:
    # Filter the dataset for the current country
    df_country = df_concentration_nz_total[df_concentration_nz_total['GU_A3'] == country].copy()
    
    # Total population for the current country
    total_population = df_country['population'].sum()
    
    # Create a temporary DataFrame to store weighted values
    temp = df_country.copy()
    
    # Compute the weighted values for each year
    for year in year_columns:
        temp[year] = temp[year].multiply(temp['population'], axis=0).div(total_population)
    
    # Sum across all grid cells for each year
    temp_sum = temp[year_columns].sum(axis=0)
    
    # Store the result in the dictionary with the country as the key
    country_results[country] = temp_sum

# Convert the dictionary to a DataFrame
df_concentration_nz_country = pd.DataFrame.from_dict(country_results, orient='index', columns=year_columns)

# Add the country names as a column (optional, since they will already be in the index)
df_concentration_nz_country.index.name = 'Country'
df_concentration_nz_country.reset_index(inplace=True)



# -------------
# MAX
# Initialize an empty dictionary to store results for each country
country_results = {}

# Get the unique countries in the dataset
countries = df_concentration_max_total['GU_A3'].unique()

# Loop over each country
for country in countries:
    # Filter the dataset for the current country
    df_country = df_concentration_max_total[df_concentration_max_total['GU_A3'] == country].copy()
    
    # Total population for the current country
    total_population = df_country['population'].sum()
    
    # Create a temporary DataFrame to store weighted values
    temp = df_country.copy()
    
    # Compute the weighted values for each year
    for year in year_columns:
        temp[year] = temp[year].multiply(temp['population'], axis=0).div(total_population)
    
    # Sum across all grid cells for each year
    temp_sum = temp[year_columns].sum(axis=0)
    
    # Store the result in the dictionary with the country as the key
    country_results[country] = temp_sum

# Convert the dictionary to a DataFrame
df_concentration_max_country = pd.DataFrame.from_dict(country_results, orient='index', columns=year_columns)

# Add the country names as a column (optional, since they will already be in the index)
df_concentration_max_country.index.name = 'Country'
df_concentration_max_country.reset_index(inplace=True)


# delete
del countries, country, country_results, total_population, temp_sum, temp, year, df_country


# # concentration level stats --- ratio of 2050 to 2024 level
# ratio_cp = df_concentration_nz_country.copy()
# ratio_cp['ratio'] = ratio_cp['2050']/ratio_cp['2024']
# ratio_cp['ratio'].describe()
# # Out[337]: 
# # count    135.000000
# # mean       1.032498
# # std        0.179010
# # min        0.995752
# # 25%        1.000290
# # 50%        1.003446
# # 75%        1.011162
# # max        3.001378
# # dtype: float64




# # cap concentration level to 2x of 2024 level
# for year in year_columns:
#     df_concentration_cp_country[year] = df_concentration_cp_country.apply(
#         lambda row: min(row[year], 2 * row['2024']), axis=1
#     )







# In[]

# export data

# --------------
# # annual concentration levels - grid
# df_concentration_cp_total.to_excel('2 - output/script 4/s4.00_- 1.1 - annual concentration - grid level - current policy.xlsx', index = False)
# df_concentration_nz_total.to_excel('2 - output/script 4/s4.00 - 1.2 - annual concentration - grid level - net zero 1.5C.xlsx', index = False)
# df_concentration_max_total.to_excel('2 - output/script 4/s4.00 - 1.3 - annual concentration - grid level - max shut down.xlsx', index = False)

# --------------
# annual concentration levels - country
df_concentration_cp_country.to_excel('2 - output/script 4/s4.00 - 2.1 - annual concentration - country level - current policy.xlsx', index = False)
df_concentration_nz_country.to_excel('2 - output/script 4/s4.00 - 2.2 - annual concentration - country level - net zero 1.5C.xlsx', index = False)
df_concentration_max_country.to_excel('2 - output/script 4/s4.00 - 2.3 - annual concentration - country level - max shut down.xlsx', index = False)
