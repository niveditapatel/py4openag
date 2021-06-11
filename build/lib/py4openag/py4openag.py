import os
import glob
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
import random 
from ipyleaflet import Map 
from ipyleaflet import basemaps 
from ipyleaflet import (Map, basemaps, WidgetControl, GeoJSON, 
                        LayersControl, Icon, Marker,FullScreenControl,
                        CircleMarker, Popup, AwesomeIcon) 
from ipywidgets import HTML
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import codecs

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
    gdd=sum/k
    return gdd

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
    pvalT=p
    r=p[0]
    return r,pvalT[1],reg.coef_[0]

  def preciptrend(self,data,years):
    pvalP=[]
    yearavg=[]
    for year in range(years[0],years[1]+1):
      new_df=data[data['Date'].dt.year==year]
      avg=new_df['total_precipitation'].mean()
      yearavg.append(avg)
    x = np.array(yearavg)
    t = np.array([i for i in range(len(yearavg))])
    reg = LinearRegression().fit(t.reshape(-1, 1), x)
    p = stats.pearsonr(t, x)
    pvalP=p
    r=p[0]
    return r,pvalP[1],reg.coef_[0]

  def plotmap(self,metric,climatedf,coorddf,filepath,filename='Map'):
    sel_cols = ['Location','Year',metric]
    climatedf = climatedf[sel_cols]
    climatedf=climatedf.reindex(columns = climatedf.columns.tolist()  
                                  + ['color'])
    color=[]
    for (i,j) in climatedf.iterrows():
        value=(j[metric]-climatedf[metric].min())/(climatedf[metric].max()-climatedf[metric].min())
        if(value>0 and value<=(1/6)):
            color.append('darkblue')
        elif(value>(1/6) and value<=(2/6)):
            color.append('blue')
        elif(value>(2/6) and value<=(3/6)):
            color.append('green')
        elif(value>(3/6) and value<=(4/6)):
            color.append('orange')
        elif(value>(4/6) and value<=(5/6)):
            color.append('red')
        else:
            color.append('darkred')
    climatedf['color']=color
    gps_color = pd.merge(climatedf, coorddf, on=['Location'])
    gps_color.head()
    newdata = pd.DataFrame([])
    for (index,row) in gps_color.iterrows():
        row['Latitude']+=random.uniform(0.1, 0.9)
        row['Longitude']+=random.uniform(0.1, 0.9)
        newdata=newdata.append(row)
    center = [39.0119, -98.4842]
    zoom = 3
    i=0
    m = Map(basemap=basemaps.Esri.WorldImagery, center=center, zoom=zoom)
    for (index,row) in newdata.iterrows():
        icon= AwesomeIcon(
            name='tint',
            marker_color=row.loc['color'], #'#583470'
            icon_color='black',
            spin=False
        )
        loc = [row.loc['Latitude'],row.loc['Longitude']]
        marker = Marker(location=loc, draggable=False, icon=icon)
        m.add_layer(marker);
        i+=1
    m.add_control(FullScreenControl())
    m.save(filepath+"/"+filename+'.html',title=filename)
    mpl.rcParams.update({'font.size': 10})
    fig=plt.figure(figsize=(8,3))
    ax=fig.add_subplot(111)
    vals=[]
    for i in range(7):
        vals.append((((climatedf[metric].max()-climatedf[metric].min())/6)*i)+climatedf[metric].min())
    cmap = mpl.colors.ListedColormap(['darkblue','deepskyblue','limegreen','orange','red','darkred'])
    norm = mpl.colors.BoundaryNorm(vals, cmap.N)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                spacing='uniform',
                                orientation='horizontal',
                                extend='neither',
                                ticks=vals)
    cb.set_label(metric)
    ax.set_position((0.1, 0.45, 0.8, 0.1))
    plt.savefig(filepath+"/"+'legend.jpg',dpi=2000,bbox_inches="tight")
    file = codecs.open(filepath+"/"+filename+'.html', "r", "utf-8")
    file_list=file.read().split("\n")
    file.close()
    print(file_list)
    file_list.insert(-3, "<img src='legend.jpg' alt='Plot Legend' style='width:35%;'>")
    file = codecs.open(filepath+"/"+filename+'.html', "w", "utf-8")
    file.write("\n".join(file_list))
    file.close()
    return m,fig

  def heavy_precipitation_days(self,data,years):
    new_df=pd.DataFrame()
    for year in range(years[0],years[1]+1):
      new_df=new_df.append(data[data['Date'].dt.year==year], ignore_index = True)
    x=(0.99*(new_df['mean_2m_air_temperature'].max()-new_df['mean_2m_air_temperature'].min()))+new_df['mean_2m_air_temperature'].min()
    heavyprecipdays=new_df[new_df['mean_2m_air_temperature'] > x]['mean_2m_air_temperature'].count()
    return heavyprecipdays