# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 03:32:04 2018

@author: Lei
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import datetime

def draw_heatmap(data,xlabels,ylabels):
    cmap = cm.Blues    
    figure=plt.figure(facecolor='w')
    ax=figure.add_subplot(1,1,1,position=[0.1,0.15,0.8,0.8])
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels)
    ax.set_xticks(range(len(xlabels)))
    ax.set_xticklabels(xlabels)
    vmax=data[0][0]
    vmin=data[0][0]
    for i in data:
        for j in i:
            if j>vmax:
                vmax=j
            if j<vmin:
                vmin=j
    map=ax.imshow(data,interpolation='nearest',cmap=cmap,aspect='auto',vmin=vmin,vmax=vmax)
    cb=plt.colorbar(mappable=map,cax=None,ax=None,shrink=0.5)
    plt.show()
        
def draw_month_heatmap(df):#传入当月的df
    day_series=df['day'].value_counts()
    first_time = pd.Timestamp.fromtimestamp(df['CreateTime'][0])
    #转化北京时间
    first_time = first_time + pd.Timedelta(hours=8)
    #print(first_time)
    #当月的首日
    #print ('%02d月%02d日 星期%1d' %(first_time.month, first_time.day, first_time.dayofweek+1))
    first_time = first_time - pd.Timedelta(days = first_time.day-1)
    last_time = first_time + pd.Timedelta(days = first_time.daysinmonth - 1)
    table_height = last_time.week - first_time.week + 1
    table_width = 7
    datamap = np.zeros(table_width*table_height)
    maskmap = np.zeros(table_width*table_height)
    for i in range(table_height*table_width):
        date_in_month = i-first_time.dayofweek+1
        if date_in_month in day_series.index:
            datamap[i]=day_series[date_in_month]
        #将不在本月的数据划掉
        if date_in_month <= 0 or date_in_month>first_time.daysinmonth:
            maskmap[i]=True
       # else: maskmap=False
    datamap = datamap.reshape((table_height, table_width))
    maskmap = maskmap.reshape((table_height, table_width))
    datamap = pd.DataFrame(datamap)
    datamap.columns=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    #print(maskmap)
    
    f, ax1 = plt.subplots(figsize=(9, 5),facecolor=cm.Blues(0))
    sns.set()
    sns.heatmap(datamap,annot=datamap.astype('int32'),mask = maskmap, square = True,yticklabels = False, fmt="d",cmap=cm.Blues, ax=ax1,linewidths=.5)
    label_y = ax1.get_yticklabels()
    plt.setp(label_y, rotation=360, horizontalalignment='right')
    label_x = ax1.get_xticklabels()
    plt.setp(label_x, rotation=0, horizontalalignment='center', y=1.1)
    plt.show()
    
def check_a_day(df, day):
      df = df[df['day']==day]
      df1 = df.apply(lambda x: pd.Timestamp.fromtimestamp(x.CreateTime).hour, axis =1)
      hour_distri = df1.value_counts().sort_index()
      print(hour_distri)
      plt.plot(hour_distri)

plt.style.use('seaborn-white') 
filename = 'df.csv'
print('Start loading file...')
df = pd.read_csv(filename, encoding='GB18030', index_col=0)
df1 = df[df['date_str']=='2018-04']
df1 = df1.rename(index = str , columns={'date_str':'month_str'}).reset_index()
draw_month_heatmap(df1)

#提取yuan的发言 并计算长度
df1=df[df['Type']==1]
df1=df1[df1['user']=='song']
df1['txt_length']=df1.apply(lambda x: len(x.Message),axis=1)
plt.hist(df1['txt_length'],range=(1,20),histtype='bar', color='yellowgreen', rwidth=0.8,\
             bins=20)