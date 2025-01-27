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
import seaborn as sns







# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory


# --------------
# LOAD CONCENTRATION DATA
df_concentration_cp = pd.read_excel('2 - output/script 4/s4.00 - 2.1 - annual concentration - country level - current policy - pw.xlsx')
df_concentration_nz = pd.read_excel('2 - output/script 4/s4.00 - 2.2 - annual concentration - country level - net zero 1.5C - pw.xlsx')


# Convert wide-format concentration data to long format
df_concentration_cp = df_concentration_cp.melt(
    id_vars=['Country'], 
    var_name='Year', 
    value_name='concentration'
)

df_concentration_nz = df_concentration_nz.melt(
    id_vars=['Country'], 
    var_name='Year', 
    value_name='concentration'
)

df_concentration_cp['Year'] = df_concentration_cp['Year'].astype(int) # set years as integers
df_concentration_nz['Year'] = df_concentration_nz['Year'].astype(int)



# --------------
# LOAD EXPOSURE RESPONSE FUNCTIONS
df_response_ihd = pd.read_csv('1 - input/5 - response functions/pm desease - cvd_ihd.csv')
df_response_stroke = pd.read_csv('1 - input/5 - response functions/pm desease - cvd_stroke.csv')
df_response_lri = pd.read_csv('1 - input/5 - response functions/pm desease - lri.csv')
df_response_lung = pd.read_csv('1 - input/5 - response functions/pm desease - neo_lung.csv')
df_response_copd = pd.read_csv('1 - input/5 - response functions/pm desease - resp_copd.csv')
df_response_t2d = pd.read_csv('1 - input/5 - response functions/pm desease - t2_dm.csv')


# --------------
# MORTALITY RATES
# https://vizhub.healthdata.org/gbd-results/
# stroke; tracjeal,bronchus, and lung cancer; diabetes melittus type 2; ischemic heart disease; lower respiratory infections; chronic obstructive pulmonary disease
# death per 100K
df_mortality = pd.read_excel('2 - output/script 5/s5.00 - 1 - mortality rate - country iso3.xlsx')


# --------------
# POPULATION PROJECTION
# world bank: https://databank.worldbank.org/source/population-estimates-and-projections#
df_pop_project = pd.read_excel('1 - input/4 - population/wb - population project - by country.xlsx')





# --------------
# set year & scenarios
year_columns = [str(year) for year in range(2024, 2051)]
scenarios = ["cp", "nz",]


# In[4]: SET ANNUAL FUNCTION RESUTLS
#####################################


# round concentration dataframes
df_concentration_cp['concentration'] = df_concentration_cp['concentration'].round(4)
df_concentration_nz['concentration'] = df_concentration_nz['concentration'].round(4)



# --------------
# iternpolate the response function to 4 decimals to match the concentration levels
# STEP 1
dataframes = [df_response_ihd, df_response_stroke, df_response_lri, df_response_lung, df_response_copd, df_response_t2d]

# Loop to interpolate each dataframe
for i, df in enumerate(dataframes):
    # Define the new exposure range with 0.0001 steps
    new_exposure = np.arange(0, 500.0001, 0.0001)
    new_exposure = np.round(np.arange(0, 500.0001, 0.0001), 4)

    # Perform interpolation
    interpolated_data = pd.DataFrame({
        'exposure': new_exposure,
        'mean': np.interp(new_exposure, df['exposure'], df['mean']),
        'lower': np.interp(new_exposure, df['exposure'], df['lower']),
        'upper': np.interp(new_exposure, df['exposure'], df['upper']),
    })
        
    # Replace the original dataframe with the interpolated one
    dataframes[i] = interpolated_data

# Assign back the interpolated dataframes
df_response_ihd, df_response_stroke, df_response_lri, df_response_lung, df_response_copd, df_response_t2d = dataframes

del i, df, dataframes, interpolated_data, new_exposure



                                                       
# --------------
# create response functions to each desease
### CP
df_annual_response_cp_total = df_concentration_cp.copy()


