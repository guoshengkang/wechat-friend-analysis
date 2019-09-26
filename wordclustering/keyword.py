#!/usr/bin/python
#-*-coding:utf-8-*-


import sys
reload(sys)
sys.setdefaultencoding('utf8')
import random
import copy
import os
import re
import pprint
import math
import random


def replace_word(file_name):
    file_data=open(file_name,"r")
    key_re=re.compile(r"(^.+):")
    value_re=re.compile(r":(.+$)")
    result={}
    while True:
        char_line = file_data.readline()
        if not char_line:
            break
        char_line = unicode(char_line.strip("\n"),"utf-8")
        key_word = key_re.findall(char_line)
        value_word = value_re.findall(char_line)
        value_word = value_word[0].split(",")
        for i in value_word:
            result.setdefault(i,"^!"+key_word[0])
    return result


def readdata(file_name,split_char,remove_word,replace_word):
    result={"id":[],"word_list":[],"key_word":{}}
    num=0
    try:
        source_data=open(file_name)
    except:
        print "not vail file"
    while True:
        num+=1
        char1=source_data.readline()
        if random.uniform(0,1)<=0.0:
            continue
        chars=unicode(char1.strip('\n'),"utf-8")
        if not char1:
            break
        chars=chars.split(",")
        word_list=chars[1].split(split_char)
        word_list=[i for i in word_list if len(i)>0]
        # for i in set(word_list): 
        for i in word_list:#修改不去重
            fag = 0
            if i in remove_word:
                continue
            r_key_word=replace_word.get(i)
            if r_key_word:
                word_list.append(r_key_word)
                if not result["key_word"].has_key(r_key_word):
                    result["key_word"][r_key_word] = [random.uniform(0, 100), 0]
                result["key_word"][r_key_word][1] += 1
            for hh in i :
                if (u'\u4e00' <= hh <= u'\u9fff') :
                    fag += 1
                elif (hh >= u'\u0041' and hh<=u'\u005a') :
                    fag += 1
                elif (hh >= u'\u0061' and hh<=u'\u007a'):
                    fag += 1
            if fag>=1 :
                if not result["key_word"].has_key(i):
                    result["key_word"][i]=[random.uniform(0,100),0]
                result["key_word"][i][1]+=1
        result["word_list"].append(word_list)
        result["id"].append(chars[0])
    print len(result["key_word"])
    result["key_word"] = {i: result["key_word"][i] for i in result["key_word"] if result["key_word"][i][1] >= 10}
    print len(result["key_word"])
    return result

def nitializationi_seed(word_items,cluster_num):
    items=sorted(word_items.items(),key=lambda x:x[1][1],reverse=True)
    result={"key_word":{},"key_tfidf":{}}
    for i in xrange(cluster_num):
        lim_low=100.00/cluster_num*i
        lim_up=100.00/cluster_num*(i+1)
        result["key_word"][i]= [j[0] for j in items if j[1][0]>=lim_low and j[1][0]<lim_up and j[1][1]>20]
        result["key_tfidf"][i]=[1]*len(result["key_word"][i])
    return result


def clustering(cluster_seed,key_tfidf,cluster_data,id_data):
    cut_lev=1
    cut_lev=max(0.5,cut_lev*0.97)
    cluster_result={"dist":{},"undis":[],"id":{}}
    seeds={}
    for j in cluster_seed:
        seeds[j]={cluster_seed[j][i]:key_tfidf[j][i] for i in xrange(len(cluster_seed[j]))}
    cluster_data_num=len(cluster_data)
    for i in xrange(cluster_data_num):
        cluster_munber = set(cluster_data[i])
        distance = []
        for j in cluster_seed:
            join = sum([seeds[j][hh] for hh in seeds[j].keys() if hh in cluster_munber])
            union = sum(seeds[j].values())
            hl = 1-join/(union+0.0001)
            distance.append(hl)
        if len(distance)==0:
            print "|".join(i).encode("utf-8")
            print cluster_seed
        if  min(distance)>=cut_lev:
            cluster_result["undis"].append(cluster_data[i])
        else:
            cluster_id=distance.index(min(distance))
            if not cluster_result["dist"].has_key(cluster_id):
                cluster_result["dist"][cluster_id]=[]
                cluster_result["id"][cluster_id]=[]
            cluster_result["dist"][cluster_id].append(cluster_data[i])
            cluster_result["id"][cluster_id].append(id_data[i])
    return cluster_result


