# In[]:
# Date: Sep 15, 2024
# Project: Response function sensitivity analysis
# Author: Farhad Panahov

# description

# Plotting results from low/mid/upper level response functions for sensitivity check
# for top 8 developig countries: India, Indonesia, South Africa, Mexico, Viet Nam, Iran, Thailand, Egypt






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


# Load final results for each of the 3 scenarios
df_mean = pd.read_excel('2 - output/script 6/s6.00_- 1 - annual economic benefits.xlsx')
df_lower = pd.read_excel('2 - output/script 6/s6.10_- 1 - annual economic benefits - response lower.xlsx')
df_upper = pd.read_excel('2 - output/script 6/s6.30_- 1 - annual economic benefits - response upper.xlsx')





# In[]: COMBINE
#####################################

# -------
# create combined dataset
df_mean = df_mean.loc[df_mean['Year'] == 2035,['Country', 'econ_benefit_discounted_cumulative_(mln $2019)', 'econ_benefit_discounted_cumulative_(mln $2019) - nogrowth']]
df_lower = df_lower.loc[df_lower['Year'] == 2035,['Country', 'econ_benefit_discounted_cumulative_(mln $2019)', 'econ_benefit_discounted_cumulative_(mln $2019) - nogrowth']]
df_upper = df_upper.loc[df_upper['Year'] == 2035,['Country', 'econ_benefit_discounted_cumulative_(mln $2019)', 'econ_benefit_discounted_cumulative_(mln $2019) - nogrowth']]
        

# -------
# filter for countries
countries = ['IND', 'IDN', 'ZAF', 'MEX', 'VNM', 'IRN', 'THA', 'EGY']
df_mean = df_mean[df_mean['Country'].isin(countries)]
df_lower = df_lower[df_lower['Country'].isin(countries)]
df_upper = df_upper[df_upper['Country'].isin(countries)]


# -------
# merge
df_combined = pd.merge(df_mean, df_lower[['Country', 'econ_benefit_discounted_cumulative_(mln $2019)', 'econ_benefit_discounted_cumulative_(mln $2019) - nogrowth']], on='Country')
df_combined = pd.merge(df_combined, df_upper[['Country', 'econ_benefit_discounted_cumulative_(mln $2019)', 'econ_benefit_discounted_cumulative_(mln $2019) - nogrowth']], on='Country')


# -------
# sort coutnry order
df_combined = df_combined.set_index('Country').loc[countries].reset_index()


# -------
# column names --- pg = population growth, npg = no population growth
df_combined.columns = [
    'country', 
    'benefit - mean - pg', 'benefit - mean - npg',
    'benefit - lower - pg', 'benefit - lower - npg',
    'benefit - upper - pg', 'benefit - upper - npg'
]


# -------
# add chart display name
display_names = ['India', 'Indonesia', 'South Africa', 'Mexico', 'Viet Nam', 'Iran', 'Thailand', 'Egypt']
df_combined['display_name'] = display_names




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








# In[]
##################################################################################################
##################### SENSITIVITY ################################################################
##################################################################################################

# Define bar positions
x = np.arange(len(df_combined["country"]))  # Bar positions
bar_width = 0.4

# Extract mean values
mean_pg = df_combined["benefit - mean - pg"]
mean_npg = df_combined["benefit - mean - npg"]

# Calculate error bars (upper and lower bounds)
error_lower_pg = mean_pg - df_combined["benefit - lower - pg"]
error_upper_pg = df_combined["benefit - upper - pg"] - mean_pg

error_lower_npg = mean_npg - df_combined["benefit - lower - npg"]
error_upper_npg = df_combined["benefit - upper - npg"] - mean_npg

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

# Plot bars for PG and NPG with error bars
bars_pg = ax.bar(x - bar_width/2, mean_pg, bar_width, yerr=[error_lower_pg, error_upper_pg],
                 capsize=5, color='skyblue', edgecolor='black', label='With population growth')

bars_npg = ax.bar(x + bar_width/2, mean_npg, bar_width, yerr=[error_lower_npg, error_upper_npg],
                  capsize=5, color='salmon', edgecolor='black', label='No population growth')

# Add a single error bar label (without plotting additional data)
ax.errorbar([0], [0], yerr=[0], fmt='none', ecolor='black', capsize=5, label='Response function sensitivity:\nupper and lower range')

# Adjust labels for long names to wrap into two lines
wrapped_labels = [
    'India', 
    'Indonesia', 
    'South\nAfrica', 
    'Mexico', 
    'Viet\nNam', 
    'Iran', 
    'Thailand', 
    'Egypt'
]

# Set x-axis labels
ax.set_xticks(x)
ax.set_xticklabels(wrapped_labels, rotation=0, ha='center', fontsize=12)

# Labels and title
ax.set_ylabel('Billions USD', fontsize=12)
ax.set_title('Cumulative Economic Benefits by Country by 2035', fontsize=16, pad=20)

# Format y-axis to show thousands with a custom formatter
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y/1000:.0f}'))

# Add a legend
ax.legend(loc='upper right', fontsize=12)

# Add horizontal grid
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Show the plot
plt.tight_layout()
plt.show()



