# In[]:
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
#   Units: all units are in fractional percentages (e.g., 0.0245 is 2.45%) 

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
   









# In[]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns










# In[]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# --------------
# FRACTIONAL CONTRIBUTION DATA
df_frac_contribution = pd.read_csv('2 - output/script 1/s1.10 - 1 - frac dist - bycountry.csv')


# --------------
# CONCENTRATION LEVELS
df_concentration_baseline = pd.read_csv('2 - output/script 2/s2.00 - 1 - pm concentration - global.csv')


# --------------
# POPULATION DATA
df_population = pd.read_csv('2 - output/script 3/s3.00 - 1 - population - global.csv')


# --------------
# EMISSSION DATA FOR CURRENT POLICIES VS NET ZERO 1.5 50% adjusted (version where positive growth in fossil fuel growth in reduced along with increase phase out pace) 
df_cp_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\9.1 - Current policy - Secondary - annual.xlsx')
df_nz_power = pd.read_excel(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script 4.2\6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')


# --------------
# LOAD ORIGINAL POWER DATA FROM FORWARD ANALYTICS --- and filter for only operating fossil fuel power plants
df_power = pd.read_csv(r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\1 - input\v3_power_Forward_Analytics2024.csv')
df_power = df_power[df_power['subsector'].isin(['Coal','Oil','Gas'])]
df_power = df_power[df_power['status'] == "operating"]
df_power.loc[df_power['countryiso3'] == 'TZ1', 'countryiso3'] = 'TZA'
df_power = df_power.loc[df_power['countryiso3'] != 'unknown']









# In[]: COMBINE FRACTION CONTRUBITIONS, POPULATION & CONCENTRATION
#####################################

# --------------
# combine fractional contrubition with population database
df_contributionXpopulation = pd.merge(df_frac_contribution, df_population, on=['Lat', 'Lon'], how='inner')

# check for population numbers
print('total population =',(df_population['population'].sum()/10**6).round(0), 'million')
print('mapped to fractional contribution =',(df_contributionXpopulation['population'].sum()/10**6).round(0), 'million')
print('missing =', ((df_population['population'].sum()-df_contributionXpopulation['population'].sum())/10**6).round(0), 'million')
# total population = 7841.0 million
# mapped to fractional contribution = 7601.0 million
# missing = 240.0 million


# --------------
# combine with concentration data
df_concentration = pd.merge(df_contributionXpopulation, df_concentration_baseline, on=['Lat', 'Lon'], how = 'inner')

# check for population numbers
print('mapped to concentration =',(df_concentration['population'].sum()/10**6).round(0), 'million')
print('missing =', ((df_population['population'].sum()-df_concentration['population'].sum())/10**6).round(0), 'million')
print('overall missing ', ((1 - df_concentration['population'].sum()/df_population['population'].sum())*100).round(2), '% of total population')
# mapped to concentration = 7600.0 million
# missing = 241.0 million
# overall missing  3.07 % of total population


# --------------
# delete
del df_concentration_baseline, df_frac_contribution, df_contributionXpopulation








    
# In[]: SHUTDOWN  --- MAX SCENARIO
#####################################
    
# get full shut down factors and total impact value
# 1 --- factors (C bar) = Concentration X Fractional contribution
# 2 --- total impact = Concentration - C bar
    
df_concentration['factor_coal'] = df_concentration['concentration'] *  df_concentration['ENEcoal'] 
df_concentration['factor_oilgas'] = df_concentration['concentration'] *  df_concentration['ENEother'] 
    
df_concentration['max_shutdown'] = df_concentration['concentration'] - (df_concentration['factor_coal'] + df_concentration['factor_oilgas'])
    

    
    
    





# In[]: GET EMISSIONS REDUCTION SHARE UNDER NZ SCENARIO
########################################################

# FORMULA
# S (s,y,f,t) = 1 - [E(s,y,f,t) / E(y,f,2024)]


# --------------
# set year & scenarios
year_columns = [str(year) for year in range(2024, 2051)]
scenarios = ["cp", "nz",]


# --------------
# STEP 1:
# Combine Oil and Gas emissions for both power and extraction to match fraction contribution data

# list of countries
countries = list(df_cp_power['Region'].unique())

# Dictionary to store results by scenario and country
results = {sc: [] for sc in scenarios}

# loop through each country within each scenario
for sc in scenarios:
    # Copy the scenario-specific DataFrame
    original_df = globals()[f"df_{sc}_power"].copy()
    
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
globals()['df_cp_power'] = final_dfs['cp']
globals()['df_nz_power'] = final_dfs['nz']

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
    df_power_scenario = globals()[f"df_{sc}_power"].copy()

    # Calculate the reduction
    # Fill NA(0) can happen if country doesnt have fossil fuel type in 2024 and stays that way
    df_power_reduction = df_power_scenario.copy()
    df_power_reduction[year_columns] = (1 - df_power_scenario[year_columns].div(df_power_scenario['2024'], axis=0)).fillna(0)

    # Store the result in a dictionary for later use
    reductions[f"{sc}_power_reduction"] = df_power_reduction

# Assign the results back to globals
globals()['df_cp_power_reduction'] = reductions['cp_power_reduction']
globals()['df_nz_power_reduction'] = reductions['nz_power_reduction']


# --------------
# CHECK
# Some countries dont have fossil fuel type in 2024, and introduce later, which results in -inf value
print('CP 2050 emissions for countries with -inf values =', df_cp_power.loc[df_cp_power_reduction['2050'] == -np.inf, '2050'].sum().round())
print('CP 2050 total emissions =', df_cp_power['2050'].sum().round())
print('NZ 2050 emissions for countries with -inf values =', df_nz_power.loc[df_cp_power_reduction['2050'] == -np.inf, '2050'].sum().round())
print('NZ 2050 total emissions =', df_nz_power['2050'].sum().round())
# CP 2050 emissions for countries with -inf values = 26.0
# CP 2050 total emissions = 17316.0
# NZ 2050 emissions for countries with -inf values = 1.0
# NZ 2050 total emissions = 182.0

# these are very small values --- hence setting them to zero
df_cp_power_reduction[year_columns] = df_cp_power_reduction[year_columns].replace(-np.inf, 0)
df_nz_power_reduction[year_columns] = df_nz_power_reduction[year_columns].replace(-np.inf, 0)


# --------------
# delete
del reductions, sc, df_power_scenario, df_power_reduction
del df_cp_power, df_nz_power







# In[]: GET NET ZERO ADJUSTED AIR POLLUTION CONCENTRATION STATS
#################################################################

# FORMULA
# C(s,y,z,t) = C(y,z,2024) - sum{} S(s,y,f,t) X C(bar)
# where C(bar) is C X F

# NOTE: Captures only countries that explicitly exists in the NGFS list
# Doesnt include 'Small country aggregate' --- Downscaling|Countries without IEA statistics
# A couple countries: NZL, TWN are not in the CONCENTRATION data

# --------------
# copy dataframes for NZ and CP 2024-2050 extension based on emissions path
df_concentration_nz = df_concentration.copy()
df_concentration_nz = df_concentration_nz[df_concentration_nz['ISO_A3'].isin(df_power['countryiso3'])]

df_concentration_cp = df_concentration.copy()
df_concentration_cp = df_concentration_cp[df_concentration_cp['ISO_A3'].isin(df_power['countryiso3'])]


# --------------
# loop through countries within each scenario across all years
for sc in scenarios:
    # Dynamically access scenario-specific DataFrames
    t_df_concentration = globals()[f"df_concentration_{sc}"].copy()
    t_df_power_reduction = globals()[f"df_{sc}_power_reduction"].copy()

    # Initialize an empty list to store the results for each country
    t_results = []

    # Get unique countries
    t_countries = df_power['countryiso3'].unique()

    # Loop over each country
    for t_country in t_countries:
        
        t_country_ngfs = t_country
        
        # Here if country doesnt exits in NGFS model, set 'Downscaling|Countries without IEA statistics' path for it
        if t_country_ngfs not in df_cp_power_reduction['Region'].values:
            t_country_ngfs = 'Downscaling|Countries without IEA statistics'

        
        # Filter the concentration DataFrame and reduction DataFrame for the current country
        t_df_country = t_df_concentration[t_df_concentration['ISO_A3'] == t_country].copy()

        t_coal_reduction_path = t_df_power_reduction[
            (t_df_power_reduction['fuel_type'] == 'Coal') & 
            (t_df_power_reduction['Region'] == t_country_ngfs)]

        t_oilgas_reduction_path = t_df_power_reduction[
            (t_df_power_reduction['fuel_type'] == 'O&G') & 
            (t_df_power_reduction['Region'] == t_country_ngfs)]

        # Perform calculations for all years
        for t_year in year_columns:
            # If no reduction data for the country, default to 0
            t_coal_reduction_value = t_coal_reduction_path[t_year].values[0] if not t_coal_reduction_path.empty else 0
            t_oilgas_reduction_value = t_oilgas_reduction_path[t_year].values[0] if not t_oilgas_reduction_path.empty else 0

            # Calculate reductions
            t_df_country.loc[:,t_year] = t_df_country['concentration'] - (
                t_df_country['factor_coal'] * t_coal_reduction_value + t_df_country['factor_oilgas'] * t_oilgas_reduction_value)

        # Append the processed country DataFrame to the results list
        t_results.append(t_df_country)

    # Combine all the country results back into the scenario DataFrame
    globals()[f"df_concentration_{sc}"] = pd.concat(t_results, ignore_index=True)


# delete
del t_coal_reduction_path, t_coal_reduction_value, t_countries, t_country, t_df_concentration
del t_df_country, t_df_power_reduction, t_oilgas_reduction_path, t_oilgas_reduction_value, t_results, t_year
del sc, t_country_ngfs
del df_concentration




# In[]: GET POPULATION WEIGHTED CONCENTRATION VALUES
#####################################################

print('Latest directly included population estimate is: ',df_concentration_nz['population'].sum().round())
print('Share of global population missed or included within "Downscaling|Countries without IEA statistics":', ((1 - (df_concentration_nz['population'].sum()/df_population['population'].sum()))*100).round(2), '%')
print('Absolute shortall: ',((df_population['population'].sum() - df_concentration_nz['population'].sum())/10**9).round(2), "billion")
# Latest included population estimate is:  7322802593.0
# Share of global population missed: 6.61 %
# Absolute shortall:  0.52 billion

# Initialize a dictionary to store results for each scenario
t_scenario_results = {}

# Loop over scenarios
for sc in scenarios:
    # Dynamically access the appropriate DataFrame
    t_df_concentration = globals()[f"df_concentration_{sc}"]
    
    # Initialize a dictionary to store results for each country
    t_country_results = {}
    
    # Get the unique countries in the dataset
    t_countries = t_df_concentration['ISO_A3'].unique()
    
    # Loop over each country
    for t_country in t_countries:
        # Filter the dataset for the current country
        t_df_country = t_df_concentration[t_df_concentration['ISO_A3'] == t_country].copy()
        
        # Total population for the current country
        t_total_population = t_df_country['population'].sum()
        
        # Compute the weighted values for each year and sum them
        t_df_country_weighted = t_df_country[['ENEcoal', 'ENEother' , 'max_shutdown'] + year_columns].multiply(t_df_country['population'], axis=0).div(t_total_population).sum(axis=0)
                
        # Store the result in the dictionary with the country as the key
        t_country_results[t_country] = t_df_country_weighted
       
    # Store the scenario results as DF in the dictionary
    t_scenario_results[sc] = pd.DataFrame.from_dict(t_country_results, orient='index', columns= ['ENEcoal', 'ENEother' , 'max_shutdown'] + year_columns)

# Access the results
df_concentration_cp_country_pw = t_scenario_results['cp'].reset_index().rename(columns={'index': 'Country'})
df_concentration_nz_country_pw = t_scenario_results['nz'].reset_index().rename(columns={'index': 'Country'})


# -------------
# delete
del t_countries, t_country, t_country_results, t_df_concentration, t_df_country
del t_df_country_weighted, t_scenario_results, t_total_population
del sc

# # concentration level stats --- ratio of 2050 to 2024 level
# t_ratio_cp = df_concentration_cp_country_pw.copy()
# t_ratio_cp['ratio'] = t_ratio_cp['2050']/t_ratio_cp['2024']
# t_ratio_cp['ratio'].describe()
# count    138.000000
# mean       1.448058
# std        1.972944
# min        0.900463
# 25%        1.006125
# 50%        1.069649
# 75%        1.216602
# max       20.680377
# Name: ratio, dtype: float64







# In[]: COUNTRY CONCENTRATION LEVEL - SIMPLE AVERAGE
#####################################################

# Initialize a dictionary to store results for each scenario
t_scenario_results = {}

# Loop over scenarios
for sc in scenarios:
    # Dynamically access the appropriate DataFrame
    t_df_concentration = globals()[f"df_concentration_{sc}"]
    
    # Group by country and compute the mean for each year
    t_df_country = t_df_concentration.groupby('ISO_A3')[['ENEcoal', 'ENEother' , 'max_shutdown'] + year_columns].mean()

    # Directly store the resulting DataFrame in the dictionary
    t_scenario_results[sc] = t_df_country
   
# Access the results
df_concentration_cp_country_npw = t_scenario_results['cp'].reset_index().rename(columns={'ISO_A3': 'Country'})
df_concentration_nz_country_npw = t_scenario_results['nz'].reset_index().rename(columns={'ISO_A3': 'Country'})


# -------------
# delete
del t_df_concentration, t_df_country, t_scenario_results, sc






# In[] MAX SHUTDOWN

# # -------------
# # population weighted

# # get dataframe
# df_concentration_max_pw = df_concentration_cp[['ISO_A3', 'population', 'max_shutdown']]

# # Get the unique countries in the dataset
# t_countries = df_concentration_max_pw['ISO_A3'].unique()

# # collect country results here
# t_country_results = {}

# # Loop over each country
# for t_country in t_countries:
#     # Filter the dataset for the current country
#     t_df_country = df_concentration_max_pw[df_concentration_max_pw['ISO_A3'] == t_country].copy()
    
#     # Total population for the current country
#     t_total_population = t_df_country['population'].sum()
    
#     # Compute the weighted values for each year and sum them
#     t_df_country_weighted = t_df_country['max_shutdown'].multiply(t_df_country['population'], axis=0).div(t_total_population).sum(axis=0)
            
#     # Store the result in the dictionary with the country as the key
#     t_country_results[t_country] = t_df_country_weighted


# # convert into a single dataframe
# df_concentration_max_pw = pd.DataFrame.from_dict(t_country_results, orient='index', columns=['max_shutdown_pw'])
# df_concentration_max_pw.reset_index(inplace = True)
# df_concentration_max_pw.rename(columns={'index': 'Country'}, inplace=True)



# # -------------
# # population weighted

# # get dataframe
# df_concentration_max_npw = df_concentration_cp[['ISO_A3', 'population', 'max_shutdown']]

# # getaverage by country
# df_concentration_max_npw = df_concentration_max_npw.groupby('ISO_A3')[['max_shutdown']].mean()
# df_concentration_max_npw.reset_index(inplace = True)
# df_concentration_max_npw.rename(columns={'ISO_A3': 'Country', 'max_shutdown': 'max_shutdown_npw'}, inplace=True)


# # -------------
# # combine
# df_concentration_max = pd.merge(df_concentration_max_pw, df_concentration_max_npw, on = 'Country')
# df_concentration_max = pd.merge(df_concentration_max, df_concentration_cp_country_pw[['Country','2024']], on='Country')

# # -------------
# # delete
# del df_concentration_max_pw, df_concentration_max_npw
# del t_countries, t_country, t_country_results, t_df_country, t_df_country_weighted, t_total_population





# In[] OVERALL FRACTIONAL CONTRIBUTION OF ENERGY SECTOR


# -------------
# populaition weighted mean
# coal (ENEcoal) - pm2.5 contribution
frac_contribution_coal_global_mean_pw = (df_concentration_cp['ENEcoal']
                                         .multiply(df_concentration_cp['population'])
                                         .div(df_concentration_cp['population'].sum())
                                         .sum())
print(frac_contribution_coal_global_mean_pw.round(3))
# 0.049
# or 4.9%


# oil/gas (ENEother) - pm2.5 contribution
frac_contribution_oilgas_global_mean_pw = (df_concentration_cp['ENEother']
                                         .multiply(df_concentration_cp['population'])
                                         .div(df_concentration_cp['population'].sum())
                                         .sum())
print(frac_contribution_oilgas_global_mean_pw.round(3))
# 0.053
# or 5.3%


# total energy sector
print((frac_contribution_coal_global_mean_pw + frac_contribution_oilgas_global_mean_pw).round(3))
# 0.102
# or 10.2%



# -------------
# simple average
frac_contribution_coal_global_mean_npw = df_concentration_cp['ENEcoal'].mean()
frac_contribution_oilgas_global_mean_npw = df_concentration_cp['ENEother'].mean()
print((frac_contribution_coal_global_mean_npw+frac_contribution_oilgas_global_mean_npw).round(3))
# 0.089
# or 8.9%


# In[] 2024 - vs 2035 COMPARISON

df_comparison = df_concentration_nz_country_pw[['Country','2024', '2035']]
df_comparison['change'] = df_comparison['2035']/df_comparison['2024']-1

print(df_comparison['change'].describe())

# count    138.000000
# mean      -0.068804
# std        0.063308
# min       -0.248130
# 25%       -0.108912
# 50%       -0.070063
# 75%       -0.023114
# max        0.197618
# Name: change, dtype: float64



# In[] ADD SELECT COUNTRIES MANUALLY

# Add Taiwan, New Zealand, Western Sahara, French Guiana
# these were in original power plants dataset, but missing due to concentration/fractional contribution not mapping

# also add Kosovo (it is in tha table in the paper)

# create manual dataframe
df_manual = pd.DataFrame({"Country": ["TWN", "NZL", "ESH", "GUF", "XKX"]})
df_manual[['ENEcoal', 'ENEother' , 'max_shutdown']+year_columns] = ""
  
                                   
# Define country mapping for replication
country_mapping = {
    "TWN": "CHN",  # Taiwan -> China
    "NZL": "AUS",  # New Zealand -> Australia
    "ESH": "MRT",  # Western Sahara -> Mauritania
    "GUF": "SUR",  # French Guiana -> Suriname
    "XKX": "MKD"   # Kosovo -> North Macedonia
}

columns_to_replicate = ['ENEcoal', 'ENEother', 'max_shutdown', '2024']



# Replicate values for each mapped country in both dataframes
for target_country, source_country in country_mapping.items():

    source_values_cp = df_concentration_cp_country_pw.loc[df_concentration_cp_country_pw['Country'] == source_country, columns_to_replicate]
    df_manual.loc[df_manual['Country'] == target_country, columns_to_replicate] = source_values_cp.values



df_manual_cp = df_manual.copy()
df_manual_nz = df_manual.copy()


# Define the list of newly added countries
added_countries = ["TWN", "NZL", "ESH", "GUF", "XKX"]

# Loop through scenarios
for sc in scenarios:
    # Dynamically access scenario-specific DataFrames
    t_df_concentration = globals()[f"df_manual_{sc}"].copy()
    t_df_power_reduction = globals()[f"df_{sc}_power_reduction"].copy()

    # Initialize an empty list to store results for the added countries
    t_results = []

    # Loop over the five added countries only
    for t_country in added_countries:
               
        # Get the mapped country for emissions paths if applicable
        t_country_ngfs = t_country
        
        # If country is missing from NGFS model, set 'Downscaling|Countries without IEA statistics'
        if t_country_ngfs not in df_cp_power_reduction['Region'].values:
            t_country_ngfs = 'Downscaling|Countries without IEA statistics'

        # Filter the concentration DataFrame and reduction DataFrame for the current country
        t_df_country = t_df_concentration[t_df_concentration['Country'] == t_country].copy()

        t_coal_reduction_path = t_df_power_reduction[
            (t_df_power_reduction['fuel_type'] == 'Coal') & 
            (t_df_power_reduction['Region'] == t_country_ngfs)
        ]

        t_oilgas_reduction_path = t_df_power_reduction[
            (t_df_power_reduction['fuel_type'] == 'O&G') & 
            (t_df_power_reduction['Region'] == t_country_ngfs)
        ]

        # Perform calculations for all years
        for t_year in year_columns:
            # If no reduction data for the country, default to 0
            t_coal_reduction_value = t_coal_reduction_path[t_year].values[0] if not t_coal_reduction_path.empty else 0
            t_oilgas_reduction_value = t_oilgas_reduction_path[t_year].values[0] if not t_oilgas_reduction_path.empty else 0

            # Calculate reductions
            t_df_country[t_year] = t_df_country['2024'] - (
                t_df_country['ENEcoal'] * t_coal_reduction_value +
                t_df_country['ENEother'] * t_oilgas_reduction_value
            )

        # Append the processed country DataFrame to the results list
        t_results.append(t_df_country)

    # Combine all the country results back into the scenario DataFrame
    globals()[f"df_manual_{sc}_filled"] = pd.concat(t_results, ignore_index=True)







# In[] ADD MANUALS

df_concentration_cp_country_pw = pd.concat([df_concentration_cp_country_pw, df_manual_cp_filled], ignore_index=True)
df_concentration_nz_country_pw = pd.concat([df_concentration_nz_country_pw, df_manual_nz_filled], ignore_index=True)


# improve this later --- nwp should be separately done as in previous step
df_concentration_cp_country_npw = pd.concat([df_concentration_cp_country_npw, df_manual_cp_filled], ignore_index=True)
df_concentration_nz_country_npw = pd.concat([df_concentration_nz_country_npw, df_manual_nz_filled], ignore_index=True)




# In[] DELETE

del df_population


# In[]

# export data

# --------------
# # annual concentration levels - grid
# df_concentration_cp.to_excel('2 - output/script 4/s4.00_- 1.1 - annual concentration - grid level - current policy.xlsx', index = False)
# df_concentration_nz.to_excel('2 - output/script 4/s4.00 - 1.2 - annual concentration - grid level - net zero 1.5C.xlsx', index = False)

# --------------
# annual concentration levels - country
df_concentration_cp_country_pw.to_excel('2 - output/script 4/s4.00 - 2.1 - annual concentration - country level - current policy - pw.xlsx', index = False)
df_concentration_nz_country_pw.to_excel('2 - output/script 4/s4.00 - 2.2 - annual concentration - country level - net zero 1.5C - pw.xlsx', index = False)

# --------------
# annual concentration levels - country
df_concentration_cp_country_npw.to_excel('2 - output/script 4/s4.00 - 3.1 - annual concentration - country level - current policy - npw.xlsx', index = False)
df_concentration_nz_country_npw.to_excel('2 - output/script 4/s4.00 - 3.2 - annual concentration - country level - net zero 1.5C - npw.xlsx', index = False)


# --------------
# shutdown scenario
df_concentration_max.to_excel('2 - output/script 4/s4.00 - 4.1 - max shutdown results - weighted and unweighted.xlsx', index = False)
