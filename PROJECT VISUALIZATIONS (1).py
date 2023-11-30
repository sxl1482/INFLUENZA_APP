#!/usr/bin/env python
# coding: utf-8

# #                                        BAR CHARTS

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data_path =  r'C:\Users\priya\Downloads\VIW_FNT.csv'
df = pd.read_csv(data_path)

variant_columns = ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'AOTHER_SUBTYPE_DETAILS']
years = range(2018, 2024)


for variant in variant_columns:
    plt.figure(figsize=(10, 6))
    plt.title(f'{variant} Cases Over Time for the top 20 countries (2018-2023)')
    plt.xlabel('Year')
    plt.ylabel('Total Cases')
    
    variant_data = []
    
    for year in years:
        df_year = df[df['ISO_YEAR'] == year]
        grouped_data_year = df_year.groupby('COUNTRY_AREA_TERRITORY')[variant].sum().reset_index()
        sorted_data = grouped_data_year.sort_values(by=variant, ascending=False).head(20)
        
    
        variant_data.append(sorted_data[variant])
    
    variant_data = np.array(variant_data)
    
    for i, year in enumerate(years):
        plt.bar(sorted_data['COUNTRY_AREA_TERRITORY'], variant_data[i], label=f'Year {year}')

    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()


# #                                             PIE CHARTS

# In[49]:


import pandas as pd
import matplotlib.pyplot as plt
import math

# as usual loading the data
df = pd.read_csv("C:/Users/priya/Downloads/VIW_FNT.csv")

# converrting it to the datetime format so it will be easy to generate
df['ISO_WEEKSTARTDATE'] = pd.to_datetime(df['ISO_WEEKSTARTDATE'])

# Filtering  data for the years 2020 to 2023 as we wsnt in that time period
start_date = pd.to_datetime('2020-01-01')
end_date = pd.to_datetime('2023-12-31')
df_filtered = df[(df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date)]

# Select columns of interest
columns_of_interest = ['ILI_ACTIVITY', 'ADENO', 'BOCA', 'HUMAN_CORONA', 'METAPNEUMO', 'PARAINFLUENZA', 'RHINO', 'RSV', 'OTHERRESPVIRUS', 'OTHER_RESPVIRUS_DETAILS']

# Calculate the number of rows and columns needed for the grid layout
num_rows = math.ceil(len(columns_of_interest) / 2)
num_cols = 2

# Creating subplots with increased spacing between rows to make it more presentable while analyzing the data
fig, axes = plt.subplots(num_rows, num_cols, figsize=(16, 6 * num_rows))
fig.suptitle(' Respiratory Virus Variant Distribution by Continent (2020-2023)', fontsize=16, weight='bold')

# Flatten the axes array for easy iteration
axes = axes.ravel()

# Create pie charts
for i, column in enumerate(columns_of_interest):
    ax = axes[i]
    wedges, texts, autotexts = ax.pie(
        continent_data[column],
        labels=None,
        autopct='',
        startangle=140,
        textprops={'color': 'w', 'fontsize': 12, 'weight': 'bold'},
    )
    
    ax.set_title(f'{column}', fontsize=14, weight='bold')
    ax.axis('equal')
    
    # Calculate percentages
    total = sum(continent_data[column])
    percentages = [(val / total) * 100 for val in continent_data[column]]
    
    # Create legend labels with percentages
    legend_labels = [f"{continent_data['WHOREGION'].iloc[j]} - {percentages[j]:.1f}%" for j in range(len(continent_data))]
    
    # Add legend with custom labels
    ax.legend(legend_labels, title='Continent', loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 12, 'weight': 'bold'})
    
# Hide any remaining empty subplots
for i in range(len(columns_of_interest), num_rows * num_cols):
    fig.delaxes(axes[i])

# Adjust spacing
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.show()


# #                                       GEO VISUALIZATION

# In[1]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

geo_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
gdf = gpd.read_file(geo_url)

data_url = r"C:/Users/priya/Downloads/VIW_FNT.csv"
df = pd.read_csv(data_url)

df['ISO_YEAR'] = pd.to_numeric(df['ISO_YEAR'])
df = df[(df['ISO_YEAR'] >= 2010) & (df['ISO_YEAR'] <= 2023)]

