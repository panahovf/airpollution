# In[1]:
# Date: Sep 2, 2024
# Project: Identify mortality rates based on response function to PM levels and share of mortality attibuted to PM
# Author: Farhad Panahov










# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.gridspec as gridspec
import scienceplots
import seaborn as sns
from matplotlib.ticker import MaxNLocator









# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# --------------
# MORTALITY DATA
df_annual_mortality_cp_total = pd.read_excel('2 - output/script 5/s5.20 - 1 - annual mortality by country - current policy - response lower.xlsx')
df_annual_mortality_nz_total = pd.read_excel('2 - output/script 5/s5.20 - 2 - annual mortality by country - nz 1.5c - response lower.xlsx')


# --------------
# ECONOMIC DATA
#df_inflation = pd.read_excel('1 - input/5 - econ data/inflation - annual change.xlsx', skiprows = 3)
#df_gdpcapita = pd.read_csv('1 - input/5 - econ data/gdp per capita ppp - WB.csv', skiprows = 4)
df_vsl = pd.read_excel('1 - input/8 - econ data/1-Age-adjusted and age-invariant VSL.xlsx', skiprows = 3)


# --------------
# REGIONAL DATA
df_regions = pd.read_excel('1 - input/6 - country datasets/UNFCCC classification.xlsx')
developing = list(df_regions[df_regions['classification'] == "Developing"]['iso_3'].unique())
developed = list(df_regions[df_regions['classification'] == "All Developed"]['iso_3'].unique())


# In[4]: SET ANNUAL VSL
# #####################################

# # --------------
# this is 2019 $
print(df_vsl['Age-invariant VSL-Mean'].describe())
# count    4.080000e+03
# mean     1.445539e+06
# std      1.555476e+06
# min      2.209026e+03
# 25%      2.217390e+05
# 50%      7.858591e+05
# 75%      2.497186e+06
# max      8.169917e+06
# Name: Age-invariant VSL-Mean, dtype: float64

df_vsl = df_vsl.groupby('Country - iso3c')['Age-invariant VSL-Mean'].mean().reset_index()









# In[4]: GET TOTAL BENEFIT
#####################################

# country names & ilness for loop
country_codes = list(df_annual_mortality_cp_total['Country'].unique())


# variable 
discount_rate = 1.028 # 2.8%


results = []

# loop through each country 
for country in country_codes:
    
    # get VSL for the country
    vsl = df_vsl.loc[df_vsl['Country - iso3c'] == country, 'Age-invariant VSL-Mean'].values[0]
    
    # empty datafram
    df_temp = pd.DataFrame()
    
    # add country & years to it
    df_temp['Country'] = ''   ### create country as first column
    df_temp['Year'] = list(range(2024, 2051))
    df_temp['Country'] = country


    # add total mortality across all diseases --- annual
    # Filter data for the country from df_annual_mortality_cp_total
    filtered_data_cp = df_annual_mortality_cp_total.loc[
        df_annual_mortality_cp_total['Country'] == country, 
        ['Year', 'annual mortality', 'annual mortality nogrowth']
    ]
    
    filtered_data_cp.rename(columns={'annual mortality': 'mortality_cp',
                            'annual mortality nogrowth': 'mortality_cp_nogrowth'}, inplace=True)
   
    # Merge the filtered data on Year to match and bring over values
    df_temp = pd.merge(
        df_temp, 
        filtered_data_cp, 
        on='Year', 
        how='left'
    )
    
    
    # add total mortality across all diseases --- annual
    # Filter data for the country from df_annual_mortality_cp_total
    filtered_data_nz = df_annual_mortality_nz_total.loc[
        df_annual_mortality_nz_total['Country'] == country, 
        ['Year', 'annual mortality', 'annual mortality nogrowth']
    ]
    
    filtered_data_nz.rename(columns={'annual mortality': 'mortality_nz',
                            'annual mortality nogrowth': 'mortality_nz_nogrowth'}, inplace=True)
   
    # Merge the filtered data on Year to match and bring over values
    df_temp = pd.merge(
        df_temp, 
        filtered_data_nz, 
        on='Year', 
        how='left'
    )
    
       
  
    # create difference CP vs NZ15 50%
    df_temp['mortality_diff_annual'] = df_temp['mortality_cp'] - df_temp['mortality_nz']
    df_temp['mortality_diff_cumulative'] = df_temp['mortality_diff_annual'].cumsum()

    # # create difference CP vs NZ15 50% - no population growth
    df_temp['mortality_diff_annual_nogrowth'] = df_temp['mortality_cp_nogrowth'] - df_temp['mortality_nz_nogrowth']
    df_temp['mortality_diff_cumulative_nogrowth'] = df_temp['mortality_diff_annual_nogrowth'].cumsum()


    # calculate economic benefit
    df_temp['econ_benefit_cumulative_(mln $2019)'] = df_temp['mortality_diff_cumulative'] * vsl/ 1000000 # in millions
    df_temp['econ_benefit_discounted_cumulative_(mln $2019)'] = df_temp['econ_benefit_cumulative_(mln $2019)'] / (discount_rate ** df_temp.index)

    # calculate economic benefit - no population growth
    df_temp['econ_benefit_cumulative_(mln $2019) - nogrowth'] = df_temp['mortality_diff_cumulative_nogrowth'] * vsl/ 1000000 # in millions
    df_temp['econ_benefit_discounted_cumulative_(mln $2019) - nogrowth'] = df_temp['econ_benefit_cumulative_(mln $2019) - nogrowth'] / (discount_rate ** df_temp.index)


    # add VSL
    df_temp['vsl'] = vsl


    results.append(df_temp)




