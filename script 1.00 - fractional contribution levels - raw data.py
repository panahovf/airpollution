# In[]:
# Date: Sep 26, 2024
# Project: Identify grid level fractional contribution levels --- Raw data --- grouped to 2 decimal places
# Author: Farhad Panahov

# description:

# Steps: Get grid level 'fractional contribution source' from each type of fossil fuels. 
#   Here is the source: https://zenodo.org/records/4739100
#   Files: Lon&Lat, ENEcoal, ENEother
#   Use: ENEcoal is used for power sector coal emissions, and ENEother is used for power sector oil & gas emissions





# In[]:
# load packages

import numpy as np
import pandas as pd
import time
import os





# In[]:
# directory

directory = r'C:\Users\panah\OneDrive\Desktop\Work\300 - Air pollution'
os.chdir(directory)
del directory





# In[]: LOAD AND EDIT ALL DATASETS
#####################################################

# This section opens each file in chunks first. Then limits decimal places to 2 decimals only.
# This helps with the size of the file. Also downstream data is also provided at 2 decimals.

# File paths
file_lonlat = '1 - input/1 - fractional contribution/GBD-MAPS_Gridded_Fractional_Contributions_LatLon.csv'
file_enecoal = '1 - input/1 - fractional contribution/GBD-MAPS_Gridded_Fractional_Contributions_ENEcoal.csv'
file_eneother = '1 - input/1 - fractional contribution/GBD-MAPS_Gridded_Fractional_Contributions_ENEother.csv'


# Define the chunk size
chunk_size = 100_000  # Adjust based on available memory


# Initialize an empty DataFrame for the overall aggregation
df_overall = pd.DataFrame(columns=['Lon', 'Lat', 'ENEcoal', 'ENEother'])


# List to accumulate chunks before aggregation
df_chunks_combined = []


# Set the batch size for grouping
batch_size = 500


# Process files in chunks
chunk_num = 1


for chunk_lonlat, chunk_enecoal, chunk_eneother in zip(
    pd.read_csv(file_lonlat, chunksize=chunk_size),
    pd.read_csv(file_enecoal, chunksize=chunk_size),
    pd.read_csv(file_eneother, chunksize=chunk_size)
):
    # Step 1: Combine columns into a single DataFrame
    combined_chunk = chunk_lonlat.copy()
    combined_chunk['ENEcoal'] = chunk_enecoal['ENEcoal']
    combined_chunk['ENEother'] = chunk_eneother['ENEother']
    
    # Step 2: Enforce the format for Lon/Lat columns
    combined_chunk['Lon'] = ((combined_chunk['Lon'] - 0.05) / 0.1).round(0) * 0.1 + 0.05
    combined_chunk['Lat'] = ((combined_chunk['Lat'] - 0.05) / 0.1).round(0) * 0.1 + 0.05
    
    # Step 3: Apply transformation to Lon and Lat (round to 2 decimal places)
    combined_chunk['Lon'] = (combined_chunk['Lon'] * 100).round() / 100
    combined_chunk['Lat'] = (combined_chunk['Lat'] * 100).round() / 100
        
    # Step 4: Group by Lon and Lat within this chunk and calculate the mean
    chunk_grouped = combined_chunk.groupby(['Lon', 'Lat'], as_index=False).agg({
        'ENEcoal': 'mean',
        'ENEother': 'mean'
    })
    
    # Step 5: Accumulate the chunk
    df_chunks_combined.append(chunk_grouped)
    
    # Step 6: Every `batch_size` chunks, concatenate and group
    if chunk_num % batch_size == 0:
        # Concatenate accumulated chunks
        batch_df = pd.concat(df_chunks_combined)
        
        # Group by Lon and Lat for the accumulated batch
        df_overall = pd.concat([df_overall, batch_df]).groupby(['Lon', 'Lat'], as_index=False).agg({
            'ENEcoal': 'mean',
            'ENEother': 'mean'
        })
        
        # Clear the accumulated chunks list
        df_chunks_combined = []
        
        # Print progress
        print(f"Processed chunk {chunk_num}")

        
    # Increment the chunk counter
    chunk_num += 1


# print
print(chunk_num)
# 6481


# Step 7: Process any remaining accumulated chunks
if df_chunks_combined:
    batch_df = pd.concat(df_chunks_combined)
    df_overall = pd.concat([df_overall, batch_df]).groupby(['Lon', 'Lat'], as_index=False).agg({
        'ENEcoal': 'mean',
        'ENEother': 'mean'
    })


# delete extras
del batch_df, chunk_enecoal, chunk_eneother, chunk_lonlat, chunk_grouped, combined_chunk, 
del batch_size, chunk_size
del file_enecoal, file_eneother, file_lonlat
del df_chunks_combined


# Print the first 10 rows of the final DataFrame
print(df_overall.head(10))
print(df_overall['Lon'].min())
print(df_overall['Lon'].max())
print(df_overall['Lat'].min())
print(df_overall['Lat'].max())
print(df_overall.describe())

#       Lon    Lat  ENEcoal  ENEother
# 0 -179.95 -89.95      NaN       NaN
# 1 -179.95 -89.85      NaN       NaN
# 2 -179.95 -89.75      NaN       NaN
# 3 -179.95 -89.65      NaN       NaN
# 4 -179.95 -89.55      NaN       NaN
# 5 -179.95 -89.45 -0.00144   -0.0039
# 6 -179.95 -89.35 -0.00144   -0.0039
# 7 -179.95 -89.25 -0.00144   -0.0039
# 8 -179.95 -89.15 -0.00144   -0.0039
# 9 -179.95 -89.05 -0.00144   -0.0039

# -179.95
# 179.95000000000002
# -89.95
# 90.05

#     Lon           Lat       ENEcoal      ENEother
# count  6.483600e+06  6.483600e+06  6.399250e+06  6.399250e+06
# mean   1.872743e-14  5.000000e-02  1.493917e-02  2.068645e-02
# std    1.039231e+02  5.199039e+01  2.507612e-02  3.009630e-02
# min   -1.799500e+02 -8.995000e+01 -1.190000e-02 -6.806000e-02
# 25%   -8.997500e+01 -4.495000e+01  4.200000e-04  1.050000e-03
# 50%    0.000000e+00  5.000000e-02  3.930000e-03  5.746000e-03
# 75%    8.997500e+01  4.505000e+01  2.069200e-02  3.192600e-02
# max    1.799500e+02  9.005000e+01  3.965800e-01  4.018900e-01


# Remove #NAs
df_overall = df_overall.dropna()










# In[]: EXPORT
#####################################################

# Save the final aggregated DataFrame to a CSV file
df_overall.to_csv('2 - output/script 1/s1.00 - 1 - frac dist - global.csv', index=False)



    


