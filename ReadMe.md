## 功能介绍
通过简单的数据分析了解微信好友的总体情况


## 具体功能
1. 同好友性别分别，省份及城市分布，生成好友签名的词云
2. 生成好友头像的照片墙
3. 根据个性签名对好友进行聚类

## 功能1：好友统计
1. **安装包**
 * itchat
 * jieba
 * wordcloud
2. **使用说明**
 * 运行文件 [WeChat_friend_statistics.py](WeChat_friend_statistics.py)
 * 手机微信扫码并确认登录， 当前目录会生成[itchat.pkl](itchat.pkl)文件，用于保存登录状态，下次运行直接手机确认即可。如需换号登录，可以先将该文件删除
 * 运行结果会保存[memberList.csv](memberList.csv)文件，包含好友的如下信息：昵称、性别（0-未知，1-男，2-女）、省份、城市、签名

|  NickName   | Sex  | Province  | City  | Signature  |
|  :----:  | :----:  | :----:  | :----:  | :----:  |
| **nickName**  | 1 | 湖南 | 邵阳 | 盼望着，离回家的路似乎还很漫长，等我，等我 |
| ...  |...。  |...  |...  |...  |

 * 运行结果会弹出3张图：好友性别分布的饼图、好友省份及城市分布的柱状图、好友签名的词云图
<div align=center><img width="800" height="400" src="data/好友性别分布.png"/></div>
<div align=center><img width="800" height="400" src="data/好友省份及城市分布.png"/></div>
<div align=center><img width="800" height="400" src="data/签名词云.png"/></div>

## 功能2：好友头像照片墙
1. **安装包**
 * wxpy
 * PIL
2. **使用说明**
 * 运行文件 [wechat_friend_wall.py](wechat_friend_wall.py)
 * 手机微信扫码并确认登录后， 再当前目录会生成照片墙图片文件[wechat_friend_wall.jpg](wechat_friend_wall.jpg)
<div align=center><img width="800" height="800" src="data/签名词云.png"/></div>
注：为保护隐私，上传的好友照片墙图片已被模糊化处理
## 功能3：好友聚类

注：为保护隐私，本项目上传文件的好友昵称均用"**nickName**"代替