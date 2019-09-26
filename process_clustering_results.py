#!/usr/bin/python
# -+- coding: utf-8 -+-
import re,os

#找到各ID的类别
fin1=open("wordclustering\\sourcedata\\result",encoding="UTF-8")
class_dict=dict() # {'16': '0', '20': '1', '25': '1',...}
for line in fin1.readlines():
	line=line.encode("gbk", "ignore").decode("gbk")
	line=line.strip("\r\n")
	field_list=line.split("\t")
	if len(field_list)==5:
		class_dict[field_list[1]]=field_list[0]

# 将同类昵称、签名放在一起
cluster_dict={}
cluster_dict["unknown"]=[]
fin2=open("No_NickName_Signature.txt")
for line in fin2.readlines():
	line=line.encode("gbk", "ignore").decode("gbk")
	line=line.strip("\r\n")
	No,NickName,Signature=line.split(",",2)
	if No in class_dict:
		if class_dict[No] in cluster_dict:
			cluster_dict[class_dict[No]].append("\t".join([NickName,Signature]))
		else:
			cluster_dict[class_dict[No]]=[]
			cluster_dict[class_dict[No]].append("\t".join([NickName,Signature]))
	else:
		cluster_dict["unknown"].append("\t".join([NickName,Signature]))

class_ids=list(cluster_dict.keys())
class_ids.sort() # 升序排序 ['0', '1', '2', '3', 'unknown']
fout=open("cluster_result.txt","w")
for no, class_id in enumerate(class_ids):
	first_line="【第{}类({})有位{}好友，如下】".format(no,class_id,len(cluster_dict[class_id]))
	fout.write(first_line+"\n")
	for NickName_Signature in cluster_dict[class_id]:
		fout.write(NickName_Signature+"\n")
	fout.write("\n"+"="*30+"\n")

