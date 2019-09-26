from wxpy import *
import PIL.Image as Image
import os
import sys
#登陆微信
bot = Bot()
#获取当前路径
curr_dir = os.path.abspath(sys.argv[0])
#创建文件夹，用来放照片
if not os.path.exists("FriendImages/"):
    os.mkdir("FriendImages/")
#获取朋友的头像
my_friends = bot.friends(update=True)
n = 0 
for friend in my_friends:
    friend.get_avatar("FriendImages/" + str(n) + ".jpg")
    n = n+1
#首先设定照片墙的大小，尺寸（650*650）
image = Image.new("RGB",(850,850))
x = 0 
y = 0
#获取之前放照片的位置
curr_dir = os.path.abspath(sys.argv[0])
#逐个获取照片
ls = os.listdir("FriendImages")
for file_names in ls:
    try:
        img = Image.open("FriendImages/" + file_names)
    except IOError:
        continue
    else:
        #设定好友头像的大小，为50*50
        img = img.resize((50,50),Image.ANTIALIAS)
        image.paste(img,(x*50,y*50))
        x += 1
        if x ==17:
            x = 0
            y += 1
img = image.save("wechat_friend_wall.jpg")
#最终生成17*17个头像的一个照片墙