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
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec  # <-- Import gridspec here
import scienceplots  # This registers the styles
from matplotlib.lines import Line2D










# In[]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# load concentration estimates
df_concentration_nz = pd.read_excel('2 - output/script 4/s4.00 - 2.2 - annual concentration - country level - net zero 1.5C - pw.xlsx')
df_concentration_cp = pd.read_excel('2 - output/script 4/s4.00 - 2.1 - annual concentration - country level - current policy - pw.xlsx')

# load full shutdown scenario
df_concentration_max = pd.read_excel('2 - output/script 4/s4.00 - 4.1 - max shutdown results - weighted and unweighted.xlsx')

# load mortality rates
df_mortality_nz = pd.read_excel('2 - output/script 5/s5.10 - 2 - annual mortality by country - nz 1.5c.xlsx')
df_mortality_cp = pd.read_excel('2 - output/script 5/s5.10 - 1 - annual mortality by country - current policy.xlsx')

# load VSL
df_vsl = pd.read_excel('1 - input/8 - econ data/1-Age-adjusted and age-invariant VSL.xlsx', skiprows = 3)

# load VSL
df_gdppercapita = pd.read_excel('1 - input/8 - econ data/API_NY.GDP.PCAP.PP.KD_DS2_en_excel_v2_316.xlsx', sheet_name='Data', skiprows = 3)

# load benefits
df_benefits = pd.read_excel('2 - output/script 6/s6.00_- 1 - annual economic benefits.xlsx')






# In[] EDIT DATA

# select countries
labels = {'IND': 'India', 'IDN': 'Indonesia', 'ZAF': 'South Africa', 'MEX': 'Mexico',
          'VNM': 'Viet Nam', 'IRN': 'Iran', 'THA': 'Thailand', 'EGY': 'Egypt',
          'USA': 'United States', 'CHN': 'China', 'QTR':'Qatar', 'NGA':'Nigeria',
          'TUR':'Türkiye', 'BRA':'Brazil', 'DEU':'Germany', 'SAU': 'Saudi Arabia'}

# create master file file --- picked concentratin max as starting point
df_master = df_concentration_max.loc[df_concentration_max['Country'].isin(labels),['Country','max_shutdown_pw','2024']]

# add nz and cp 2030,2035,2050
df_master = pd.merge(df_master, df_concentration_nz[['Country','2030', '2035','2050']], on='Country', how='inner')
df_master = pd.merge(df_master, df_concentration_cp[['Country','2030', '2035','2050']], on='Country', how='inner')

df_master.columns = ['country', 'shutdown','currentlevel', '2030nz', '2035nz', '2050nz', '2030cp', '2035cp', '2050cp'] # rename columns


# add mortality annual
df_mortality_annual = (df_benefits.loc[df_benefits['Year'].isin([2030, 2035, 2050]), 
                                        ['Country', 'Year', 'mortality_diff_annual']]
                    .pivot(index='Country', columns='Year', values='mortality_diff_annual')
                    .reset_index())
df_mortality_annual.columns = ['country', 'avoideddeathannual_2030', 'avoideddeathannual_2035', 'avoideddeathannual_2050']

df_master = pd.merge(df_master, df_mortality_annual, on='country',how='inner')


# add cumulative mortality
df_avoideddeath = (df_benefits.loc[df_benefits['Year'].isin([2030, 2035, 2050]), 
                                        ['Country', 'Year', 'mortality_diff_cumulative']]
                    .pivot(index='Country', columns='Year', values='mortality_diff_cumulative')
                    .reset_index())
df_avoideddeath.columns = ['country', 'avoideddeathcum_2030', 'avoideddeathcum_2035', 'avoideddeathcum_2050']

df_master = pd.merge(df_master, df_avoideddeath,on='country',how='inner')


# add VSL
df_vsl = df_vsl.groupby('Country - iso3c')['Age-invariant VSL-Mean'].mean().reset_index().rename(columns={'Country - iso3c': 'country','Age-invariant VSL-Mean': 'vsl'})
df_master = pd.merge(df_master, df_vsl[['country', 'vsl']], on='country', how='inner')

# add GDP per capita
df_gdppercapita = df_gdppercapita.rename(columns = {'Country Code': 'country', '2023': 'gdppercapita'})
df_master = pd.merge(df_master, df_gdppercapita[['country','gdppercapita']], on='country', how = 'inner')


# add benefits
df_benefits = (df_benefits.loc[df_benefits['Year'].isin([2030, 2035, 2050]), 
                                        ['Country', 'Year', 'econ_benefit_discounted_cumulative_(mln $2019)' ]]
                    .pivot(index='Country', columns='Year', values='econ_benefit_discounted_cumulative_(mln $2019)')
                    .reset_index())
df_benefits.columns = ['country', 'benefit_2030', 'benefit_2035', 'benefit_2050']

df_master = pd.merge(df_master, df_benefits,on='country',how='inner')





