#!/usr/bin/env python
# coding: utf-8

# In[7]:


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


# In[17]:


data = pd.read_excel('./data/DAB_data.xlsx')
data.head()


# In[18]:


data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.Latitude, data.Longitude))
data = data.reset_index()
data = data.rename(columns = {'col_name' : 'weights'}) # 가중치로 쓸 컬럼
data.head()


# In[14]:


data.crs = 'epsg:4326'


# In[15]:


base = pdk.Layer(
    'PolygonLayer', # 사용할 Layer 타입
    data, # 시각화에 쓰일 데이터프레임
    get_polygon='coordinates', # geometry 정보를 담고있는 컬럼 이름
    get_fill_color='[255, 255, 255]', # 각 데이터 별 rgb 또는 rgba 값 (0~255)
    opacity = 0.005
)


# In[ ]:


I = data.index.values
J = data.index.values
S = 300 # Coverage 거리
# min_dist =
a = data.weights.values
P = 100 # 설치예정 시설물 수

# Compute the sets Ni
# NB: this will be a list in which each item is a list of nodes
# within the threshold distance of the i'th node
N = [[j for j in J if d[i][j] < S] for i in I]
R = [[int(r[station_i][station_j] < min_dist) for station_j in J ] for station_i in J]
# Formulate optimisation

prob = LpProblem("MCLP", LpMaximize)
x = LpVariable.dicts("x", J, lowBound=0, upBound=1, cat='Integer')
y = LpVariable.dicts("y", I, lowBound=0, upBound=1, cat='Integer')

# Objective
prob += lpSum([a[i]*y[i] for i in I])

# Constraints
for i in I:
    prob += lpSum([x[j] for j in N[i]]) >= y[i]
for j in J:
    prob += lpSum([x[rr] for rr in R[j]]) <= 1
    

prob += lpSum([x[j] for j in J]) == P

# Solve problem
prob.solve()

x_soln = np.array([x[j].varValue for j in J])

# And print some output
print (("Status:"), LpStatus[prob.status])
print ("Weight Covered is = ", value(prob.objective))
print ("x = ", x_soln)