df['TotalCases'] = df[['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE',
                       'AOTHER_SUBTYPE', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM',
                       'BNOTDETERMINED', 'INF_B']].sum(axis=1)

df['Percentage'] = (df['TotalCases'] / df['SPEC_PROCESSED_NB']) * 100

merged_data = gdf.merge(df, left_on='id', right_on='COUNTRY_CODE', how='left')

fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.axis('off')
ax.set_title('Flu Cases by Percentage (2010-2023)', fontsize=16)

cmap = plt.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=100)

merged_data.plot(column='Percentage', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, norm=norm, legend_kwds={'label': 'Percentage of Flu Cases (%)'})

plt.show()


# In[13]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

geo_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
gdf = gpd.read_file(geo_url)

data_url = r"C:/Users/priya/Downloads/VIW_FNT.csv"
df = pd.read_csv(data_url)


df['ISO_YEAR'] = pd.to_numeric(df['ISO_YEAR']) 
filtered_df = df[(df['ISO_YEAR'] >= 2010) & (df['ISO_YEAR'] <= 2023) &
                 (df['ISO_WEEKSTARTDATE'].str.slice(5, 7).astype(int).isin([12, 1, 2]))]


filtered_df['TotalCases'] = filtered_df[['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED',
                                         'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'BVIC_2DEL', 'BVIC_3DEL',
                                         'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B']].sum(axis=1)
filtered_df['Percentage'] = (filtered_df['TotalCases'] / filtered_df['SPEC_PROCESSED_NB']) * 100


merged_data = gdf.merge(filtered_df, left_on='id', right_on='COUNTRY_CODE', how='left')


fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.axis('off')  
ax.set_title('Flu Cases by Percentage (Dec to Feb 2010-2023)', fontsize=16)


cmap = plt.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=100)  # Set the normalization range to 0-100

merged_data.plot(column='Percentage', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, norm=norm, legend_kwds={'label': 'Percentage of Flu Cases (%)'})

plt.show()


# In[3]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

geo_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
gdf = gpd.read_file(geo_url)

data_url = r"C:/Users/priya/Downloads/VIW_FNT.csv"
df = pd.read_csv(data_url)

df['ISO_YEAR'] = pd.to_numeric(df['ISO_YEAR'])
filtered_df = df[(df['ISO_YEAR'] >= 2010) & (df['ISO_YEAR'] <= 2023) &
                 (df['ISO_WEEKSTARTDATE'].str.slice(5, 7).astype(int).isin([2, 4]))]

filtered_df['TotalCases'] = filtered_df[['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED',
                                         'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'BVIC_2DEL', 'BVIC_3DEL',
                                         'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B']].sum(axis=1)
filtered_df['Percentage'] = (filtered_df['TotalCases'] / filtered_df['SPEC_PROCESSED_NB']) * 100

merged_data = gdf.merge(filtered_df, left_on='id', right_on='COUNTRY_CODE', how='left')

fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.axis('off')
ax.set_title('Flu Cases by Percentage (Feb to April 2010-2023)', fontsize=16)

cmap = plt.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=100)

merged_data.plot(column='Percentage', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, norm=norm, legend_kwds={'label': 'Percentage of Flu Cases (%)'})

plt.show()


# In[5]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

geo_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
gdf = gpd.read_file(geo_url)

data_url = r"C:/Users/priya/Downloads/VIW_FNT.csv"
df = pd.read_csv(data_url)

df['ISO_YEAR'] = pd.to_numeric(df['ISO_YEAR'])
filtered_df = df[(df['ISO_YEAR'] >= 2010) & (df['ISO_YEAR'] <= 2023) &
                 (df['ISO_WEEKSTARTDATE'].str.slice(5, 7).astype(int).isin([4, 6]))]

filtered_df['TotalCases'] = filtered_df[['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED',
                                         'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'BVIC_2DEL', 'BVIC_3DEL',
                                         'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B']].sum(axis=1)
filtered_df['Percentage'] = (filtered_df['TotalCases'] / filtered_df['SPEC_PROCESSED_NB']) * 100

