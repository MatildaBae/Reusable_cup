#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from geoband.API import *
from tqdm import tqdm
import pandas as pd
import numpy as np
import geopandas as gpd
import seaborn as sns
import json
import random
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# MCLP를 위한 선형계획법 툴
from pulp import *
from ortools.linear_solver import pywraplp


# 시각화 툴 : Pydeck
import pydeck as pdk

# 지리 데이터 전처리 툴 : Shapely
import shapely.speedups
shapely.speedups.enable()
from shapely.ops import unary_union
from shapely.geometry import Point, MultiLineString, mapping, shape

mapbox_key = 'pk.eyJ1IjoiY3V0aWVueSIsImEiOiJja3J1ZTJrMTYxMG51MnVtd21iaGw5bjZuIn0.1W_w68zfsaE-2bc6QAW1nA'

import warnings
warnings.filterwarnings(action='ignore')

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 200)


# In[6]:


data = pd.read_csv('full_cafe_withscores.csv', index_col=False)
data = data.drop(columns=['Unnamed: 0'])
data.head()


# ### 후보지, 수요지 = 전체 카페 데이터  
# 1. 카페별로 score 구하기 -> 스타벅스 요인분석으로 weight나와서 구할 것  
# 2. descending order로 나열  
# 3. score이 최대인 카페부터 GAAS MCLP  => 해당 코드에서 진행할 부분

# In[7]:


data.columns


# In[9]:


# 카페명, 위도, 경도, score
data = data[['cafe_nm','Latitude','Longitude','scores']]
data.sort_values('scores', ascending = False, inplace = True) # score 내림차순 정렬
data.reset_index(inplace = True)

data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.Latitude, data.Longitude))


# In[10]:


data.head()


# ## MCLP

# In[11]:


# Define parameters
n = 100  # Number of points to select
radius_m = 300  # Radius in meters

# Convert meters to degrees (approximation)
def meters_to_degrees(meters):
    return meters / 111320

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x[i] is 1 if location i is selected, 0 otherwise
x = {}
for i in range(len(data)):
    x[i] = solver.IntVar(0, 1, f'x[{i}]')


# In[14]:


from tqdm import tqdm
import numpy as np

# Objective function: Maximize the weighted score
objective = solver.Objective()
for i in tqdm(range(len(data)), desc="Objective Setup"):
    objective.SetCoefficient(x[i], data['scores'][i])
objective.SetMaximization()

# Constraints: Limit selection based on distance
for i in tqdm(range(len(data)), desc="Constraints Setup"):
    for j in range(len(data)):
        if i != j:
            lat1, lon1 = data['Latitude'][i], data['Longitude'][i]
            lat2, lon2 = data['Latitude'][j], data['Longitude'][j]
            
            # Calculate the distance between two points (using Haversine formula)
            distance = np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111320  # Convert degrees to meters
            
            if distance <= radius_m:
                # Ensure that if j is selected, i cannot be selected
                solver.Add(x[i] + x[j] <= 1)


# In[15]:


from tqdm import tqdm

# Solve the problem
solver.Solve()

# Get the selected points with a progress bar
selected_indices = [i for i in tqdm(range(len(data)), desc="Selecting Points") if x[i].solution_value() == 1]
selected_data = data.iloc[selected_indices]


# In[16]:


selected_data.to_csv('selected_data.csv', index=False)


# In[17]:


selected_data


# In[22]:


# Visualizing selected points using Pydeck
deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=selected_data['Latitude'].mean(),
        longitude=selected_data['Longitude'].mean(),
        zoom=15,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=selected_data,
            get_position="[Longitude, Latitude]",
            get_color = "[255, 255, 0, 255]",  # Fully opaque yellow
            get_radius=60,  # Radius of the points
            pickable=True,
        ),
    ],
)

# Render the visualization
deck.show()


# ## 얼마나 커버하는지

# In[24]:


from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# Step 1: Calculate the coverage of each selected cafe with tqdm
coverage_counts = []

for idx, selected_point in tqdm(selected_data.iterrows(), total=selected_data.shape[0], desc="Computing Coverage for Selected Cafes"):
    count = 0
    lat1, lon1 = selected_point['Latitude'], selected_point['Longitude']
    
    for _, other_point in data.iterrows():
        lat2, lon2 = other_point['Latitude'], other_point['Longitude']
        
        # Calculate the distance between selected cafe and other cafes
        distance = np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111320  # Convert degrees to meters
        
        # If the distance is within the radius, increment the coverage count
        if distance <= radius_m:
            count += 1
    
    coverage_counts.append(count)

