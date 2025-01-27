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
#plt.style.use(['science'])

# Disable LaTeX rendering to avoid LaTeX-related errors
plt.rcParams['text.usetex'] = False










# In[]
##################################################################################################
##################### WEIGHTED vs UNWEIGHETED vs WORLD BANK ######################################
##################################################################################################

# Combine the two scatter plots side by side with additional spacing
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

# Scatter plot: Weighted vs Unweighted
axs[0].scatter(df_concentration['weighted'], df_concentration['unweighted'], color='blue', alpha=0.7, label='Countries', marker='x')
axs[0].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')
axs[0].set_xlabel('Population weighted', fontsize=12)
axs[0].set_ylabel('Unweighted (average)', fontsize=12)
axs[0].set_title('Weighted vs Unweighted', fontsize=14)
axs[0].legend()
axs[0].grid(True, linestyle='--', alpha=0.5)

# Scatter plot: Weighted vs World Bank
axs[1].scatter(df_concentration['weighted'], df_concentration['world_bank'], color='green', alpha=0.7, label='Countries', marker='x')
axs[1].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')
axs[1].set_xlabel('Population weighted', fontsize=12)
axs[1].set_ylabel('World Bank estimate', fontsize=12)
axs[1].set_title('Weighted vs World Bank', fontsize=14)
#axs[1].legend()
axs[1].grid(True, linestyle='--', alpha=0.5)

# Add spacing between subplots
plt.subplots_adjust(wspace=0.2)  # Increase the spacing between subplots

# Show the combined plot
plt.show()











# Adjust labels with a fixed flat offset for all points
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

# Scatter plot: Weighted vs Unweighted
axs[0].scatter(df_concentration['weighted'], df_concentration['unweighted'], color='blue', alpha=0.7, label='Countries', marker='x')
axs[0].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with a flat offset
labels = {'CHN': 'China', 'USA': 'USA', 'IND': 'India', 'QAT': 'Qatar', 'NGA': 'Nigeria', 'BRA': 'Brazil', 'ZAF': 'South Africa'}
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[0].annotate(
            labels[row['country']],
            (row['weighted'], row['unweighted']),
            textcoords="offset points",
            xytext=(50, 5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='black', lw=0.8)
        )

axs[0].set_xlabel('Population weighted', fontsize=12)
axs[0].set_ylabel('Unweighted (average)', fontsize=12)
axs[0].set_title('Weighted vs Unweighted', fontsize=14)
axs[0].legend()
axs[0].grid(True, linestyle='--', alpha=0.5)

# Scatter plot: Weighted vs World Bank
axs[1].scatter(df_concentration['weighted'], df_concentration['world_bank'], color='green', alpha=0.7, label='Countries', marker='x')
axs[1].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with a flat offset
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[1].annotate(
            labels[row['country']],
            (row['weighted'], row['world_bank']),
            textcoords="offset points",
            xytext=(15, 15),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='black', lw=0.8)
        )

axs[1].set_xlabel('Population weighted', fontsize=12)
axs[1].set_ylabel('World Bank estimate', fontsize=12)
axs[1].set_title('Weighted vs World Bank', fontsize=14)
axs[1].grid(True, linestyle='--', alpha=0.5)

# Add spacing between subplots
plt.subplots_adjust(wspace=0.3)  # Increase the spacing between subplots

# Show the combined plot
plt.show()




# Adjust labels with a fixed flat offset and ensure consistency across plots
fig, axs = plt.subplots(1, 2, figsize=(16, 8))


# Scatter plot: Weighted vs Unweighted
axs[0].scatter(df_concentration['weighted'], df_concentration['unweighted'], color='blue', alpha=0.7, label='Countries', marker='x')
axs[0].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with a flat offset
labels = {'CHN': 'China', 'USA': 'USA', 'IND': 'India', 'QAT': 'Qatar', 'NGA': 'Nigeria', 'BRA': 'Brazil', 'ZAF': 'South Africa'}
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[0].annotate(
            labels[row['country']],
            (row['weighted'], row['unweighted']),
            textcoords="offset points",
            xytext=(50, 5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='darkgrey', lw=0.8)
        )

axs[0].set_xlabel('Population weighted', fontsize=12)
axs[0].set_ylabel('Unweighted (average)', fontsize=12)
axs[0].set_title('Weighted vs Unweighted', fontsize=14)
axs[0].legend(color = 'darkgrey')
axs[0].grid(True, linestyle='--', alpha=0.5)

# Scatter plot: Weighted vs World Bank
axs[1].scatter(df_concentration['weighted'], df_concentration['world_bank'], color='green', alpha=0.7, label='Countries', marker='x')
axs[1].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with the same offset and style
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[1].annotate(
            labels[row['country']],
            (row['weighted'], row['world_bank']),
            textcoords="offset points",
            xytext=(50, 5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='darkgrey', lw=0.8)
        )