merged_data = gdf.merge(filtered_df, left_on='id', right_on='COUNTRY_CODE', how='left')

fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.axis('off')
ax.set_title('Flu Cases by Percentage (April to June 2010-2023)', fontsize=16)

cmap = plt.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=100)

merged_data.plot(column='Percentage', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, norm=norm, legend_kwds={'label': 'Percentage of Flu Cases (%)'})

plt.show()


# In[6]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

geo_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
gdf = gpd.read_file(geo_url)

data_url = r"C:/Users/priya/Downloads/VIW_FNT.csv"
df = pd.read_csv(data_url)

df['ISO_YEAR'] = pd.to_numeric(df['ISO_YEAR'])  
filtered_df = df[(df['ISO_YEAR'] >= 2010) & (df['ISO_YEAR'] <= 2023) &
                 (df['ISO_WEEKSTARTDATE'].str.slice(5, 7).astype(int).isin([6, 8]))]


filtered_df['TotalCases'] = filtered_df[['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED',
                                         'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'BVIC_2DEL', 'BVIC_3DEL',
                                         'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B']].sum(axis=1)
filtered_df['Percentage'] = (filtered_df['TotalCases'] / filtered_df['SPEC_PROCESSED_NB']) * 100


merged_data = gdf.merge(filtered_df, left_on='id', right_on='COUNTRY_CODE', how='left')

fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.axis('off') 
ax.set_title('Flu Cases by Percentage (june to august 2010-2023)', fontsize=16)

cmap = plt.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=100)  
merged_data.plot(column='Percentage', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, norm=norm, legend_kwds={'label': 'Percentage of Flu Cases (%)'})


plt.show()


# In[10]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

geo_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
gdf = gpd.read_file(geo_url)

data_url = r"C:/Users/priya/Downloads/VIW_FNT.csv"
df = pd.read_csv(data_url)

df['ISO_YEAR'] = pd.to_numeric(df['ISO_YEAR'])  
filtered_df = df[(df['ISO_YEAR'] >= 2010) & (df['ISO_YEAR'] <= 2023) &
                 (df['ISO_WEEKSTARTDATE'].str.slice(5, 7).astype(int).isin([8, 11]))]

filtered_df['TotalCases'] = filtered_df[['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED',
                                         'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE', 'BVIC_2DEL', 'BVIC_3DEL',
                                         'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED', 'INF_B']].sum(axis=1)
filtered_df['Percentage'] = (filtered_df['TotalCases'] / filtered_df['SPEC_PROCESSED_NB']) * 100

merged_data = gdf.merge(filtered_df, left_on='id', right_on='COUNTRY_CODE', how='left')


fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.axis('off')  
ax.set_title('Flu Cases by Percentage (august to november 2010-2023)', fontsize=16)


cmap = plt.get_cmap('YlOrRd')
norm = colors.Normalize(vmin=0, vmax=100)  


merged_data.plot(column='Percentage', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, norm=norm, legend_kwds={'label': 'Percentage of Flu Cases (%)'})


plt.show()


# #                                         TIME SERIES

# In[2]:


import pandas as PD
import plotly. express as px

df = pd.read_csv("C:/Users/priya/Downloads/VIW_FNT.csv")

df['ISO_WEEKSTARTDATE'] = pd.to_datetime(df['ISO_WEEKSTARTDATE'])

start_date = pd.to_datetime('2018-01-01')
end_date = pd.to_datetime('2023-12-31')
df_filtered = df[(df['ISO_WEEKSTARTDATE'] >= start_date) & (df['ISO_WEEKSTARTDATE'] <= end_date)]

variant_columns = ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE']
continent_column = 'WHOREGION'

time_series_data = df_filtered.groupby(['ISO_WEEKSTARTDATE', continent_column])[variant_columns].sum().reset_index()
fig = px.line(time_series_data, x='ISO_WEEKSTARTDATE', y=variant_columns, color=continent_column,
              labels={'ISO_WEEKSTARTDATE': 'Time', 'value': 'Count'},
              title='Influenza A, B,C Flu Virus Variants Over Time (2018-2023) by Continent',
              template='plotly_dark')
fig.show()


# In[ ]:




