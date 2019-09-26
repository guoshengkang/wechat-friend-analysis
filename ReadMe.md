## 功能介绍
通过简单的数据分析了解微信好友的总体情况


## 具体功能
1. 同好友性别分别，省份及城市分布，生成好友签名的词云
2. 生成好友头像的照片墙
3. 根据个性签名对好友进行聚类
## 功能1
1. 安装包
 * itchat
 * jieba
 * wordcloud
2. 使用说明
 * 运行文件[WeChat_friend_statistics.py](WeChat_friend_statistics.py)
 * 手机微信扫码并确认登录， 当前目录会生成itchat.pkl文件，用于保存登录状态，下次运行直接手机确认即可。如需换号登录，可以先将该文件删除
 * 运行结果会保存memberList.csv文件，包含好友的如下信息：

|  NickName   | Sex  | Province  | City  | Signature  |
|  :----:  | :----:  | :----:  | :----:  | :----:  |
| 叶落倾城  | 1 | 湖南 | 邵阳 | 盼望着，离回家的路似乎还很漫长，等我，等我 |
| 。。。  |。。。  |。。。  |。。。  |。。。  |

 * 运行结果会弹出3张图：好友性别分布的饼图、好友省份及城市分布的柱状图、好友签名的词云图
<div align=center><img width="400" height="200" src="data/好友性别分布.png"/></div>
<div align=center><img width="400" height="200" src="data/好友省份及城市分布.png"/></div>
<div align=center><img width="400" height="200" src="data/签名词云.png"/></div>