# Add the coverage counts to the selected data for visualization
selected_data['coverage_count'] = coverage_counts


# In[28]:


selected_data.to_csv('selected_data_with_coverage.csv', index=False)


# In[29]:


selected_data.to_file('selected_data_with_coverage.geojson', driver='GeoJSON')


# In[30]:


pip install contextily


# In[32]:


# 불러오기
selected_data = pd.read_csv('selected_data_with_coverage.csv')
import geopandas as gpd
selected_data = gpd.read_file('selected_data_with_coverage.geojson')


import contextily as ctx

# Convert the selected data to a GeoDataFrame if it's not already one
gdf = gpd.GeoDataFrame(selected_data, geometry=gpd.points_from_xy(selected_data['Longitude'], selected_data['Latitude']))

# Set the coordinate reference system (CRS) to Web Mercator (EPSG:3857) for compatibility with most map tiles
gdf = gdf.to_crs(epsg=3857)

# Plot with base map
fig, ax = plt.subplots(figsize=(10, 8))

# Plot points with size proportional to the coverage count
gdf.plot(
    ax=ax, 
    marker='o', 
    color='green', 
    markersize=gdf['coverage_count'] * 10,  # Adjust the size
    alpha=0.6
)

# Add a base map (OpenStreetMap or other tile providers)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Add title and labels
plt.title('Selected Cafes and Their Coverage on Map', fontsize=15)

# Show plot
plt.show()


# ## 선으로 연결?

# In[27]:


from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, LineString

# Step 1: Convert data to a GeoDataFrame
gdf_all = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['Longitude'], data['Latitude']))
gdf_selected = gpd.GeoDataFrame(selected_data, geometry=gpd.points_from_xy(selected_data['Longitude'], selected_data['Latitude']))

# Step 2: Prepare the figure
fig, ax = plt.subplots(figsize=(10, 8))

# Step 3: Plot all cafes (non-selected ones in grey)
gdf_all.plot(ax=ax, marker='o', color='grey', markersize=5, alpha=0.5, label='Other Cafes')

# Step 4: Plot selected cafes (in yellow, larger size)
gdf_selected.plot(ax=ax, marker='o', color='yellow', markersize=100, alpha=0.7, label='Selected Cafes')

# Step 5: Draw lines connecting selected cafes to nearby cafes using tqdm
for idx, selected_point in tqdm(selected_data.iterrows(), total=selected_data.shape[0], desc="Drawing Connections"):
    lat1, lon1 = selected_point['Latitude'], selected_point['Longitude']
    
    for _, other_point in data.iterrows():
        lat2, lon2 = other_point['Latitude'], other_point['Longitude']
        
        # Calculate the distance between selected cafe and other cafes
        distance = np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111320  # Convert degrees to meters
        
        # If the distance is within the radius, draw a line connecting the points
        if distance <= radius_m:
            line = LineString([(lon1, lat1), (lon2, lat2)])
            ax.plot([lon1, lon2], [lat1, lat2], color='blue', linewidth=0.5, alpha=0.6)

# Step 6: Add title and labels
plt.title('Selected Cafes and Coverage Connections', fontsize=15)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show plot with legend
plt.legend()
plt.show()


# In[50]:


import matplotlib.pyplot as plt
from matplotlib import rc
import platform

# Set font family and size for Korean text
if platform.system() == 'Darwin':  # Mac OS
    rc('font', family='AppleGothic')  # Apple SD Gothic Neo (default Mac font)
else:
    rc('font', family='NanumGothic')  # Or use 'NanumGothic' if you installed it

# Prevent Korean text from being displayed as blocks or cut-off
plt.rcParams['axes.unicode_minus'] = False


# In[67]:


# Save the central cafe (as GeoJSON)
gdf_central.to_file('central_cafe.geojson', driver='GeoJSON')
# Save nearby cafes (as GeoJSON)
gdf_nearby.to_file('nearby_cafes.geojson', driver='GeoJSON')
# Save the connecting lines (as GeoJSON)
gdf_lines.to_file('connection_lines.geojson', driver='GeoJSON')


