# In[]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Compare weighted vs unweighted and weighted vs WB concentration values








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


# load weighted and unweighted country estimates
df_weighted = pd.read_excel('2 - output/script 4/s4.00 - 2.2 - annual concentration - country level - net zero 1.5C - pw.xlsx')
df_unweighted = pd.read_excel('2 - output/script 4/s4.00 - 3.2 - annual concentration - country level - net zero 1.5C - npw.xlsx')

# world bank estimates
df_wb = pd.read_excel('1 - input/3 - concentration levels/API_EN.ATM.PM25.MC.M3_DS2_en_excel_v2_1313.xlsx', skiprows=3)




# In[]: MATCH REGIONS
#####################################

# start a combined df
df_combined = df_weighted[['Country', '2024']]

# add unweighted
df_combined = pd.merge(df_combined, df_unweighted[['Country', '2024']], on='Country', how='inner')

# add wb extimate
df_combined = pd.merge(df_combined, df_wb[['Country Code', '2020']], left_on='Country', right_on='Country Code', how='inner')

# drop and rename columns
df_combined.drop(columns=['Country Code'], inplace=True)
df_combined.columns = ['country', 'weighted', 'unweighted', 'world_bank']








# In[]

# export data

# --------------
df_combined.to_excel('2 - output/script 4/s4.10 - 1 - concentration level - comparison.xlsx', index = False)













