#!/usr/bin/python
# -*- coding: utf-8 -*-
import itchat
import json
import os,sys
import pandas
import numpy
from matplotlib import cm
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pylab as plt
import re
import jieba
from wordcloud import WordCloud, ImageColorGenerator
# from scipy.misc import imread
from imageio import imread
# Ref. https://www.jianshu.com/p/39505d2320fb
############################################
# 1. 登录微信 
itchat.auto_login()  # 会出现一个二维码，扫码即可登录 
# hotReload=True方法会生成一个静态文件 itchat.pkl ，用于存储登陆的状态，不用每次扫码

############################################
# 2. 提取存储微信好友信息的json文件，并保存到本地
# 爬取好友的相关信息，返回json文件
friends = itchat.get_friends(update=True)
# 将获取的内容写入user.json文件中
# fw = open('users.json', 'w')
# json.dump(friends, fw)
# 退出微信 
itchat.logout()
############################################
# 3. 从json文件中获得好友性别，城市，省份和个性签名等信息
# 读取json文件
# load_f = open('users.json')
# Users = json.load(load_f)
Users = friends
# 获取想要的好友信息
NickName = []  # 定义一个列表，存储好友昵称
Sex = []  # 存储好友性别
Province = []  # 存储好友所在省份
City = []  # 存储好友所在城市
Signature = []  # 个性签名

for user in Users[1:]:
    # nickName = user['NickName']  # 好友昵称
    nickName="**nickName**"
    sex = user['Sex']  # 好友性别
    province = user['Province']  # 好友所在省份
    city = user['City']  # 好友所在城市
    signature = user['Signature'].replace('\n','').replace('\r','')  # 个性签名
    NickName.append(nickName)
    Sex.append(sex)
    Province.append(province)
    City.append(city)
    Signature.append(signature)

memberList = pandas.DataFrame({
    'NickName': NickName,
    'Sex': Sex,
    'Province': Province,
    'City': City,
    'Signature': Signature
})
memberList.to_csv('memberList.csv', index=False,encoding="UTF-8")
############################################
# 4. 查看好友的性别比例
# 查看所有好友的性别比例（ 1为男性，2为女性，0为未知）
sexStat = memberList.groupby(
    by='Sex'
)['Sex'].agg({
    '计数': len
}).reset_index().sort_values(
    by='计数',
    ascending=False
)

# 性别转换表（将1，2，0分别转化为'男'， '女'， '未知'）
sex = []
count = []
for index, rows in sexStat.iterrows():
    if rows['Sex'] == 1:
        sex.append('男')
    if rows['Sex'] == 2:
        sex.append('女')
    if rows['Sex'] == 0:
        sex.append('未知')
    count.append(rows['计数'])
sexTran = pandas.DataFrame({
    'Sex': sex,
    '计数': count
})
print('[INFO]:{:-^30}'.format('您一共有{0}个好友'.format(sum(sexTran['计数']))))
print('[INFO]:{:-^30}'.format('男女统计数据如下'))
print(sexTran)

fig=plt.figure(1)
# 调节图形大小，宽，高
plt.rcParams['font.sans-serif'] = ['simhei']
plt.rcParams['axes.unicode_minus'] = False
# plt.figure(figsize=(6, 9))
# 定义饼状图的标签，标签是列表
labels = [sex for sex in sexTran['Sex']]
# 每个标签占多大，会自动去算百分比
sizes = [count for count in sexTran['计数']]
# 定义每块标签
colors = ['red', 'yellowgreen', 'lightskyblue']
# 将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (0.05, 0, 0)
patches, l_text, p_text = plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                labeldistance=1.1, autopct='%3.1f%%', shadow=False,
                                startangle=90, pctdistance=0.6)
# labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
# autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
# shadow，饼是否有阴影
# startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
# pctdistance，百分比的text离圆心的距离
# patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

# 改变文本的大小,方法是把每一个text遍历。调用set_size方法设置它的属性
for t in l_text:
    t.set_size=(30)
for t in p_text:
    t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
# plt.show()
############################################
# 5. 查看好友所在城市和省份的分布情况
# 查看好友所在地区分布情况
cityStat = memberList.groupby(
    by=['City']
)['City'].agg({
    '计数': len
}).reset_index().sort_values(
    by='计数',
    ascending=False
)
cityStat=cityStat[:20] # 取top-20
# 查看好友所在身份分布情况
provinceStat = memberList.groupby(
    by=['Province']
)['Province'].agg({
    '计数': len
}).reset_index().sort_values(
    by='计数',
    ascending=False
)
provinceStat=provinceStat[:20] # 取top-20
# 绘图（好友省份分布）
fig=plt.figure(2)
plt.subplot(2, 1, 1)
plt.title('Top20-好友省份分布')
axis1 = numpy.arange(len(provinceStat))
color = cm.jet(axis1/max(axis1))
plt.bar(axis1, provinceStat['计数'], color=color)
province = []
for p in provinceStat['Province']:
    if len(p) == 0:
        p = '未知'
    province.append(p)
plt.grid(color='#95a5a6', axis='y', linestyle='--', linewidth=1, alpha=0.4)
plt.ylabel('好友数量')
plt.xticks(axis1, province)
# 绘图（好友城市分布）
plt.subplot(2, 1, 2)
axis2 = numpy.arange(len(cityStat))
plt.rc('font', family='simhei', size=9)
plt.title('Top20-好友城市分布')
cityStat = cityStat.sort_values('计数')
color = cm.jet(axis2/max(axis2))
plt.barh(axis2, cityStat['计数'], color=color)
city = []
for c in cityStat['City']:
    if len(c) == 0:
        c = '未知'
    city.append(c)
plt.grid(color='#95a5a6', axis='x', linestyle='--', linewidth=1, alpha=0.4)
plt.xlabel('好友数量')
plt.yticks(axis2, city)
# plt.show()

############################################
# 6. 对好友个性签名统计词频，并绘制词云图
# 好友个性签名词频统计及词云绘制
signature_list = []
# 删除个性签名中的表情符号和除文字以外的所有符号
for user in Users:
    signature = user['Signature'].strip().replace('span', '')\
        .replace('class', '').replace('emoji', '')
    rep = re.compile('1f\d+\w*|[<>/=]')
    signature = rep.sub('', signature)
    if len(signature.strip()) > 0:
        signature_list.append(signature)
#  对个性签名进行分词处理
text = ''.join(signature_list)
signature_seg = jieba.cut(text)
signature_seg = ' '.join(signature_seg)
# 绘制词云图

bimg = imread('data/ChineseMap.png')
wordCloud = WordCloud(
    background_color='white', # 背景颜色
    font_path='data/simhei.ttf', # 设置字体可以显示中文
    stopwords='data/StopwordsCN.txt',
    mask=bimg # 设置背景图片
)

wordCloud = wordCloud.generate(signature_seg)
bimgColors = ImageColorGenerator(bimg)
fig=plt.figure(3)
plt.imshow(wordCloud.recolor(color_func=bimgColors))
plt.axis("off")
plt.show()