# In[72]:


# 불러오기
# import geopandas as gpd

# # Load central cafe
# gdf_central = gpd.read_file('central_cafe.geojson')

# # Load nearby cafes
# gdf_nearby = gpd.read_file('nearby_cafes.geojson')

# # Load connection lines
# gdf_lines = gpd.read_file('connection_lines.geojson')

# data = pd.read_csv('all_cafe_with_scores_geo.csv', index_col=False)


import random
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import contextily as ctx

# Step 2: Convert data to GeoDataFrame if not done already
gdf_all = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['Longitude'], data['Latitude']))

# Step 3: Select one random cafe as the center
random_cafe_idx = random.randint(0, len(gdf_all) - 1)
central_cafe = gdf_all.iloc[random_cafe_idx]

# Step 4: Calculate distances and select nearby cafes within a given radius
radius_m = 500  # You can set your desired radius in meters
lat1, lon1 = central_cafe['Latitude'], central_cafe['Longitude']
cafe_name = central_cafe['cafe_nm']  # Correctly accessing the name of the cafe


# Step 5: Find nearby cafes
nearby_cafes = []
lines = []
for _, other_point in gdf_all.iterrows():
    lat2, lon2 = other_point['Latitude'], other_point['Longitude']
    distance = np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111320  # Convert degrees to meters
    
    if distance <= radius_m:
        nearby_cafes.append(other_point)
        line = LineString([(lon1, lat1), (lon2, lat2)])
        lines.append(line)

# Convert nearby cafes and lines to GeoDataFrames
gdf_nearby = gpd.GeoDataFrame(nearby_cafes)
gdf_lines = gpd.GeoDataFrame(geometry=lines)

# Step 6: Set up the figure and plot
fig, ax = plt.subplots(figsize=(7, 5))

# Plot all other cafes (grey and small, for context)
gdf_all.plot(ax=ax, marker='o', color='grey', markersize=5, alpha=0.3, label='Other Cafes')

# Plot nearby cafes (Green, medium size, semi-opaque)
gdf_nearby.plot(ax=ax, marker='o', color='orange', markersize=20, alpha=0.7, label='Nearby Cafes')

# Plot the connecting lines (Orange)
gdf_lines.plot(ax=ax, color='green', linewidth=2, alpha=0.8, label='Connections')

# Plot the central cafe (Red, larger, semi-opaque)
gdf_central = gpd.GeoDataFrame([central_cafe])
gdf_central.plot(ax=ax, marker='o', color='red', markersize=40, alpha=0.7, label='Central Cafe', zorder=5)


# Add a base map (OpenStreetMap)
# ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Add annotation for central cafe (latitude, longitude, and name)
ax.text(
    lon1 + 0.001, lat1,  # Adjust text position relative to the point
    f"{cafe_name}\nLat: {lat1:.6f}, Lon: {lon1:.6f}",
    fontsize=10,
    color='black',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='black')
)

# Add names for nearby cafes, placing text around them in a circular pattern
# for _, nearby_cafe in gdf_nearby.iterrows():
#     lat2, lon2 = nearby_cafe['Latitude'], nearby_cafe['Longitude']
#     nearby_name = nearby_cafe['cafe_nm']
    
#     # Calculate the angle between the central cafe and the nearby cafe
#     angle = np.arctan2(lat2 - lat1, lon2 - lon1)
    
#     # Adjust the position of the text based on the angle
#     offset_x = 0.002 * np.cos(angle)  # Horizontal offset based on angle
#     offset_y = 0.002 * np.sin(angle)  # Vertical offset based on angle
    
#     # Add text labels near the nearby cafes (slightly offset for clarity)
#     ax.text(
#         lon2 + offset_x, lat2 + offset_y,  # Adjust text position based on angle
#         nearby_name,
#         fontsize=8,
#         color='black'
#     )

# Set zoom to central cafe and nearby points
ax.set_xlim(gdf_central.geometry.x.min() - 0.01, gdf_central.geometry.x.max() + 0.01)
ax.set_ylim(gdf_central.geometry.y.min() - 0.01, gdf_central.geometry.y.max() + 0.01)

# Add labels and title
plt.title('Central Cafe and Nearby Coverage with Connections', fontsize=15)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Add legend
plt.legend()

# Show the plot
plt.show()


# In[ ]:




