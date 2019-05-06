# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 22:50:35 2019

"""

import os 
os.chdir('F:\\python_study\\pachong\\doubangame')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import Radar,Pie,Style,Line,WordCloud
from PIL import Image
import jieba
import jieba.analyse
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

"""
数据合并
"""
path = os.listdir()

dataall = pd.DataFrame()
for i in path[6:]:
 
    datas = pd.read_excel(i,index_col = 0)
    dataall = pd.concat([dataall,datas],axis = 0)
    print(i + ' finished!')

dataall = dataall.reset_index(drop = True)
dataall['name_num'] = dataall.name.apply(lambda x:len(x))
dataall.to_excel('游戏数据汇总.xlsx',index = False)






"""
游戏分布
"""

dataall['n_platforms'] = dataall.platforms.apply(lambda x:len(str(x).split('/')))
dataall['platform'] =  dataall.platforms.apply(lambda x:str(x).split('/')[0].strip())


sns.pairplot(dataall,diag_kind = 'kde')   
plt.show()
 


data2 = dataall.dropna()
sns.pairplot(data2,diag_kind = 'kde')   
plt.show()
 



"""
各类型游戏分析
"""
 
# 各类型游戏数

num = len(dataall.name.unique())
result = dataall.groupby('type').count()['name'].reset_index().sort_values('name',ascending = False)



attr = list(result.type)
v  = list(np.round(result.name/num,3)) 

pie = Pie()
style = Style()
pie_style = style.add(
    label_pos="center",
    is_label_show=True,
    label_text_color=None,
    is_legend_show = False
)
pie.add("",[attr[0],"其他"],[v[0],1-v[0]],radius=[18, 24],center = [10,20],**pie_style)
pie.add("",[attr[1],"其他"],[v[1],1-v[1]],radius=[18, 24],center = [30,20],**pie_style)
pie.add("",[attr[2],"其他"],[v[2],1-v[2]],radius=[18, 24],center = [50,20],**pie_style)
pie.add("",[attr[3],"其他"],[v[3],1-v[3]],radius=[18, 24],center = [70,20],**pie_style)
pie.add("",[attr[4],"其他"],[v[4],1-v[4]],radius=[18, 24],center = [90,20],**pie_style)

pie.add("",[attr[5],"其他"],[v[5],1-v[5]],radius=[18, 24],center = [10,50],**pie_style)
pie.add("",[attr[6],"其他"],[v[6],1-v[6]],radius=[18, 24],center = [30,50],**pie_style)
pie.add("",[attr[7],"其他"],[v[7],1-v[7]],radius=[18, 24],center = [50,50],**pie_style)
pie.add("",[attr[8],"其他"],[v[8],1-v[8]],radius=[18, 24],center = [70,50],**pie_style)
pie.add("",[attr[9],"其他"],[v[9],1-v[9]],radius=[18, 24],center = [90,50],**pie_style)

pie.add("",[attr[10],"其他"],[v[10],1-v[10]],radius=[18, 24],center = [10,80],**pie_style)
pie.add("",[attr[11],"其他"],[v[11],1-v[11]],radius=[18, 24],center = [30,80],**pie_style)
pie.add("",[attr[12],"其他"],[v[12],1-v[12]],radius=[18, 24],center = [50,80],**pie_style)
pie.add("",[attr[13],"其他"],[v[13],1-v[13]],radius=[18, 24],center = [70,80],**pie_style)
pie.add("",[attr[14],"其他"],[v[14],1-v[4]],radius=[18, 24],center = [90,80],**pie_style)


pie.render('各类型游戏数.html')




# 各类型游戏均分
c_schema= [( "乱斗/清版",10),
           ( "体育",10),
           ( "冒险",10),
           ( "动作",10),
           ( "即时战略",10),
           ( "射击",10),
           ( "格斗",10),
           ( "模拟",10),
           ( "横版过关",10),
           ( "益智",10),
           ( "竞速",10),
           ( "第一人称射击",10),
           ( "策略",10),
           ( "角色扮演",10),
           ( "音乐/旋律",10)]
result1 = dataall.rating.fillna(0).groupby(dataall.type).mean().reset_index()
result2 = dataall.rating.dropna().groupby(dataall.dropna().type).mean().reset_index()

v1 = [result1.rating.apply(lambda x:round(x,1)).tolist()]
v2 = [result2.rating.apply(lambda x:round(x,1)).tolist()]
  
radar = Radar()
radar.config(c_schema)
radar.add("游戏均分（无评分视为0）", v1, is_splitline=True, is_axisline_show=True,is_label_show = True)
radar.add("游戏均分（删除无评分）", v2, label_color=["#4e79a7"],item_color="#f9713c",is_label_show = True)
radar.render('各类型游戏评分.html')

 
# 各类型游戏评分人数
 
result1 = dataall.n_ratings.fillna(0).groupby(dataall.type).mean().reset_index()
result2 = dataall.n_ratings.dropna().groupby(dataall.dropna().type).mean().reset_index()

attr = result1.type.tolist()
v1 = np.round(result1.n_ratings.tolist(),1)
v2 = np.round(result2.n_ratings.tolist(),1)
line = Line()
#line.add(x_axis = attr,y_axis = xaxis_type = 'category')
line.add("包含无评分", attr, v1, mark_point=["max"],is_label_show = True)
line.add("不包含无评分", attr, v2, is_smooth=True, mark_point=["max"],is_label_show = True,xaxis_rotate  = 30)
line.render('各类型游戏-评分人数.html')




"""
游戏平台分析
"""
# 各平台游戏数

num = len(dataall.name.unique())
result = dataall.groupby('platform').count()['name'].reset_index()


name = result.platform.tolist()
value = result.name.tolist()
wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("", name, value, word_size_range=[20, 120])
wordcloud.render('游戏平台.html')


platforms = result.loc[result.name >100,'platform'].tolist()


dataall.platform = dataall.platform.apply(lambda x:x if x in platforms else '其他')
result = dataall.groupby('platform').count()['name'].reset_index().sort_values('name',ascending = False).reset_index(drop = True)


attr = result.platform
v1 = result.name
pie = Pie('各平台游戏数',title_pos = 'center',title_text_size = 20)
pie.add(
    "",
    attr,
    v1,
    radius=[40, 75],center = [50,60],
    label_text_color=None,is_legend_show = False,
    is_label_show=True
)
pie.render('各平台游戏数.html')






# 各平台游戏评分人数

result1 = dataall.n_ratings.fillna(0).groupby(dataall.platform).mean().reset_index()
result2 = dataall.n_ratings.dropna().groupby(dataall.dropna().platform).mean().reset_index()

attr = result1.platform.tolist()
v1 = np.round(result1.n_ratings.tolist(),1)
v2 = np.round(result2.n_ratings.tolist(),1)
line = Line()
#line.add(x_axis = attr,y_axis = xaxis_type = 'category')
line.add("包含无评分", attr, v1, mark_point=["max"],is_label_show = True)
line.add("不包含无评分", attr, v2, is_smooth=True, mark_point=["max"],is_label_show = True,xaxis_rotate  = 70)
line.render('各平台游戏-评分人数.html')


# 各平台游戏均分

result1 = dataall.rating.fillna(0).groupby(dataall.platform).mean().reset_index()
result2 = dataall.rating.dropna().groupby(dataall.dropna().platform).mean().reset_index()

attr = result1.platform.tolist()
v1 = np.round(result1.rating.tolist(),1)
v2 = np.round(result2.rating.tolist(),1)
line = Line()
#line.add(x_axis = attr,y_axis = xaxis_type = 'category')
line.add("包含无评分", attr, v1, mark_point=["max"],is_label_show = True)
line.add("不包含无评分", attr, v2, is_smooth=True, mark_point=["max"],is_label_show = True,xaxis_rotate  = 70)
line.render('各平台游戏-均分.html')





"""
高rating游戏分析
"""
 
data1 = dataall.loc[dataall.rating>=9.5]

result = data1.groupby('type').count()['name'].reset_index().sort_values('name',ascending = False).reset_index(drop = True)


attr = result.type
v1 = result.name
pie = Pie('9.5分以上游戏',title_pos = 'center',title_text_size = 20)
pie.add(
    "",
    attr,
    v1,
    radius=[40, 75],center = [50,60],
    label_text_color=None,is_legend_show = False,
    is_label_show=True
)
pie.render('高评分游戏-分类型.html')




data1['title'] = data1.name.apply(lambda x:str(x).split(':')[0].split(' ')[0])


# 9.5以上评分，评分人数超过1000
result = data1.loc[data1.n_ratings >= 100,['name','genres','content','platforms','rating','n_ratings']].drop_duplicates().reset_index(drop = True) 

result = result.sort_values(by = ['n_ratings','genres'],ascending = False).reset_index(drop = True)
result.to_excel('评分9.5以上游戏.xlsx')



 
"""
标题分析

"""


# 分词
import re
stopwords = open('中文停用词表（比较全面，有1208个停用词）.txt','r').read()
stopwords = stopwords.split('\n')


texts = ''.join(dataall.name.tolist())
texts =''.join(re.findall(r'[\u4e00-\u9fa5]',texts))
result = jieba.cut(texts,cut_all=False)


allwords = [word for word in result if len(word)>1 and word not in stopwords]


 
result = pd.DataFrame(allwords)
result.columns =['word']
res = result.word.groupby(result.word).count()

res.index.name = 'text'
res = res.reset_index()

res = res.loc[res.word >= 10].reset_index(drop = True)


# 标题词云
name = res.text.tolist()
value = res.word.tolist()
wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("", name, value, word_size_range=[10, 80])
wordcloud.render('游戏名称高频词.html')




"""
游戏类型关联分析
"""

alltype = dataall.type.unique().tolist()

#result = pd.DataFrame(columns = ['i','j','n'])
#for i in alltype:
#    for j in alltype:
#        if i!=j:
#            name1 = dataall.loc[dataall.type==i,'name'].tolist()
#            name2 = dataall.loc[dataall.type==j,'name'].tolist()
#            
#            num = len(set(name1)&set(name2))
#            s = pd.DataFrame(np.array([i,j,num])).T
#            s.columns = ['i','j','n']
#            result = pd.concat([result,s],axis =0)
#        else:
#            num = dataall.loc[dataall.type==i,'name'].shape[0]
#            s = pd.DataFrame(np.array([i,j,num])).T
#            s.columns = ['i','j','n']
#            result = pd.concat([result,s],axis =0)
#    print(i + ' finished!')
#result = result.reset_index(drop = True)
#
# 


result = pd.DataFrame(columns = alltype,index = alltype)
for i in alltype:
    for j in alltype:
        if i!=j:
            name1 = dataall.loc[dataall.type==i,'name'].tolist()
            name2 = dataall.loc[dataall.type==j,'name'].tolist()
            
            num = len(set(name1)&set(name2))

        else:
#            num = dataall.loc[dataall.type==i,'name'].shape[0]
            num = 0
        result.loc[i,j] = num
    print(i + ' finished!')
 
# ,cmap = 'YlGnBu'    
plt.figure(figsize = (10,5))
sns.heatmap(-result)