# SORT BY 2024 concentration level
df_master = df_master.sort_values(by='currentlevel', ascending=True)

# name contries
df_master['country'] = df_master['country'].map(labels)



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

# --- Assume df_master is your DataFrame with the required columns ---
# Required columns for this example:
# For Plot 1: 'country', 'shutdown', 'currentlevel', 
#             '2030nz', '2035nz', '2050nz', '2030cp', '2035cp', '2050cp'
# For Plot 2: 'avoideddeathannual_2030', 'avoideddeathannual_2035', 'avoideddeathannual_2050',
#             'avoideddeathcum_2030', 'avoideddeathcum_2035', 'avoideddeathcum_2050'
# For Plot 3 & Plot 4, placeholders are provided.

# Get the list of countries (assumed to be in the desired order)
countries = df_master['country'].tolist()
n_countries = len(countries)
y_pos = np.arange(n_countries)

# Define a colors array for Plot 2 markers (for three years)
colors = cm.viridis_r(np.linspace(0, 1, 6))

plot2_colors = ['grey', 'blue', 'brown']
years_labels = ['2030', '2035', '2050']

#############################################
# Create figure with a 2x2 grid of subplots
#############################################
fig, axs = plt.subplots(2, 2, figsize=(12, 8))


#############################################
# TOP-LEFT: Plot 1 (Economic Measures)
#############################################
ax1 = axs[0, 0]

# Plot 'currentlevel' as an X marker (black)
ax1.scatter(df_master['currentlevel'].values, y_pos,
            marker='x', color='black', s=75, label='Current level')

# Plot 'shutdown' as an X marker (green)
ax1.scatter(df_master['shutdown'].values, y_pos,
            marker='x', color='lime', s=75, label='Global fossil fuel shutdown')

# --- Mapping for 2035/2050 Data --- #
# Now we assign:
#   - Marker shape to indicate the year:
#         2035 → circle ('o')
#         2050 → square ('s')
#   - Marker color to indicate the scenario:
#         Carbon budget consistent net zero ('nz') → green
#         Current policies ('cp') → dark orange

# Define the mapping dictionaries:
year_marker  = {'2030': '*','2035': 'd', '2050': 's'}           # marker shape by year
scenario_color = {'nz': 'forestgreen', 'cp': 'purple'}  # marker color by scenario

# Loop over scenarios and years; we assume dataframe columns are named as "2035nz", "2050nz", "2035cp", "2050cp".
for scenario in ['nz', 'cp']:
    for year in ['2030','2035', '2050']:
        col = f"{year}{scenario}"
        ax1.scatter(df_master[col].values, y_pos,
                    marker=year_marker[year],
                    color=scenario_color[scenario],
                    s=15)

# Set y-axis ticks and labels.
ax1.set_yticks(y_pos)
ax1.set_yticklabels(countries, fontsize=11)
ax1.minorticks_off()

ax1.set_title('PM2.5 concentration levels (μg/m3, weighted)', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.5)

# --- Build a Combined Legend ---
# We want a single legend that includes:
#   1. The "Current level" and "Global fossil fuel shutdown" markers.
#   2. A dummy legend for year (marker shape) mapping.
#   3. A dummy legend for scenario (marker color) mapping.

legend_handles = [
    # Already plotted items:
    Line2D([0], [0], marker='x', color='black', linestyle='None', markersize=6, label='Current level'),
    Line2D([0], [0], marker='x', color='lime', linestyle='None', markersize=6, label='Global power sector fossil fuel shut down'),
    
    # Year legend (marker shape indicates year)
    Line2D([0], [0], marker=year_marker['2030'], color='grey', linestyle='None', markersize=5,
           label='Shape: 2030'),
    Line2D([0], [0], marker=year_marker['2035'], color='grey', linestyle='None', markersize=5,
           label='Shape: 2035'),
    Line2D([0], [0], marker=year_marker['2050'], color='grey', linestyle='None', markersize=5,
           label='Shape: 2050'),
    
    # Scenario legend (marker color indicates scenario)
    Line2D([0], [0], marker='o', color=scenario_color['nz'], linestyle='None', markersize=5,
           label='Color: Carbon budget consistent net zero'),
    Line2D([0], [0], marker='o', color=scenario_color['cp'], linestyle='None', markersize=5,
           label='Color: Current policies')
]

ax1.legend(handles=legend_handles, fontsize=8, loc='lower right')


#############################################
# TOP-RIGHT: Plot 2 (Avoided Mortalities)
# Here we split the top-right cell horizontally into 2 subplots
#############################################
ax2 = axs[0, 1]

ax2.tick_params(labelleft=False)
ax2.tick_params(labelbottom=False)
ax2.minorticks_off()

for spine in ax2.spines.values():
    spine.set_visible(False)

