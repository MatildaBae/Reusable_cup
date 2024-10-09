#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Font
# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf

import matplotlib.pyplot as plt
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] =False

import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


# In[2]:


# 스타벅스 데이터
data = pd.read_csv('starbucks_f.csv', index_col=0)
data = data.iloc[:,:-1]
data.head()


# In[3]:


# 런타임 재시작
# numeric 변수만 추출해서 분포 확인
num_data = data.drop(columns=['branchnm', '동이름', '매출액추정(행정동)'])
num_data.hist(figsize=(20,20))

corr = num_data.corr()
plt.figure(figsize=(20,20))
sns.heatmap(corr, annot=True, cmap='Blues')


# In[7]:


data.columns


# In[ ]:





# In[8]:


# 필요한 변수만 추출
# data = data.drop(['branchnm', '동이름', '매출액추정(행정동)', '매출건수추정(행정동)', 'Latitude', 'Longitude'], axis=1)
data = data[['에코매장 유무','지하철역 거리','버스정류장거리','유동인구수',
       '근방카페개수', '근방쓰레기통개수','근방공공시설수', '지가', '근방 음식점 수','매출추정(블록에 포함된 것, 19년도 3분기 총매출)',
             '일회용품 소비정도']]
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
y = data['에코매장 유무']
X = data.drop('에코매장 유무', axis=1)

col_list = data.columns.tolist()
col_list.remove('에코매장 유무')
X[col_list] = scaler.fit_transform(X[col_list])

X.head()


# In[20]:


# 필요한 변수만 추출
# data = data.drop(['branchnm', '동이름', '매출액추정(행정동)', '매출건수추정(행정동)', 'Latitude', 'Longitude'], axis=1)
data = data[['에코매장 유무','지하철역 거리','버스정류장거리','유동인구수',
       '근방쓰레기통개수','근방공공시설수', '지가', '근방 음식점 수','매출추정(블록에 포함된 것, 19년도 3분기 총매출)',
             '일회용품 소비정도']]
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
y = data['에코매장 유무']
X = data.drop('에코매장 유무', axis=1)

col_list = data.columns.tolist()
col_list.remove('에코매장 유무')
X[col_list] = scaler.fit_transform(X[col_list])

X.head()


# In[17]:


data.drop('근방카페개수', axis=1, inplace = True)
vif_df = calculate_vif(data2)


print(vif_df)


# In[9]:


