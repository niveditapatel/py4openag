import os
import glob
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

class functions:
    
  def __init__(self, data):
    validation = self.data_validation(data)
    if(validation[0]):
      columns = self.has_columns(data)
      if(columns[0]):
        self.data = data
        print('Successfully imported the data!\n')
      else:
        print(columns[1])
    else:
      print(validation[1])

  def has_columns(self,data):
    if set(['mean_2m_air_temperature','minimum_2m_air_temperature','maximum_2m_air_temperature','total_precipitation','Date']).issubset(data.columns):
      return (True,None)
    else:
      return (False,"Data is missing columns")

  def data_validation(self,data):
    if (data['Date'].dtype=='datetime64[ns]'):
      return (True,None)
    else:
      return (False, "Date has to be in datetime format")

  def extreme_degree_days(self,data,thresholdtemp, year, months=[1,12]): 
    sum=self.integral_time(data,thresholdtemp,'above',year,months)
    new_df=pd.DataFrame()
    tempdata=data[data['Date'].dt.year==year]
    for i in range(months[0],months[1]+1):
      new_df=new_df.append(tempdata[tempdata['Date'].dt.month==i], ignore_index = True)
    index=new_df.index
    extreme_degree_days=sum/len(index)
    return extreme_degree_days

  def integral_time(self,data, threshold, area, year, months): 
    sum=0
    new_df=pd.DataFrame()
    tempdata=data[data['Date'].dt.year==year]
    for i in range(months[0],months[1]+1):
      new_df=new_df.append(tempdata[tempdata['Date'].dt.month==i], ignore_index = True)
    if area=='above':
      for i, j in new_df.iterrows(): 
        sum+=max((j['mean_2m_air_temperature']-threshold),0)
    if area=='below':
      for i, j in new_df.iterrows(): 
        sum+=max((threshold-j['mean_2m_air_temperature']),0)
    return sum

  def growing_degree_days(self,data,year,basetemp):
    sum=0
    k=0
    new_df=data[data['Date'].dt.year==year]
    for i, j in new_df.iterrows(): 
        temp=(((j['minimum_2m_air_temperature']+j['maximum_2m_air_temperature'])/2)- basetemp)
        if (temp>0):
          sum+=temp
        k+=1
    return sum

  def growingdays_basetemp(self,crop):
    if crop in ["wheat", "barley", "rye", "oats", "flaxseed", "lettuce", "asparagus"]:
      return 4.5
    elif crop in ["sunflower","potato"]:
      return 8
    elif crop in ["maize", "sorghum","rice", "soybeans", "tomato", "coffee"]:
      return 10
    else:
      print("The crop is not present. Look up base temperature for: [wheat,barley,rye,oats,flaxseed,lettuce,asparagus,sunflower,potato,maize,sorghum,rice,soybeans,tomato,coffee] instead")  
      return None
  
  def average_temperature(self,data,year,months=[1,12]):
    new_df=pd.DataFrame()
    tempdata=data[data['Date'].dt.year==year]
    for i in range(months[0],months[1]+1):
      new_df=new_df.append(tempdata[tempdata['Date'].dt.month==i], ignore_index = True)
    avg=new_df['mean_2m_air_temperature'].mean()
    return avg

  def total_precipitation(self,data,year,months=[1,12]):
    new_df=pd.DataFrame()
    tempdata=data[data['Date'].dt.year==year]
    for i in range(months[0],months[1]+1):
      new_df=new_df.append(tempdata[tempdata['Date'].dt.month==i], ignore_index = True)
    sum=new_df['total_precipitation'].sum()
    return sum

  def temptrend(self,data,years): 
    trendT=[]
    pvalT=[]
    yearavg=[]
    for year in range(years[0],years[1]+1):
      new_df=data[data['Date'].dt.year==year]
      avg=new_df['mean_2m_air_temperature'].mean()
      yearavg.append(avg)
    x = np.array(yearavg)
    t = np.array([i for i in range(len(yearavg))])
    reg = LinearRegression().fit(t.reshape(-1, 1), x)
    p = stats.pearsonr(t, x)
    pvalT=p[1]
    r=p[0]
    return r,pvalT,reg.coef_[0]
