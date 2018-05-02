# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime


def ana_message(message, ms_type, des):
    #此处放用户id字典，为了隐私我都改成***了
    user_dict ={u'**********:':'zhao',
                u'******:':'wang',
                u'****:':'shen',
                u'*******:':'yan',
                u'******:':'zhu',
                u'*******:':'song',
                u'********:':'li',
                u'*******:':'yuan',
                u'********:':'zhu2',
                u'******@chatroom:':'group'#修改群昵称
                }
    user_id = ''
    content = ''
    ms_list = message.split('\n')
    if ms_type==10000:
        user_id = 'wechat'
        content = message
    elif des==0:
        user_id = 'gl'
        content = message
    elif re.match('.*:', ms_list[0]):
        user_name = ms_list[0]
        if user_name in user_dict.keys():
            user_id = user_dict[user_name]
            content = message[len(user_name)+1:]
        else:
            if ms_type==49:#红包 <fromusername>wxid_here</fromusername>
                match = re.search(r'<fromusername>.*</fromusername>',message)
                user_name = match.group(0)[len('<fromusername>'):-len('<fromusername>')-1]+':'
                if user_name in user_dict.keys():
                    user_id = user_dict[user_name]
                else:
                    user_id = 'ukPerson'
            content = 'TYPE.HONGBAO'
            
    
    elif ms_type==43:#视频 关键字fromusername
        match = re.search(r'fromusername=".*?"', message)
        user_name = match.group(0)[len('fromusername=\"'):-1]+':'
        if user_name in user_dict.keys():
            user_id = user_dict[user_name]
        else:
            user_id = 'ukPerson'
        content = 'TYPE.VIDEO'
    else:#未知bug 4条10002重新编辑
        user_id = 'gl'
        content = '你撤回了一条消息'
    return user_id, content

def timestamp2datetime(timestamp, convert_to_local=True):
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    if convert_to_local: # 是否转化为本地时间
      dt = dt + datetime.timedelta(hours=8) # 中国默认时区
    return dt
        
#初始化 导入数据 进行筛选
plt.style.use('ggplot')
filename = '111.csv'
print('Start loading file...')
df = pd.read_csv(filename, encoding='GB18030')
print('File-loading done. Start analysing message...')
df = df[['CreateTime','Message','Type','Des']]
#df = df.reindex(columns=['date','hour','week','user_id','content'])
print('user...')
df['user']=df.apply(lambda x: ana_message(x.Message, x.Type, x.Des)[0], axis=1)
print('content..')
df['Message']=df.apply(lambda x: ana_message(x.Message, x.Type, x.Des)[1], axis=1)
print('time...')
df['time']=df.apply(lambda x: timestamp2datetime(x.CreateTime, True), axis=1)
print('DataFrame created successfully!')

#开始对数据进行分析
#1 对dataFrame的用户条message数分析
#筛选时间
#df1 = df[df['CreateTime']>='2018-04-01 00:00:00'] 
plt.hist(df['user'], bins=12, color='yellowgreen', histtype='bar', rwidth=0.8)

def mes_count(df):
    ax1 = plt.subplot(111)
    ax1.hist(df['user'],histtype='bar', color='yellowgreen', rwidth=0.8,\
             bins=11)
    
def date_count(df):
    pass

def histdf(df, barnum):
    plt.hist(df['user'], bins=barnum, color='yellowgreen', histtype='bar', rwidth=0.8)
    
    
#查看谁最喜欢撤回消息  
df1=df[df['user']=='wechat']

df.to_csv('df.csv', encoding='GB18030')

    