# VIF 계산
def calculate_vif(df):
    vif = pd.DataFrame()
    vif["Variable"] = df.columns
    vif["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    return vif

vif_df = calculate_vif(data)


print(vif_df)


# In[21]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
from sklearn.linear_model import LassoCV
import numpy as np

# Fit the Lasso model
lasso = LassoCV(random_state=42).fit(X_train, y_train)
importance = np.abs(lasso.coef_)

# Print R-squared values
r_squared_train = lasso.score(X_train, y_train)
r_squared_test = lasso.score(X_test, y_test)
print(f"R-squared (train): {r_squared_train}")
print(f"R-squared (test): {r_squared_test}")


# In[22]:


from sklearn.linear_model import LassoCV
import numpy as np

lasso = LassoCV(random_state=42).fit(X_train, y_train) #alpha설정 안 해도 됨!
importance = np.abs(lasso.coef_)

# 중요도가 0인 변수 제외
feature_columns = data.columns
feature_columns = [col for col in feature_columns if col != '에코매장 유무']
nonzero_importance = importance[importance > 0]
nonzero_features = np.array(feature_columns)[importance > 0]

# 중요도를 기준으로 내림차순 정렬
sorted_indices = np.argsort(nonzero_importance)[::-1]

plt.figure(figsize=(15, 6))
plt.bar(height=nonzero_importance[sorted_indices], x=nonzero_features[sorted_indices])
plt.title("Feature importances via coefficients - Lasso")
plt.xlabel("Features")
plt.ylabel("Absolute Coefficients")
plt.show()


# In[23]:


from sklearn.linear_model import RidgeCV

ridge = RidgeCV().fit(X_train, y_train)
importance = np.abs(ridge.coef_)

# 중요도가 0인 변수 제외
nonzero_importance = importance[importance > 0]
nonzero_features = np.array(feature_columns)[importance > 0]

top_n = 10
sorted_indices = np.argsort(nonzero_importance)[::-1]

plt.figure(figsize=(24, 6))
plt.bar(height=nonzero_importance[sorted_indices][:top_n], x=nonzero_features[sorted_indices][:top_n])
plt.title("Feature importances via coefficients - Ridge(Top10)")
plt.xlabel("Features")
plt.ylabel("Absolute Coefficients")
plt.show()


# In[24]:


from sklearn.linear_model import ElasticNetCV

# Fit the Elastic Net model
elastic_net = ElasticNetCV(cv=5, random_state=42).fit(X_train, y_train)
importance = np.abs(elastic_net.coef_)

# Exclude features with zero importance
nonzero_importance = importance[importance > 0]
nonzero_features = np.array(feature_columns)[importance > 0]

# Sort features by importance
top_n = 10
sorted_indices = np.argsort(nonzero_importance)[::-1]

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.bar(x=nonzero_features[sorted_indices][:top_n], height=nonzero_importance[sorted_indices][:top_n], color='#00bc70')
plt.title("Feature importances via coefficients - Elastic Net (Top 10)")
plt.xlabel("Features")
plt.ylabel("Absolute Coefficients")
plt.xticks(rotation=45)
plt.show()


# In[25]:


# Print R-squared values
r_squared_train = lasso.score(X_train, y_train)
r_squared_test = lasso.score(X_test, y_test)
print(f"R-squared (train): {r_squared_train}")
print(f"R-squared (test): {r_squared_test}")

# Print R-squared values
r_squared_train = ridge.score(X_train, y_train)
r_squared_test = ridge.score(X_test, y_test)
print(f"R-squared (train): {r_squared_train}")
print(f"R-squared (test): {r_squared_test}")

# Print R-squared values
r_squared_train = elastic_net.score(X_train, y_train)
r_squared_test = elastic_net.score(X_test, y_test)
print(f"R-squared (train): {r_squared_train}")
print(f"R-squared (test): {r_squared_test}")


# In[52]:


X_new.columns


# In[53]:


X_new['scores']=scores_new
X_new.drop('유동인구수', axis=1, inplace=True)
X_new.to_csv('full_cafe_withscores.csv')


# In[33]:


from sklearn.preprocessing import StandardScaler


# In[46]:


# •	전체 카페 데이터 프레임은 X_new
X_new = pd.read_csv('ffcafe.csv', index_col=0)  # Your new DataFrame here
# numeric 변수들만 뽑아서 분포 확인 -> 스케일러 종류 지정하기 위함
num_data = X_new[['일회용품 소비정도 = 매출건수*근방카페개수*0.5','근방쓰레기통개수', 
 '당월_매출_금액_y','공시지가','지하철역 거리', '근방공공시설수','버스정류장 거리']]

num_data.hist(figsize=(20,20))
# X_new 데이터 스케일링
scaler = StandardScaler() # or MinMaxScaler(적합한 스케일러로 지정)
X_new_scaled = scaler.fit_transform(num_data)

# Calculate scores using non-zero importances as weights
scores_new = np.dot(X_new_scaled, nonzero_importance)

# Add the score as a new column to the X_new DataFrame
X_new_with_scores = pd.DataFrame(X_new_scaled, columns=X_new_scaled.columns)  # Create DataFrame from scaled data
X_new_with_scores['Score'] = scores_new  # Add the scores as a new column
X_new_with_scores.head(10)
score_result = X_new_with_scores[['branchnm', '']]


# In[30]:


X_new.columns


# In[31]:


X_new['일회용품 소비정도 = 매출건수*근방카페개수*0.5']


# In[ ]:


['일회용품 소비정도 = 매출건수*근방카페개수*0.5','근방쓰레기통개수', 
 '당월_매출_금액_y','공시지가','지하철역 거리', '버스정류장 거리', '근방공공시설수']

