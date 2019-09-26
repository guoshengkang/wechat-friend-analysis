#!/usr/bin/python
# -+- coding: utf-8 -+-
import re,os
import sys,io
from jieba_cut import seg_sentence

fout1=open("wordclustering\\sourcedata\\source_file","w",encoding="UTF-8")
fout2=open("No_NickName_Signature.csv","w")
f=open("memberList.csv",encoding="UTF-8")
f.readline()
lines=f.readlines()
for No, line in enumerate(lines):
	line=line.encode("gbk", "ignore").decode("gbk")
	# 将Unicode编码转换成gbk编码，在转换的过程中通过“ignore”忽略掉gbk不能识别的字符（😒），
	# 然后再把gbk转换成Unicode编码,毕竟牺牲部分字符串。
	line=line.strip("\r\n")
	NickName,Sex,Province,City,Signature=line.split(',',4)
	Signature=re.sub(r'<span.*/span>','',Signature)
	keyword_list=seg_sentence(Signature)
	write_line1=','.join([str(No),keyword_list])
	fout1.write(write_line1+'\n')
	write_line2=','.join([str(No),NickName,Signature])
	fout2.write(write_line2+'\n')
