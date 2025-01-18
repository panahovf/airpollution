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
df_annual_mortality_cp_total = pd.read_excel('2 - output/script 5/s5.20 - 1 - annual mortality by country - current policy.xlsx')
df_annual_mortality_nz_total = pd.read_excel('2 - output/script 5/s5.20 - 2 - annual mortality by country - nz 1.5c.xlsx')


# --------------
# ECONOMIC DATA
#df_inflation = pd.read_excel('1 - input/5 - econ data/inflation - annual change.xlsx', skiprows = 3)
#df_gdpcapita = pd.read_csv('1 - input/5 - econ data/gdp per capita ppp - WB.csv', skiprows = 4)
df_vsl = pd.read_excel('1 - input/8 - econ data/1-Age-adjusted and age-invariant VSL.xlsx', skiprows = 3)





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
    
       
    # add VSL 
    df_temp['vls'] = vsl
    
    
    # create difference CP vs NZ15 50%
    df_temp['diff_annual'] = df_temp['mortality_cp'] - df_temp['mortality_nz']
    df_temp['diff_cumulative'] = df_temp['diff_annual'].cumsum()

    # create difference CP vs NZ15 50%
    df_temp['diff_annual_nogrowth'] = df_temp['mortality_cp_nogrowth'] - df_temp['mortality_nz_nogrowth']
    df_temp['diff_cumulative_nogrowth'] = df_temp['diff_annual_nogrowth'].cumsum()


    # calculate economic benefit
    df_temp['econ_benefit (mln)'] = df_temp['diff_cumulative'] * vsl/ 1000000 # in millions
    df_temp['econ_benefit_discounted (mln)'] = df_temp['econ_benefit (mln)'] / (discount_rate ** df_temp.index)

    # calculate economic benefit
    df_temp['econ_benefit (mln) - nogrowth'] = df_temp['diff_cumulative_nogrowth'] * vsl/ 1000000 # in millions
    df_temp['econ_benefit_discounted (mln) - nogrowth'] = df_temp['econ_benefit (mln) - nogrowth'] / (discount_rate ** df_temp.index)


    results.append(df_temp)




master = pd.concat(results, ignore_index=True)


# delete



master.loc[master['Year'] == 2050, 'econ_benefit_discounted (mln)'].sum()





# In[]

# export data

# --------------
# annual concentration levels - grid
master.to_excel('2 - output/script 6/s6.10_- 1 - annual economic benefits - global decarb.xlsx', index = False)