# df_annual_response_cp_total
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_ihd[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_copd[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_lri[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')

df_annual_response_cp_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)   ### this step just renames columns, otherwise you get an error
df_annual_response_cp_total.rename(columns={'upper_x': 'ihd', 'upper_y': 'copd', 'upper': 'lri'}, inplace=True)


df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_lung[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_stroke[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_cp_total = pd.merge(df_annual_response_cp_total, df_response_t2d[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')

df_annual_response_cp_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_cp_total.rename(columns={'upper_x': 'lung', 'upper_y': 'stroke', 'upper': 't2d'}, inplace=True)




### NZ
df_annual_response_nz_total = df_concentration_nz.copy()


# df_annual_response_cp_total
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_ihd[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_copd[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_lri[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')

df_annual_response_nz_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)   ### this step just renames columns, otherwise you get an error
df_annual_response_nz_total.rename(columns={'upper_x': 'ihd', 'upper_y': 'copd', 'upper': 'lri'}, inplace=True)


df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_lung[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_stroke[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')
df_annual_response_nz_total = pd.merge(df_annual_response_nz_total, df_response_t2d[['exposure', 'upper']], left_on='concentration', right_on='exposure', how='left')

df_annual_response_nz_total.drop(columns=['exposure', 'exposure_x', 'exposure_y'], inplace=True)
df_annual_response_nz_total.rename(columns={'upper_x': 'lung', 'upper_y': 'stroke', 'upper': 't2d'}, inplace=True)



# delete
del df_concentration_cp, df_concentration_nz
del df_response_copd, df_response_ihd, df_response_lri, df_response_lung, df_response_stroke, df_response_t2d









# In[4]: ESTIMATE SHARE OF DEATH BY DISEASE
#####################################

# --------------
# get growth rates in attibution to disease based on response function
# (R(C) - 1)/R(C)
list_of_columns = df_annual_response_cp_total.columns.drop(['Country', 'Year','concentration']).tolist()


# --------------
### CP
df_attirubtion_cp = df_annual_response_cp_total.copy()
df_attirubtion_cp[list_of_columns] = (df_attirubtion_cp[list_of_columns] - 1)/df_attirubtion_cp[list_of_columns]


### NZ
df_attirubtion_nz = df_annual_response_nz_total.copy()
df_attirubtion_nz[list_of_columns] = (df_attirubtion_nz[list_of_columns] - 1)/df_attirubtion_nz[list_of_columns]





# BOTH
# get mortality rates by year
# List of diseases and their corresponding column names
diseases = [
    ('Ischemic heart disease', 'ihd'),
    ('Lower respiratory infections', 'lri'),
    ('Chronic obstructive pulmonary disease', 'copd'),
    ('Tracheal, bronchus, and lung cancer', 'lung'),
    ('Stroke', 'stroke'),
    ('Diabetes mellitus type 2', 't2d')
]


# get list of countries
countries_ngfs = list(df_attirubtion_cp['Country'].unique())
countries_mortality = list(df_mortality['alpha-3'].unique())

# missing countries (countries in NGFS but not in Mortality)
missing = list(set(countries_ngfs) - set(countries_mortality))
print(missing)
#['HKG']
# there is only 1 country missing. leaving it out

# common countries
countries = list(set(countries_ngfs) & set(countries_mortality))


df_annual_mortalityrate_cp_total = df_attirubtion_cp.copy()
df_annual_mortalityrate_nz_total = df_attirubtion_nz.copy()

df_annual_mortalityrate_cp_total = df_annual_mortalityrate_cp_total[df_annual_mortalityrate_cp_total['Country'].isin(countries)]
df_annual_mortalityrate_nz_total = df_annual_mortalityrate_nz_total[df_annual_mortalityrate_nz_total['Country'].isin(countries)]


for country in countries:
    # Filter mortality data for the current country
    temp_mortality = df_mortality[df_mortality['alpha-3'] == country]
    
    # Iterate through each disease
    for disease, column in diseases:
        # Extract the initial value for the disease
        temp = temp_mortality.loc[temp_mortality['Cause'] == disease, 'Value'].values[0]
        
        # Update CP and NZ DataFrames
        df_annual_mortalityrate_cp_total.loc[df_annual_mortalityrate_cp_total['Country'] == country, column] =  temp * df_annual_mortalityrate_cp_total[column]
        df_annual_mortalityrate_nz_total.loc[df_annual_mortalityrate_nz_total['Country'] == country, column] =  temp * df_annual_mortalityrate_nz_total[column]






# In[4]: NOW GET ABSOLUTE NUMBER OF DEATH BY DISEASE
#####################################

# --------------
# Extract and clean population data
df_pop_cleaned = df_pop_project.copy()

# Keep only relevant columns (e.g., 'Country Code' and year columns)
year_columns = [col for col in df_pop_cleaned.columns if '[YR' in col]  # Extract year columns
df_pop_cleaned = df_pop_cleaned[['Country Code'] + year_columns]  # Keep 'Country Code' and year columns

# Rename year columns to clean format
df_pop_cleaned.columns = ['Country Code'] + [col.split()[0] for col in year_columns]  # Remove "[YR...]"

# Melt data for easier analysis
df_pop_cleaned = df_pop_cleaned.melt(id_vars='Country Code', var_name='Year', value_name='Population')

# Clean the 'Year' column
df_pop_cleaned['Year'] = df_pop_cleaned['Year'].astype(int)


# Add '100K population' column
df_pop_cleaned['Population'] = pd.to_numeric(df_pop_cleaned['Population'], errors='coerce')
df_pop_cleaned['100K population'] = df_pop_cleaned['Population'] / 100000


del df_pop_project






# --------------
# now get absolute death rates by year by disease
# create dataframes
df_annual_mortality_cp_total = df_annual_mortalityrate_cp_total.copy()
df_annual_mortality_nz_total = df_annual_mortalityrate_nz_total.copy()


# multiple death per 100K to population values (1ooK count)
df_annual_mortality_cp_total = pd.merge(
    df_annual_mortality_cp_total, 
    df_pop_cleaned[['Country Code', 'Year', '100K population']],
    left_on=['Country', 'Year'],  # Specify the keys from the left DataFrame
    right_on=['Country Code', 'Year'],  # Specify the keys from the right DataFrame
    how='left'  # Merge type
).drop(columns=['Country Code'])


df_annual_mortality_nz_total = pd.merge(
    df_annual_mortality_nz_total, 
    df_pop_cleaned[['Country Code', 'Year', '100K population']],
    left_on=['Country', 'Year'],  # Specify the keys from the left DataFrame
    right_on=['Country Code', 'Year'],  # Specify the keys from the right DataFrame
    how='left'  # Merge type
).drop(columns=['Country Code'])



diseases = ['ihd', 'copd', 'lri', 'lung', 'stroke', 't2d']

df_annual_mortality_cp_total['annual mortality'] = (
    df_annual_mortality_cp_total[diseases].multiply(df_annual_mortality_cp_total['100K population'], axis=0).sum(axis=1)
)

df_annual_mortality_nz_total['annual mortality'] = (
    df_annual_mortality_nz_total[diseases].multiply(df_annual_mortality_nz_total['100K population'], axis=0).sum(axis=1)
)



# --------------
# mortality without population growth
# current population estimate
population_2024 = df_pop_cleaned.loc[df_pop_cleaned['Year'] == 2024, ('Country Code','100K population')]
population_2024.rename(columns={'100K population': '100K population_nogrowth'}, inplace=True)

# multiple death per 100K to population values (1ooK count)
# multiple death per 100K to population values (1ooK count)
df_annual_mortality_cp_total = pd.merge(
    df_annual_mortality_cp_total, 
    population_2024[['Country Code', '100K population_nogrowth']],
    left_on=['Country'],  # Specify the keys from the left DataFrame
    right_on=['Country Code'],  # Specify the keys from the right DataFrame
    how='left'  # Merge type
).drop(columns=['Country Code'])


df_annual_mortality_nz_total = pd.merge(
    df_annual_mortality_nz_total, 
    population_2024[['Country Code', '100K population_nogrowth']],
    left_on=['Country'],  # Specify the keys from the left DataFrame
    right_on=['Country Code'],  # Specify the keys from the right DataFrame
    how='left'  # Merge type
).drop(columns=['Country Code'])


df_annual_mortality_cp_total['annual mortality nogrowth'] = (
    df_annual_mortality_cp_total[diseases].multiply(df_annual_mortality_cp_total['100K population_nogrowth'], axis=0).sum(axis=1)
)

df_annual_mortality_nz_total['annual mortality nogrowth'] = (
    df_annual_mortality_nz_total[diseases].multiply(df_annual_mortality_nz_total['100K population_nogrowth'], axis=0).sum(axis=1)
)





# In[]

# export data

# --------------
# mortality - annual result - no population growth
df_annual_mortality_cp_total.to_excel('2 - output/script 5/s5.30 - 1 - annual mortality by country - current policy - response upper.xlsx', index = False)
df_annual_mortality_nz_total.to_excel('2 - output/script 5/s5.30 - 2 - annual mortality by country - nz 1.5c - response upper.xlsx', index = False)









