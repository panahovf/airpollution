# In[1]:
# Date: Sep 2, 2024
# Project: Identify 3 letter code for mortality dataset 
# Author: Farhad Panahov










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
# MORTALITY RATES
# https://vizhub.healthdata.org/gbd-results/
# stroke; tracjeal,bronchus, and lung cancer; diabetes melittus type 2; ischemic heart disease; lower respiratory infections; chronic obstructive pulmonary disease
# death per 100K
df_mortality = pd.read_excel('1 - input/7 - mortality/mortality rates - by country.xlsx')


# --------------
# country name/codes
df_countries = pd.read_excel('1 - input/6 - country datasets/country_gca_region.xlsx')










# In[4]: IDENTIFY 3 LETTER CODES
#####################################

# merge to get 3 letter codes
df_mortality = pd.merge(df_mortality, df_countries[['name', 'alpha-3']],
                           left_on= 'Location', right_on='name', how = 'left')


# identify missing countries
missing = df_mortality.loc[df_mortality['alpha-3'].isna(), 'Location'].unique()
print(missing)

# ["Democratic People's Republic of Korea"
#  'Democratic Republic of the Congo' 'Palestine' 'Republic of Korea'
#  'Republic of Moldova' 'Taiwan (Province of China)' 'United Kingdom'
#  'United Republic of Tanzania' 'United States Virgin Islands']


# manually override
df_mortality.loc[df_mortality['Location'] == "Democratic People's Republic of Korea", 'alpha-3'] = "PRK"
df_mortality.loc[df_mortality['Location'] == "Democratic Republic of the Congo", 'alpha-3'] = "COD"
df_mortality.loc[df_mortality['Location'] == "Palestine", 'alpha-3'] = "PSE"
df_mortality.loc[df_mortality['Location'] == "Republic of Korea", 'alpha-3'] = "KOR"
df_mortality.loc[df_mortality['Location'] == "Republic of Moldova", 'alpha-3'] = "MDA"
df_mortality.loc[df_mortality['Location'] == "Taiwan (Province of China)", 'alpha-3'] = "TWN"
df_mortality.loc[df_mortality['Location'] == "United Kingdom", 'alpha-3'] = "GBR"
df_mortality.loc[df_mortality['Location'] == "United Republic of Tanzania", 'alpha-3'] = "TZA"
df_mortality.loc[df_mortality['Location'] == "United States Virgin Islands", 'alpha-3'] = "VIR"


# check
missing_still = df_mortality.loc[df_mortality['alpha-3'].isna(), 'Location'].unique()
print(missing_still)
# []







# In[]

# export data

# --------------
df_mortality.to_excel('2 - output/script 5/s5.00 - 1 - mortality rate - country iso3.xlsx', index = False)