master = pd.concat(results, ignore_index=True)


# In[] GLOBAL and REGIONAL

master_global = master.groupby('Year', as_index=False).sum(numeric_only=True)
master_global["Country"] = "Global"

master_developing = master[master['Country'].isin(developing)].groupby('Year', as_index=False).sum(numeric_only=True)
master_developed = master[master['Country'].isin(developed)].groupby('Year', as_index=False).sum(numeric_only=True)

master_developing["Country"] = "Developing"
master_developed["Country"] = "Developed"

master_global['vsl'] = ""
master_developing['vsl'] = ""
master_developed['vsl'] = ""


master = pd.concat([master, master_global, master_developed, master_developing], ignore_index=True)






# In[4]: GET OVERALL TABLE
#####################################

# Example list of country names
countries = list(master['Country'].unique())

# List to store country DataFrames (this is just an example; replace with your actual DataFrames)

# Initialize an empty list to collect the data
temp_data_benefit = []
temp_data_death = []

# Iterate over each country DataFrame
for country in countries:
    # Extract values for the years 2035 and 2050 --- BENEFIT
    value_2035_benefit = master.loc[(master['Year'] == 2035) & (master['Country'] == country), 'econ_benefit_discounted_cumulative_(mln $2019)'].values[0]  # Replace 'value_column_name' with the column name you want
    value_2050_benefit = master.loc[(master['Year'] == 2050) & (master['Country'] == country), 'econ_benefit_discounted_cumulative_(mln $2019)'].values[0]  # Replace 'value_column_name' with the column name you want
    
    # Extract values for the years 2035 and 2050 --- DEATH
    value_2035_death = master.loc[(master['Year'] == 2035) & (master['Country'] == country), 'mortality_diff_cumulative'].values[0]  # Replace 'value_column_name' with the column name you want
    value_2050_death = master.loc[(master['Year'] == 2050) & (master['Country'] == country), 'mortality_diff_cumulative'].values[0]  # Replace 'value_column_name' with the column name you want
    
    # Append the data as a dictionary
    temp_data_benefit.append({'Country': country, 'Cumulative economic benefit (mln $2019): 2035': value_2035_benefit, 'Cumulative economic benefit (mln $2019): 2050': value_2050_benefit})
    temp_data_death.append({'Country': country, 'Cumulative avoided death: 2035': value_2035_death, 'Cumulative avoided death: 2050': value_2050_death})

# Create a new DataFrame with the collected data
df_benefit = pd.DataFrame(temp_data_benefit)
df_death = pd.DataFrame(temp_data_death)


# delete
del temp_data_benefit, temp_data_death, countries, value_2035_benefit, value_2050_benefit, value_2035_death, value_2050_death
del country, country_codes, df_regions, df_temp, vsl
del filtered_data_cp, filtered_data_nz, results, master_developed, master_developing, master_global






# In[]

# export data

# --------------
# annual concentration levels - grid
master.to_excel('2 - output/script 6/s6.10_- 1 - annual economic benefits - response lower.xlsx', index = False)


# tables
df_benefit.to_excel('2 - output/script 6/s6.10_- 2.1 - table - economic benefits - response lower.xlsx', index = False)
df_death.to_excel('2 - output/script 6/s6.10_- 2.2 - table - avoided death - response lower.xlsx', index = False)