axs[1].set_xlabel('Population weighted', fontsize=12)
axs[1].set_ylabel('World Bank estimate', fontsize=12)
axs[1].set_title('Weighted vs World Bank', fontsize=14)
axs[1].grid(True, linestyle='--', alpha=0.5)

# Add spacing between subplots
plt.subplots_adjust(wspace=0.3)  # Increase the spacing between subplots

# Show the combined plot
plt.show()










# Adjust labels with consistent color and legend styling
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

# Scatter plot: Weighted vs Unweighted
axs[0].scatter(df_concentration['weighted'], df_concentration['unweighted'], color='blue', alpha=0.7, label='Countries', marker='x')
axs[0].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with a flat offset
labels = {'CHN': 'China', 'USA': 'USA', 'IND': 'India', 'QAT': 'Qatar', 'NGA': 'Nigeria', 'BRA': 'Brazil', 'ZAF': 'South Africa'}
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[0].annotate(
            labels[row['country']],
            (row['weighted'], row['unweighted']),
            textcoords="offset points",
            xytext=(40, 2.5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='darkgrey', lw=0.8)
        )

axs[0].set_xlabel('Population weighted', fontsize=12)
axs[0].set_ylabel('Unweighted (average)', fontsize=12)
axs[0].set_title('Population weighted vs Unweighted', fontsize=14)
axs[0].legend()
axs[0].grid(True, linestyle='--', alpha=0.5)

# Scatter plot: Weighted vs World Bank
axs[1].scatter(df_concentration['weighted'], df_concentration['world_bank'], color='green', alpha=0.7, label='Countries', marker='x')
axs[1].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with the same offset and style
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[1].annotate(
            labels[row['country']],
            (row['weighted'], row['world_bank']),
            textcoords="offset points",
            xytext=(40, 2.5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='darkgrey', lw=0.8)
        )

axs[1].set_xlabel('Population weighted', fontsize=12)
axs[1].set_ylabel('World Bank estimate (2020)', fontsize=12)
axs[1].set_title('Population weighted vs World Bank', fontsize=14)
axs[1].grid(True, linestyle='--', alpha=0.5)

# Add spacing between subplots
plt.subplots_adjust(wspace=0.3)  # Increase the spacing between subplots

# Show the combined plot
plt.show()







# Adjust labels with consistent color and legend styling, changing legend marker color to black
fig, axs = plt.subplots(1, 2, figsize=(16, 8))

# Scatter plot: Weighted vs Unweighted
scatter_0 = axs[0].scatter(df_concentration['weighted'], df_concentration['unweighted'], color='blue', alpha=0.7, label='Countries', marker='x')  # Keep graph color blue
axs[0].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with a flat offset
labels = {'CHN': 'China', 'USA': 'USA', 'IND': 'India', 'QAT': 'Qatar', 'NGA': 'Nigeria', 'BRA': 'Brazil', 'ZAF': 'South Africa'}
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[0].annotate(
            labels[row['country']],
            (row['weighted'], row['unweighted']),
            textcoords="offset points",
            xytext=(40, 2.5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='darkgrey', lw=0.8)
        )

axs[0].set_xlabel('Population weighted', fontsize=12)
axs[0].set_ylabel('Unweighted (average)', fontsize=12)
axs[0].set_title('Population weighted vs Unweighted', fontsize=14)
axs[0].legend(handles=[
    plt.Line2D([0], [0], color='black', marker='x', linestyle='', label='Countries'),  # Legend marker color black
    plt.Line2D([0], [0], color='red', linestyle='--', label='45° Line')
], loc='best')
axs[0].grid(True, linestyle='--', alpha=0.5)

# Scatter plot: Weighted vs World Bank
scatter_1 = axs[1].scatter(df_concentration['weighted'], df_concentration['world_bank'], color='green', alpha=0.7, label='Countries', marker='x')  # Keep graph color green
axs[1].plot([df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            [df_concentration['weighted'].min(), df_concentration['weighted'].max()],
            color='red', linestyle='--', label='45° Line')

# Label specific countries with the same offset and style
for _, row in df_concentration.iterrows():
    if row['country'] in labels:
        axs[1].annotate(
            labels[row['country']],
            (row['weighted'], row['world_bank']),
            textcoords="offset points",
            xytext=(40, 2.5),  # Fixed offset for all points
            ha='center',
            arrowprops=dict(arrowstyle='-', color='darkgrey', lw=0.8)
        )

axs[1].set_xlabel('Population weighted', fontsize=12)
axs[1].set_ylabel('World Bank estimate', fontsize=12)
axs[1].set_title('Population weighted vs World Bank', fontsize=14)
axs[1].grid(True, linestyle='--', alpha=0.5)

# Add spacing between subplots
plt.subplots_adjust(wspace=0.3)  # Increase the spacing between subplots

# Show the combined plot
plt.show()

