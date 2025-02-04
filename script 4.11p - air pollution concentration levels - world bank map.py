# In[]:
# Date: Sep 15, 2024
# Project: Identify grid level particulate matter (PM2.5) concentration
# Author: Farhad Panahov

# description:

# Compare weighted vs unweighted and weighted vs WB concentration values --- PLOT









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


# load weighted and unweighted concentration estimates
df_concentration_worldbank = pd.read_excel('1 - input/3 - concentration levels/API_EN.ATM.PM25.MC.M3_DS2_en_excel_v2_1313.xlsx', skiprows=3)

# load world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# merge
world_merged = pd.merge(world, df_concentration_worldbank[['Country Code', '2020']], left_on='iso_a3', right_on='Country Code', how='left')





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
#plt.style.use(['science'])

# Disable LaTeX rendering to avoid LaTeX-related errors
plt.rcParams['text.usetex'] = False










# In[]
##################################################################################################
##################### WORLD BANK WORLD PM25 LEVEL MAP ############################################
##################################################################################################


# Plot the map with 2020 values and adjust the legend size and spacing
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world_merged.plot(column='2020', cmap='coolwarm', legend=True, ax=ax,
                  legend_kwds={'label': "PM2.5 Air Pollution (µg/m³)",
                               'orientation': "horizontal",
                               'shrink': 0.6,
                               'pad': 0.05})  # Reduce padding between the plot and legend

# Add title and clean up the layout
ax.axis('off')
plt.show()



