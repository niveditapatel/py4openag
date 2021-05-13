import os
import glob
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

def has_columns(data):
  if set(['mean_2m_air_temperature','total_precipitation','startDate']).issubset(data.columns):
    return (True,None)
  else:
    return (False,"Data is missing columns")

def data_validation(data):
  if (data['startDate'].dtype=='datetime64[ns]'):
    return (True,None)
  else:
    return (False, "Date has to be in datetime format")

def extreme_degree_days(data, year, months): 
  sum=integral_time(data,30,'above',year,months)
  new_df=pd.DataFrame()
  tempdata=data[data['startDate'].dt.year==year]
  for i in range(months[0],months[1]+1):
    new_df=new_df.append(tempdata[tempdata['startDate'].dt.month==i], ignore_index = True)
  index=new_df.index
  extreme_degree_days=sum/len(index)
  return extreme_degree_days

def integral_time(data, threshold, area, year, months): 
  sum=0
  new_df=pd.DataFrame()
  tempdata=data[data['startDate'].dt.year==year]
  for i in range(months[0],months[1]+1):
    new_df=new_df.append(tempdata[tempdata['startDate'].dt.month==i], ignore_index = True)
  if area=='above':
    for i, j in new_df.iterrows(): 
      sum+=max((j['mean_2m_air_temperature']-threshold),0)
  if area=='below':
    for i, j in new_df.iterrows(): 
      sum+=max((threshold-j['mean_2m_air_temperature']),0)
  return sum

def growing_days(data,year,basetemp):
  sum=0
  k=0
  new_df=data[data['startDate'].dt.year==year]
  for i, j in new_df.iterrows(): 
      temp=(((j['minimum_2m_air_temperature']+j['maximum_2m_air_temperature'])/2)- basetemp)
      if (temp>0):
        sum+=temp
      k+=1
  return sum

def growingdays_basetemp(crop):
  if crop in ["wheat", "barley", "rye", "oats", "flaxseed", "lettuce", "asparagus"]:
    return 4.5
  elif crop in ["sunflower","potato"]:
    return 8
  elif crop in ["maize", "sorghum","rice", "soybeans", "tomato", "coffee"]:
    return 10
  else:
    print("The crop is not present. Look up base temperature for: [wheat,barley,rye,oats,flaxseed,lettuce,asparagus,sunflower,potato,maize,sorghum,rice,soybeans,tomato,coffee] instead")  
    return None
  
def average_temperature(data,year,months):
  new_df=pd.DataFrame()
  tempdata=data[data['startDate'].dt.year==year]
  for i in range(months[0],months[1]+1):
    new_df=new_df.append(tempdata[tempdata['startDate'].dt.month==i], ignore_index = True)
  avg=new_df['mean_2m_air_temperature'].mean()
  return ['months '+str(months[0])+'-'+str(months[-1])+" "+str(year),avg]

def total_precipitation(data,year,months):
  new_df=pd.DataFrame()
  tempdata=data[data['startDate'].dt.year==year]
  for i in range(months[0],months[1]+1):
    new_df=new_df.append(tempdata[tempdata['startDate'].dt.month==i], ignore_index = True)
  sum=new_df['total_precipitation'].sum()
  return ['months '+str(months[0])+'-'+str(months[-1])+" "+str(year),sum]

def temptrend(data,years): 
  trendT=[]
  pvalT=[]
  yearavg=[]
  for year in range(years[0],years[1]+1):
    new_df=data[data['startDate'].dt.year==year]
    avg=new_df['mean_2m_air_temperature'].mean()
    yearavg.append(avg)
  x = np.array(yearavg)
  t = np.array([i for i in range(len(yearavg))])
  reg = LinearRegression().fit(t.reshape(-1, 1), x)
  p = stats.pearsonr(t, x)
  pvalT=p[1]
  return pvalT,reg.coef_[0]
