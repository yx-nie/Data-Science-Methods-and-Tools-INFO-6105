#!/usr/bin/env python
# coding: utf-8

# Importing Libraries

# In[1]:


import pandas as pd
import os
from math import pow, sqrt
from copy import deepcopy
import content_based2 


# Reading dataset

# In[2]:


ratings = pd.read_csv('./ratings.csv')


# Data preprocessing

# In[3]:


#Reading ratings.csv obtains the data dictionary in the format {userid:{movieid:rating, movieid:rating}}
file = open('./ratings.csv','r',encoding='utf-8')

data = {}
linenum=0
for line in file.readlines():

    if linenum==0:
        linenum+=1
        continue
    line = line.strip().split(',')

    if not line[0] in data.keys():
        data[line[0]] = {line[1]:float(line[2])}

    else:
        data[line[0]][line[1]] = float(line[2])

data_dict=data
#print(data_dict)


# Calculate the cos similarity between two users

# In[4]:


def calculate_cos(user1,user2,data):
    user1_data = data[user1]
    user2_data = data[user2]
    # print("user1_data: ",user1_data)
    # print("user2_data: ",user2_data)
    Molecular=0
    for key in user1_data.keys():
        if key in user2_data.keys():
            Molecular += float(user1_data[key])*float(user2_data[key])
    rxdistance=0
    for key in user1_data.keys():
        rxdistance += user1_data[key]*user1_data[key]
    rxdistance=sqrt(rxdistance)
    rydistance=0
    for key in user2_data.keys():
        rydistance += user2_data[key] * user2_data[key]
    rydistance = sqrt(rydistance)

    cos=Molecular/(rxdistance*rydistance)
    return cos


# Find the user most similar to this user

# In[5]:


def most_similar(userID,data):
    res = []
    for userid in data.keys():
        if not userid == userID:
            sim = calculate_cos(userID,userid,data)
            res.append((userid, sim))
    res.sort(key=lambda val: val[1], reverse=True)

    return res[0]


# Obtain the most similar user list for each user

# In[6]:


def get_similar_list(data):
    record={}
    for key in data.keys():
        res=most_similar(key,data)
        record[key]=res
    return record


# In[7]:


similar_list=get_similar_list(data_dict)
print(similar_list)


# Get high score movies from users who are most similar to users and recommend them to users

# In[8]:


def recommend(user):
    recomm = []
    most_sim=similar_list[user][0]
    sim=similar_list[user][1]
    
    # When the highest similarity is less than 0.2, it is considered that there is no user similar to the user, return -1
    if sim< 0.2:
        return -1
  
    # When similar users have not seen a movie that is different from this user and has a score of more than 4 points, return - 1
    items = data_dict[most_sim]   
    for item in items.keys():
        if item not in data_dict[user].keys() and items[item]>4.0:
            recomm.append((item, items[item]))

    if(len(recomm)==0):
        return -1
    
    recomm.sort(key=lambda val: val[1], reverse=True)

    # When the number of recommended films is less than 3, it is recommended directly; when it is more than 3, only the first 3 films are recommended
    if(len(recomm)<3):
        return {user:recomm}
    else:
        return {user:recomm[:3]}


# In[9]:


recommend('150')


# Collaborative + Content-based

# In[10]:


def run():   
    results={}
    for key in similar_list.keys():
        # print(similar_list[key][1])
        result=recommend(key)
        # CF algorithm is used when the result is not equal to - 1
        if result!=-1:
            results.update(result)
        # CB algorithm is used when result is equal to - 1
        else:
            result=content_based2.recommend(key)
            results.update(result)

    return results


# Return Results {'UserID':[('MovieID', rating)]}

# In[11]:


run()


# In[ ]:




