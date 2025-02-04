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
from adjustText import adjust_text
import scienceplots  # This registers the styles










# In[]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# load weighted and unweighted concentration estimates
df_concentration = pd.read_excel('2 - output/script 4/s4.10 - 1 - concentration level - comparison.xlsx')







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
##################### WEIGHTED vs UNWEIGHETED vs WORLD BANK ######################################
##################################################################################################

# Label specific countries with a flat offset
labels = {'IND': 'India', 'IDN': 'Indonesia', 'ZAF': 'South Africa', 'MEX': 'Mexico',
          'VNM': 'Viet Nam', 'IRN': 'Iran', 'THA': 'Thailand', 'EGY': 'Egypt',
          'USA': 'United States', 'CHN': 'China', 'QTR':'Qatar', 'NGA':'Nigeria',
          'TUR':'Türkiye', 'BRA':'Brazil', 'DEU':'Germany', 'SAU': 'Saudi Arabia'}


fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Define arrow properties with a curved connection style
arrow_props = dict(
    arrowstyle='->',
    color='grey',
    lw=0.5,
    shrinkA=5,
    shrinkB=5,
    connectionstyle="arc3,rad=0.1"  # adjust the rad parameter to change curvature
)

# ===============================
# Subplot 1: Weighted vs Unweighted
# ===============================
axs[0].scatter(df_concentration['weighted'], df_concentration['unweighted'],
               color='blue', alpha=0.3, label='Countries', marker='x')
axs[0].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line', alpha=0.4)

texts0 = []
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        txt = axs[0].annotate(
            labels[row['country']],
            xy=(row['weighted'], row['unweighted']),  # Data point (arrow tip)
            xytext=(row['weighted']+5, row['unweighted']+3),  # Offset position
            fontsize=10,
            arrowprops=arrow_props,
        )
        texts0.append(txt)

# Adjust text positions to avoid overlaps
adjust_text(texts0, ax=axs[0])

axs[0].set_xlabel('Population weighted', fontsize=12)
axs[0].set_ylabel('Unweighted (average)', fontsize=12)
axs[0].set_title('Population weighted vs Unweighted', fontsize=14)
axs[0].legend(handles=[
    plt.Line2D([0], [0], color='black', marker='x', linestyle='', label='Countries'),
    plt.Line2D([0], [0], color='red', linestyle='--', label='45° Line')
], loc='best')
axs[0].grid(True, linestyle='--', alpha=0.5)

# ===============================
# Subplot 2: Weighted vs World Bank
# ===============================
axs[1].scatter(df_concentration['weighted'], df_concentration['world_bank'],
               color='green', alpha=0.3, label='Countries', marker='x')
axs[1].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line', alpha=0.4)

texts1 = []
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        txt = axs[1].annotate(
            labels[row['country']],
            xy=(row['weighted'], row['world_bank']),
            xytext=(row['weighted']+5, row['world_bank']+3),  # Offset position
            fontsize=10,
            arrowprops=arrow_props,
        )
        texts1.append(txt)

# Adjust text positions to avoid overlaps
adjust_text(texts1, ax=axs[1])

axs[1].set_xlabel('Population weighted', fontsize=12)
axs[1].set_ylabel('World Bank estimate', fontsize=12)
axs[1].set_title('Population weighted vs World Bank', fontsize=14)
axs[1].grid(True, linestyle='--', alpha=0.5)

plt.subplots_adjust(wspace=30)


fig.tight_layout()
fig.savefig('comparison.png', dpi=1200, bbox_inches='tight')
plt.show()