gs_top_right = axs[0, 1].get_subplotspec()
subgs = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs_top_right, wspace=0.1)
ax2a = fig.add_subplot(subgs[0])  # Left subplot: Annual avoided mortality (log-transformed)
ax2b = fig.add_subplot(subgs[1])  # Right subplot: Cumulative avoided mortality (log-transformed)

# Plot 2a: Annual avoided mortalities (log-transformed)
annual_cols = ['avoideddeathannual_2030', 'avoideddeathannual_2035', 'avoideddeathannual_2050']
for j, col in enumerate(annual_cols):
    ax2a.scatter(np.log10(df_master[col].values), y_pos,
                 marker='o', color=plot2_colors[j], s=10, label=years_labels[j])

ax2a.tick_params(labelleft=False)  # Hide y tick labels (to avoid clutter)
ax2a.grid(True, linestyle='--', alpha=0.5)
ax2a.legend(fontsize=8, loc='lower left', title='Annual')

ax2a.tick_params(labelleft=False)
ax2a.minorticks_off()

# Plot 2b: Cumulative avoided mortalities (log-transformed)
cum_cols = ['avoideddeathcum_2030', 'avoideddeathcum_2035', 'avoideddeathcum_2050']
for j, col in enumerate(cum_cols):
    ax2b.scatter(np.log10(df_master[col].values), y_pos,
                 marker='x', color=plot2_colors[j], s=10, label=years_labels[j])

ax2b.tick_params(labelleft=False)
ax2b.grid(True, linestyle='--', alpha=0.5)
ax2b.legend(fontsize=8, loc='lower left', title='Cumulative')

ax2b.tick_params(labelleft=False)
ax2b.minorticks_off()

ax2.set_title('Avoided death (persons, log scale)', fontsize=14)




#############################################
# BOTTOM-RIGHT: Plot 3 (VSL vs GDP per Capita)
# Replace this placeholder with your actual Plot 4 code if needed.
#############################################
ax3 = axs[1, 0]
# Get a normalized marker size based on gdppercapita
gdp_min = df_master['gdppercapita'].min()
gdp_max = df_master['gdppercapita'].max()
scale_factor = 300  # This factor determines the range of marker sizes
base_size = 50      # This is the minimum marker size


for i, (_, row) in enumerate(df_master.iterrows()):
    y = y_pos[i]
    vsl_val = row['vsl']
    gdp = row['gdppercapita']
    # Normalize the GDP value between 0 and 1:
    norm_size = (gdp - gdp_min) / (gdp_max - gdp_min)
    # Compute marker size:
    marker_size = base_size + norm_size * scale_factor
    ax3.scatter(vsl_val, y, marker='o', color='pink', s=marker_size, edgecolor='k')

ax3.set_yticks(y_pos)
ax3.set_yticklabels(countries, fontsize=11)
ax3.minorticks_off()

ax3.set_title('VSL (thousands US$)', fontsize=14)
ax3.grid(True, linestyle='--', alpha=0.5)

def thousands_formatter(x, pos):
    # x is the value on the axis (in thousands), so multiply by 1000.
    return '{:,.0f}'.format(x/1000)

ax3.xaxis.set_major_formatter(FuncFormatter(thousands_formatter))

ax3.legend(fontsize=10, loc='upper center', title='Bubble size = GDP per capita \n(based on purchasing power parity)')







#############################################
# BOTTOM-LEFT: Plot 4 (Avoided Deaths Stacked)
# Replace this placeholder with your actual Plot 3 code if needed.
# #############################################
ax4 = axs[1, 1]
for i, (_, row) in enumerate(df_master.iterrows()):
    y = y_pos[i]
    base = row['benefit_2030']
    diff1 = row['benefit_2035'] - row['benefit_2030']
    diff2 = row['benefit_2050'] - row['benefit_2035']
    ax4.barh(y, base, color='skyblue', edgecolor='k', label='2030' if i==0 else "")
    ax4.barh(y, diff1, left=base, color='deepskyblue', edgecolor='k', label='2035' if i==0 else "")
    ax4.barh(y, diff2, left=base+diff1, color='dodgerblue', edgecolor='k', label='2050' if i==0 else "")
ax4.set_yticks(y_pos)
ax4.set_yticklabels(countries, fontsize=11)
ax4.set_title('Cumulative economic benefits (billions US$)', fontsize=14)
handles3, labels3 = ax3.get_legend_handles_labels()
by_label3 = dict(zip(labels3, handles3))

ax4.tick_params(labelleft=False)
ax4.minorticks_off()

def thousands_formatter(x, pos):
    # x is the value on the axis (in thousands), so multiply by 1000.
    return '{:,.0f}'.format(x/1000)

ax4.xaxis.set_major_formatter(FuncFormatter(thousands_formatter))


ax4.legend(fontsize=10, loc='lower right')
ax4.grid(True, linestyle='--', alpha=0.5)



#############################################
# Final adjustments and display
#############################################
fig.tight_layout()
fig.savefig('hero graph.png', dpi=1200, bbox_inches='tight')
plt.show()