def find_seed(key_word,cluster_data,lim_num,total_lines,keys_num):
    result_tmp={}
    result={"tfidf":{},"key_word":{},"key_tfidf":{}}
    for i in key_word:
        if key_word[i][1]<=lim_num:
            continue
        for j in cluster_data:
            if not result_tmp.has_key(j):
                result_tmp[j]={}
            j_num=0
            ij_num=0
            for h in cluster_data[j]:
                ij_num+=h.count(i)
                j_num+=len(h)
            tfidf=(ij_num*1.000/j_num)*math.log(total_lines*1.00/(key_word[i][1]+1))
            if tfidf>0:
                result_tmp[j][i]=tfidf
    for j in result_tmp:
        r_len=len(result_tmp[j])
        keys_len=min(r_len,keys_num)
        tmp=sorted(result_tmp[j].items(),key=lambda x:x[1],reverse=True)
        result["key_word"][j]=[i[0] for i in tmp[0:keys_len]]
        result["key_tfidf"][j] = [i[1] for i in tmp[0:keys_len]]
        result["tfidf"][j]=sum([i[1] for i in tmp[0:keys_len]])/keys_len

    return result

def train_model(raw_data,id_data,key_word,cluster_num,keyword_num,iter_max):
    total_tfidf1 = 0.001
    total_line = len(raw_data)
    result={}
    for h in xrange(iter_max):
        if h==0:
            gseeds = nitializationi_seed(key_word, cluster_num)
            print "nitializationi_seed"
            seeds = gseeds["key_word"]
            seedt = gseeds["key_tfidf"]
        else:
            gseeds =find_seed(key_word,clus["dist"],15,total_line,keyword_num)
            print ("find_seed",h)
            seeds = gseeds["key_word"]
            seedt = gseeds["key_tfidf"]
            total_tfidf0=copy.deepcopy(total_tfidf1)
            total_tfidf1=sum([fg[1] for fg in gseeds["tfidf"].items()])
            diff_tfidf=total_tfidf1/total_tfidf0-1
            print (h,total_tfidf1,diff_tfidf)
            if abs(diff_tfidf)<=0.000001:
                break
        clus = clustering(seeds,seedt,raw_data,id_data)
        print ("clustering",h)
    clus_num={}
    for i in clus["dist"]:
        clus_num[i]=len(clus["dist"][i])
    result["seeds"]=gseeds
    result["seeds"]["num"]=clus_num
    result["cluster"]=clus
    return result

if __name__ == '__main__':

    file_path = os.path.join(os.getcwd(), "sourcedata")
    file_name = os.path.join(file_path, "source_file")
    remove_file = os.path.join(file_path, "keyword_remove")
    replace_file = os.path.join(file_path, "replace_word")
    replace_words = replace_word(replace_file)
    remove=open(remove_file,"r")
    remove_word=[]
    while True:
        lis=remove.readline()
        if not lis:
            break
        remove_word.append(unicode(lis.strip('\n'),"utf-8"))
    s=readdata(file_name,"|",remove_word,replace_words)
    t=train_model(s["word_list"],s["id"],s["key_word"],10,10,60)

    cluster_gender=os.path.join(file_path,"gender")
    gender=open(cluster_gender,"w")
    cluster_keyword=os.path.join(file_path,"keyword")
    keyword = open(cluster_keyword, "w")
    cluster_result=os.path.join(file_path,"result")
    result = open(cluster_result, "w")

    keyword_vaild=[]
    for l in t["seeds"]["key_word"]:
        for i in xrange(len(t["seeds"]["key_word"][l])):
            keyword_vaild.append(t["seeds"]["key_word"][l][i])
            char_line=str(l) + "\t" + t["seeds"]["key_word"][l][i] + "\t" + str(t["seeds"]["key_tfidf"][l][i]) + "\n"
            keyword.write(char_line.encode("utf-8"))
    keyword.close()

    for l in t["seeds"]["tfidf"]:
        char_line=str(l) + "\t" + str(t["seeds"]["tfidf"][l])+"\t"+str(t["seeds"]["num"][l])+"\n"
        gender.write(char_line.encode("utf-8"))
    gender.close()

    keyword_total=set(keyword_vaild)
    for l in t["cluster"]["dist"]:
        cluster_dist_num=len(t["cluster"]["dist"][l])
        for i in xrange(cluster_dist_num):
            k_i = t["cluster"]["dist"][l][i]
            d_i = t["cluster"]["id"][l][i]
            keyword=set(k_i)&set(t["seeds"]["key_word"][l])
            keyword_diff = set(k_i)&(keyword_total - set(t["seeds"]["key_word"][l]))
            char_line=str(l)+"\t"+d_i+"\t"+"|".join(k_i)+"\t"+"|".join(list(keyword))+"\t"+"|".join(list(keyword_diff))+"\n"
            result.write(char_line.encode("utf-8"))
    for i in t["cluster"]["undis"]:
        char_line="undis"+"\t"+"|".join(i)+"\n"
        result.write(char_line.encode("utf-8"))
    result.close()
