#!/usr/bin/env python
# coding: utf-8

# Importing Libraries

# In[1]:


from __future__ import division
import os
import operator
from tqdm import tqdm
from time import sleep


# Reading dataset

# In[2]:


if not os.path.exists('./ratings.csv'):
    data = {}
    
linenum = 0
data = []
fp = open('./ratings.csv')
for line in fp:

    if linenum == 0:
        linenum += 1
        continue
    item = line.strip().split(",")
    data.append([item[0], item[1], float(item[2]), int(item[3])])

fp.close()

#print(data)


# Average score of each movie

# In[3]:


record = {}
score = {}
linenum = 0
fp = open("./ratings.csv",encoding='utf-8')
for line in fp:
    if linenum == 0:
        linenum += 1
        continue
    item = line.strip().split(",")

    userid, itemid, rating = item[0],item[1],float(item[2])
    if itemid not in record:
        record[itemid] = [0,0]
    record[itemid][0] += rating
    record[itemid][1] += 1
fp.close()

for itemid in record:
    score[itemid] = round(record[itemid][0]/record[itemid][1],3)
    
avg_score=score
#print(avg_score)


# Get the ranking of movies with different genres and the genres ratio of each movie

# In[4]:


'''
genres_ratio： the genres ratio of each movie
genres_rating_sort: the ranking of movies with different genres

'''
record = {}
genres_ratio = {}
genres_rating_sort = {}
linenum = 0
topk = 100

if not os.path.exists("./movies.csv"):
    genres_ratio = {}
    genres_rating_sort = {}

fp = open("./movies.csv",encoding='utf-8')
for line in fp:
    if linenum == 0:
        linenum += 1
        continue
    item = line.strip().split(",")
    if(len(item) < 3):
        continue
    itemid = item[0]
    cate_str = item[-1]
    cate_list = cate_str.strip().split("|")
    ratio = round(1/len(cate_list),3)
    if itemid not in genres_ratio:
        genres_ratio[itemid] = {}
    for fix_cate in cate_list:
        genres_ratio[itemid][fix_cate] = ratio
fp.close()
     
for itemid in genres_ratio:
    for cate in genres_ratio[itemid]:
        if cate not in record:
            record[cate] = {}
        itemid_rating_score = avg_score.get(itemid,0)
        record[cate][itemid] = itemid_rating_score
for cate in record:
    if cate not in genres_rating_sort:
        genres_rating_sort[cate] = []
    for combo in sorted(record[cate].items(),key=operator.itemgetter(1),reverse=True)[:topk]:
        genres_rating_sort[cate].append((combo[0],float(combo[1])))
            
#print(genres_ratio)


# In[5]:


print(genres_rating_sort)


# Obtain the timestamp with the largest value to calculate the timestamp weight

# In[6]:


linenum = 0
largest_time = 0
fp = open("./ratings.csv",encoding='utf-8')
for line in fp:
    if linenum == 0:
        linenum += 1
        continue
    item = line.strip().split(",")
    if len(item) < 4:
        continue
    timestamp = int(item[3])
    if timestamp > largest_time:
        largest_time = timestamp
fp.close()

print(largest_time)


# Return score of time

# In[7]:


def get_time_score(time):

    fix_time_stamp = int(largest_time)
    total_sec = 24*60*60
    delta = (fix_time_stamp-time)/total_sec/100
    return round(1/(1+delta),3)


# Get users' genres popularity list

# In[8]:


'''
Genres popularity = genres original weight of the movie * user rating of the movie * time weighting
Where, the original weight of the movie = 1/the number of genres of the movie
       time weighting = normalization of timestamps
'''

def get_user_tags(item_cate,data):

    record = {}
    user_tags = {}
    topk = 2  #Find the top two favorite movie genres of users

    for item in tqdm(data):
        sleep(0.1)
        userid, itemid, rating, time=item[0],item[1],item[2],item[3]
        # When ratings less than 4 on movies, they will not participate in the calculation of genres popularity
        if rating < 4:
            continue
        # Map the timestamp to a 0-1 weighted number
        time_score = get_time_score(time)
        if userid not in record:
            record[userid] = {}
        for fix_cate in item_cate[itemid]:
            if fix_cate not in record[userid]:
                record[userid][fix_cate] = 0
            record[userid][fix_cate] += rating * time_score * item_cate[itemid][fix_cate]

    # Calculate the top two favorite movie genres of users, and map the sum of the two proportions to 1, so as to recommend the number of movies according to the proportion
    for userid in tqdm(record):
        sleep(0.1)
        if userid not in user_tags:
            user_tags[userid]=[]
        total = 0
        for combo in sorted(record[userid].items(),key=operator.itemgetter(1),reverse=True)[:topk]:
            user_tags[userid].append((combo[0],combo[1]))
            total += combo[1]
        for index in range(len(user_tags[userid])):
            user_tags[userid][index] = (user_tags[userid][index][0],round(user_tags[userid][index][1]/total,3))
    return user_tags



# In[9]:


#user_tags = get_user_tags(genres_ratio,data)


# In[10]:


#print(user_tags)


# In[13]:



user_tags={'1': [('Drama', 0.545), ('Thriller', 0.455)], '2': [('Drama', 0.629), ('Thriller', 0.371)], '3': [('Drama', 0.577), ('Comedy', 0.423)], '4': [('Drama', 0.726), ('Comedy', 0.274)], '5': [('Comedy', 0.679), ('Animation', 0.321)], '6': [('Drama', 0.537), ('Comedy', 0.463)], '7': [('Action', 0.607), ('Thriller', 0.393)], '8': [('Drama', 0.744), ('Comedy', 0.256)], '9': [('Comedy', 0.506), ('Drama', 0.494)], '10': [('Comedy', 0.512), ('Drama', 0.488)], '11': [('Adventure', 0.562), ('Action', 0.438)], '12': [('Comedy', 0.625), ('Romance', 0.375)], '13': [('Drama', 0.515), ('Thriller', 0.485)], '14': [('Comedy', 0.7), ('Adventure', 0.3)], '15': [('Drama', 0.589), ('Comedy', 0.411)], '16': [('Action', 0.503), ('Thriller', 0.497)], '17': [('Comedy', 0.56), ('Adventure', 0.44)], '18': [('Thriller', 0.572), ('Drama', 0.428)], '19': [('Drama', 0.86), ('War', 0.14)], '20': [('Drama', 0.629), ('Romance', 0.371)], '21': [('Adventure', 0.563), ('Drama', 0.437)], '22': [('Drama', 0.581), ('Comedy', 0.419)], '23': [('Drama', 0.566), ('Thriller', 0.434)], '24': [('Drama', 0.715), ('Thriller', 0.285)], '25': [('Comedy', 0.797), ('Romance', 0.203)], '26': [('Drama', 0.608), ('Crime', 0.392)], '27': [('Comedy', 0.737), ('Drama', 0.263)], '28': [('Drama', 0.574), ('Comedy', 0.426)], '29': [('Thriller', 0.538), ('Action', 0.462)], '30': [('Action', 0.516), ('Adventure', 0.484)], '31': [('Drama', 0.72), ('Crime', 0.28)], '32': [('Drama', 0.685), ('Comedy', 0.315)], '33': [('Drama', 0.743), ('Comedy', 0.257)], '34': [('Comedy', 0.638), ('Drama', 0.362)], '35': [('Comedy', 0.574), ('Thriller', 0.426)], '36': [('Drama', 0.548), ('Thriller', 0.452)], '37': [('Drama', 0.634), ('Crime', 0.366)], '38': [('Drama', 0.625), ('Comedy', 0.375)], '39': [('Drama', 0.57), ('Adventure', 0.43)], '40': [('Comedy', 0.632), ('Action', 0.368)], '41': [('Comedy', 0.587), ('Drama', 0.413)], '42': [('Comedy', 0.58), ('Drama', 0.42)], '43': [('Drama', 0.803), ('Comedy', 0.197)], '44': [('Drama', 0.515), ('Comedy', 0.485)], '45': [('Drama', 0.513), ('Comedy', 0.487)], '46': [('Drama', 0.732), ('Comedy', 0.268)], '47': [('Drama', 0.769), ('Crime', 0.231)], '48': [('Drama', 0.579), ('Comedy', 0.421)], '49': [('Crime', 0.51), ('Thriller', 0.49)], '50': [('Drama', 0.711), ('Comedy', 0.289)], '51': [('Thriller', 0.521), ('Action', 0.479)], '52': [('Drama', 0.504), ('Comedy', 0.496)], '53': [('Comedy', 0.616), ('Drama', 0.384)], '54': [('Drama', 0.658), ('Action', 0.342)], '55': [('Comedy', 0.636), ('Drama', 0.364)], '56': [('Drama', 0.726), ('Crime', 0.274)], '57': [('Drama', 0.682), ('Comedy', 0.318)], '58': [('Thriller', 0.667), ('Action', 0.333)], '59': [('Comedy', 0.507), ('Sci-Fi', 0.493)], '60': [('Comedy', 0.542), ('Drama', 0.458)], '61': [('Drama', 0.774), ('Comedy', 0.226)], '62': [('Drama', 0.67), ('Thriller', 0.33)], '63': [('Drama', 0.657), ('Comedy', 0.343)], '64': [('Comedy', 0.51), ('Drama', 0.49)], '65': [('Drama', 0.554), ('Thriller', 0.446)], '66': [('Drama', 0.503), ('Comedy', 0.497)], '67': [('Drama', 0.525), ('Comedy', 0.475)], '68': [('Drama', 0.717), ('Romance', 0.283)], '69': [('Drama', 0.681), ('Action', 0.319)], '70': [('Drama', 0.614), ('Comedy', 0.386)], '71': [('Drama', 0.54), ('Thriller', 0.46)], '72': [('Comedy', 0.531), ('Drama', 0.469)], '73': [('Drama', 0.621), ('Thriller', 0.379)], '74': [('Thriller', 0.595), ('Drama', 0.405)], '75': [('Comedy', 0.577), ('Drama', 0.423)], '76': [('Drama', 0.565), ('Adventure', 0.435)], '77': [('Drama', 0.592), ('Comedy', 0.408)], '78': [('Action', 0.565), ('Adventure', 0.435)], '79': [('Drama', 0.674), ('Crime', 0.326)], '80': [('Drama', 0.656), ('Crime', 0.344)], '81': [('Comedy', 0.537), ('Animation', 0.463)], '82': [('Drama', 0.677), ('Crime', 0.323)], '83': [('Comedy', 0.531), ('Action', 0.469)], '84': [('Drama', 0.624), ('Comedy', 0.376)], '85': [('Drama', 0.736), ('Crime', 0.264)], '86': [('Drama', 0.647), ('Thriller', 0.353)], '87': [('Drama', 0.771), ('Thriller', 0.229)], '88': [('Drama', 0.51), ('Comedy', 0.49)], '89': [('Comedy', 0.552), ('Adventure', 0.448)], '90': [('Comedy', 0.774), ('Action', 0.226)], '91': [('Drama', 0.85), ('Romance', 0.15)], '92': [('Drama', 0.587), ('Thriller', 0.413)], '93': [('Drama', 0.612), ('Comedy', 0.388)], '94': [('Horror', 0.597), ('Thriller', 0.403)], '95': [('Drama', 0.579), ('Romance', 0.421)], '96': [('Comedy', 0.55), ('Drama', 0.45)], '97': [('Adventure', 0.549), ('Sci-Fi', 0.451)], '98': [('Thriller', 0.565), ('Drama', 0.435)], '99': [('Comedy', 0.513), ('Drama', 0.487)], '100': [('Drama', 0.7), ('Adventure', 0.3)], '101': [('Comedy', 0.564), ('Drama', 0.436)], '102': [('Drama', 0.657), ('Comedy', 0.343)], '103': [('Drama', 0.625), ('Comedy', 0.375)], '104': [('Comedy', 0.532), ('Drama', 0.468)], '105': [('Drama', 0.542), ('Romance', 0.458)], '106': [('Action', 0.526), ('Drama', 0.474)], '107': [('Drama', 0.541), ('Comedy', 0.459)], '108': [('Comedy', 0.715), ('Action', 0.285)], '109': [('Comedy', 0.512), ('Drama', 0.488)], '110': [('Comedy', 0.523), ('Drama', 0.477)], '111': [('Drama', 0.603), ('Comedy', 0.397)], '112': [('Drama', 0.631), ('Comedy', 0.369)], '113': [('Drama', 0.588), ('Comedy', 0.412)], '114': [('Sci-Fi', 0.502), ('Adventure', 0.498)], '115': [('Comedy', 0.611), ('Drama', 0.389)], '116': [('Thriller', 0.633), ('Drama', 0.367)], '117': [('Drama', 0.546), ('Thriller', 0.454)], '118': [('Drama', 0.544), ('Comedy', 0.456)], '119': [('Drama', 0.56), ('Thriller', 0.44)], '120': [('Drama', 0.517), ('Comedy', 0.483)], '121': [('Comedy', 0.524), ('Drama', 0.476)], '122': [('Drama', 0.512), ('Thriller', 0.488)], '123': [('Comedy', 0.665), ('Romance', 0.335)], '124': [('Drama', 0.656), ('Comedy', 0.344)], '125': [('Comedy', 0.795), ('Adventure', 0.205)], '126': [('Thriller', 0.509), ('Drama', 0.491)], '127': [('Drama', 0.722), ('Action', 0.278)], '128': [('Drama', 0.533), ('Comedy', 0.467)], '129': [('Thriller', 0.62), ('Drama', 0.38)], '130': [('Drama', 0.775), ('Comedy', 0.225)], '131': [('Drama', 0.765), ('Romance', 0.235)], '132': [('Drama', 0.723), ('Comedy', 0.277)], '133': [('Drama', 0.549), ('Comedy', 0.451)], '134': [('Comedy', 0.505), ('Drama', 0.495)], '135': [('Drama', 0.7), ('Comedy', 0.3)], '136': [('Drama', 0.584), ('Sci-Fi', 0.416)], '137': [('Drama', 0.684), ('Comedy', 0.316)], '138': [('Drama', 0.612), ('Comedy', 0.388)], '139': [('Drama', 0.724), ('Comedy', 0.276)], '140': [('Drama', 0.778), ('Romance', 0.222)], '141': [('Adventure', 0.536), ('Action', 0.464)], '142': [('Comedy', 0.556), ('Romance', 0.444)], '143': [('Drama', 0.519), ('Action', 0.481)], '144': [('Drama', 0.641), ('Romance', 0.359)], '145': [('Drama', 0.744), ('Crime', 0.256)], '146': [('Drama', 0.633), ('Comedy', 0.367)], '147': [('Drama', 0.643), ('Comedy', 0.357)], '148': [('Drama', 0.586), ('Comedy', 0.414)], '149': [('Drama', 0.635), ('Comedy', 0.365)], '150': [('Drama', 0.589), ('Comedy', 0.411)], '151': [('Drama', 0.536), ('Comedy', 0.464)], '152': [('Action', 0.609), ('Adventure', 0.391)], '153': [('Drama', 0.654), ('Crime', 0.346)], '154': [('Drama', 0.655), ('Comedy', 0.345)], '155': [('Drama', 0.567), ('Comedy', 0.433)], '156': [('Comedy', 0.547), ('Drama', 0.453)], '157': [('Action', 0.584), ('Sci-Fi', 0.416)], '158': [('Drama', 0.527), ('Action', 0.473)], '159': [('Drama', 0.501), ('Adventure', 0.499)], '160': [('Drama', 0.761), ('Romance', 0.239)], '161': [('Thriller', 0.521), ('Action', 0.479)], '162': [('Drama', 0.517), ('Thriller', 0.483)], '163': [('Drama', 0.703), ('Thriller', 0.297)], '164': [('Drama', 0.525), ('Action', 0.475)], '165': [('Drama', 0.698), ('Thriller', 0.302)], '166': [('Drama', 0.596), ('Thriller', 0.404)], '167': [('Drama', 0.77), ('Comedy', 0.23)], '168': [('Drama', 0.598), ('Comedy', 0.402)], '169': [('Drama', 0.677), ('Thriller', 0.323)], '170': [('Drama', 0.652), ('Comedy', 0.348)], '171': [('Comedy', 0.635), ('Drama', 0.365)], '172': [('Drama', 0.651), ('Romance', 0.349)], '173': [('Comedy', 0.513), ('Drama', 0.487)], '174': [('Comedy', 0.509), ('Drama', 0.491)], '175': [('Drama', 0.566), ('Sci-Fi', 0.434)], '176': [('Action', 0.529), ('Adventure', 0.471)], '177': [('Drama', 0.57), ('Comedy', 0.43)], '178': [('Thriller', 0.58), ('Action', 0.42)], '179': [('Drama', 0.718), ('Comedy', 0.282)], '180': [('Drama', 0.555), ('Comedy', 0.445)], '181': [('Comedy', 0.665), ('Adventure', 0.335)], '182': [('Drama', 0.761), ('Crime', 0.239)], '183': [('Drama', 0.535), ('Comedy', 0.465)], '184': [('Drama', 0.61), ('Comedy', 0.39)], '185': [('Action', 0.687), ('Comedy', 0.313)], '186': [('Drama', 0.524), ('Thriller', 0.476)], '187': [('Comedy', 0.622), ('Drama', 0.378)], '188': [('Drama', 0.533), ('Comedy', 0.467)], '189': [('Drama', 0.76), ('Thriller', 0.24)], '190': [('Comedy', 0.51), ('Drama', 0.49)], '191': [('Comedy', 0.598), ('Drama', 0.402)], '192': [('Drama', 0.706), ('Comedy', 0.294)], '193': [('Sci-Fi', 0.546), ('Action', 0.454)], '194': [('Drama', 0.522), ('Romance', 0.478)], '195': [('Drama', 0.6), ('Comedy', 0.4)], '196': [('Drama', 0.593), ('Thriller', 0.407)], '197': [('Drama', 0.559), ('Comedy', 0.441)], '198': [('Drama', 0.624), ('Comedy', 0.376)], '199': [('Sci-Fi', 0.696), ('Adventure', 0.304)], '200': [('Thriller', 0.552), ('Drama', 0.448)], '201': [('Comedy', 0.614), ('Drama', 0.386)], '202': [('Drama', 0.568), ('Comedy', 0.432)], '203': [('Drama', 0.637), ('Comedy', 0.363)], '204': [('Drama', 0.78), ('Crime', 0.22)], '205': [('Drama', 0.675), ('Thriller', 0.325)], '206': [('Drama', 0.691), ('Action', 0.309)], '207': [('Drama', 0.713), ('Comedy', 0.287)], '208': [('Drama', 0.52), ('Thriller', 0.48)], '209': [('Drama', 0.651), ('Romance', 0.349)], '210': [('Drama', 0.574), ('Comedy', 0.426)], '211': [('Drama', 0.794), ('Romance', 0.206)], '212': [('Drama', 0.741), ('Romance', 0.259)], '213': [('Drama', 0.746), ('Comedy', 0.254)], '214': [('Comedy', 0.791), ('Drama', 0.209)], '215': [('Adventure', 0.52), ('Action', 0.48)], '216': [('Horror', 0.783), ('Comedy', 0.217)], '217': [('Drama', 0.684), ('Mystery', 0.316)], '218': [('Drama', 0.588), ('Comedy', 0.412)], '219': [('Action', 0.535), ('Drama', 0.465)], '220': [('Drama', 0.577), ('Comedy', 0.423)], '221': [('Thriller', 0.597), ('Crime', 0.403)], '222': [('Romance', 0.557), ('Drama', 0.443)], '223': [('Drama', 0.872), ('Romance', 0.128)], '224': [('Drama', 0.608), ('Comedy', 0.392)], '225': [('Drama', 0.669), ('Romance', 0.331)], '226': [('Comedy', 0.656), ('Drama', 0.344)], '227': [('Drama', 0.752), ('Comedy', 0.248)], '228': [('Drama', 0.506), ('Comedy', 0.494)], '229': [('Drama', 0.627), ('Comedy', 0.373)], '230': [('Drama', 0.769), ('Crime', 0.231)], '231': [('Comedy', 0.538), ('Drama', 0.462)], '232': [('Comedy', 0.531), ('Drama', 0.469)], '233': [('Thriller', 0.569), ('Drama', 0.431)], '234': [('Drama', 0.584), ('Comedy', 0.416)], '235': [('Drama', 0.554), ('Comedy', 0.446)], '236': [('Drama', 0.593), ('Comedy', 0.407)], '237': [('Comedy', 0.563), ('Action', 0.437)], '238': [('Drama', 0.772), ('Romance', 0.228)], '239': [('Comedy', 0.589), ('Drama', 0.411)], '240': [('Comedy', 0.545), ('Action', 0.455)], '241': [('Drama', 0.611), ('Thriller', 0.389)], '242': [('Drama', 0.643), ('Comedy', 0.357)], '243': [('Action', 0.552), ('Thriller', 0.448)], '244': [('Drama', 0.601), ('Comedy', 0.399)], '245': [('Drama', 0.594), ('Comedy', 0.406)], '246': [('Drama', 0.599), ('Thriller', 0.401)], '247': [('Drama', 0.504), ('Comedy', 0.496)], '248': [('Drama', 0.611), ('Action', 0.389)], '249': [('Comedy', 0.676), ('Drama', 0.324)], '250': [('Comedy', 0.516), ('Drama', 0.484)], '251': [('Drama', 0.568), ('Adventure', 0.432)], '252': [('Drama', 0.555), ('Horror', 0.445)], '253': [('Drama', 0.737), ('Comedy', 0.263)], '254': [('Drama', 0.636), ('Comedy', 0.364)], '255': [('Drama', 0.693), ('Comedy', 0.307)], '256': [('Action', 0.589), ('Drama', 0.411)], '257': [('Drama', 0.575), ('Action', 0.425)], '258': [('Thriller', 0.57), ('Comedy', 0.43)], '259': [('Drama', 0.567), ('Thriller', 0.433)], '260': [('Drama', 0.646), ('Romance', 0.354)], '261': [('Drama', 0.643), ('Crime', 0.357)], '262': [('Drama', 0.545), ('Comedy', 0.455)], '263': [('Drama', 0.603), ('Comedy', 0.397)], '264': [('Thriller', 0.628), ('Drama', 0.372)], '265': [('Action', 0.65), ('Drama', 0.35)], '266': [('Thriller', 0.554), ('Action', 0.446)], '267': [('Drama', 0.708), ('Comedy', 0.292)], '268': [('Drama', 0.787), ('Thriller', 0.213)], '269': [('Thriller', 0.502), ('Crime', 0.498)], '270': [('Drama', 0.635), ('Crime', 0.365)], '271': [('Comedy', 0.691), ('Thriller', 0.309)], '272': [('Comedy', 0.533), ('Adventure', 0.467)], '273': [('Thriller', 0.512), ('Drama', 0.488)], '274': [('Action', 0.568), ('Thriller', 0.432)], '275': [('Comedy', 0.558), ('Drama', 0.442)], '276': [('Drama', 0.568), ('Comedy', 0.432)], '277': [('Drama', 0.647), ('Action', 0.353)], '278': [('Comedy', 0.517), ('Action', 0.483)], '279': [('Drama', 0.575), ('Comedy', 0.425)], '280': [('Comedy', 0.586), ('Drama', 0.414)], '281': [('Action', 0.688), ('Thriller', 0.312)], '282': [('Drama', 0.601), ('Comedy', 0.399)], '283': [('Drama', 0.799), ('Comedy', 0.201)], '284': [('Thriller', 0.616), ('Drama', 0.384)], '285': [('Drama', 0.521), ('Thriller', 0.479)], '286': [('Horror', 0.574), ('Action', 0.426)], '287': [('Action', 0.546), ('Adventure', 0.454)], '288': [('Crime', 0.529), ('Comedy', 0.471)], '289': [('Drama', 0.582), ('Adventure', 0.418)], '290': [('Drama', 0.57), ('Thriller', 0.43)], '291': [('Comedy', 0.558), ('Drama', 0.442)], '292': [('Drama', 0.5), ('Comedy', 0.5)], '293': [('Drama', 0.746), ('Romance', 0.254)], '294': [('Drama', 0.659), ('Comedy', 0.341)], '295': [('Drama', 0.527), ('Thriller', 0.473)], '296': [('Drama', 0.575), ('Action', 0.425)], '297': [('Drama', 0.677), ('Comedy', 0.323)], '298': [('Drama', 0.87), ('Fantasy', 0.13)], '299': [('Comedy', 0.57), ('Drama', 0.43)], '300': [('Comedy', 0.651), ('Action', 0.349)], '301': [('Drama', 0.66), ('Adventure', 0.34)], '302': [('Drama', 0.598), ('Comedy', 0.402)], '303': [('Drama', 0.626), ('Comedy', 0.374)], '304': [('Drama', 0.699), ('Crime', 0.301)], '305': [('Sci-Fi', 0.708), ('Drama', 0.292)], '306': [('Comedy', 0.587), ('Action', 0.413)], '307': [('Drama', 0.775), ('Crime', 0.225)], '308': [('Drama', 0.513), ('Action', 0.487)], '309': [('Action', 0.525), ('Drama', 0.475)], '310': [('Drama', 0.789), ('Thriller', 0.211)], '311': [('Drama', 0.503), ('Comedy', 0.497)], '312': [('Comedy', 0.533), ('Drama', 0.467)], '313': [('Comedy', 0.648), ('Crime', 0.352)], '314': [('Action', 0.556), ('Adventure', 0.444)], '315': [('Drama', 0.647), ('Adventure', 0.353)], '316': [('Drama', 0.699), ('Crime', 0.301)], '317': [('Drama', 0.724), ('Comedy', 0.276)], '318': [('Drama', 0.683), ('Crime', 0.317)], '319': [('Comedy', 0.546), ('Thriller', 0.454)], '320': [('Drama', 0.591), ('Comedy', 0.409)], '321': [('Drama', 0.648), ('Romance', 0.352)], '322': [('Drama', 0.792), ('Comedy', 0.208)], '323': [('Drama', 0.694), ('Crime', 0.306)], '324': [('Drama', 0.828), ('Comedy', 0.172)], '325': [('Drama', 0.586), ('Adventure', 0.414)], '326': [('Drama', 0.71), ('Romance', 0.29)], '327': [('Comedy', 0.583), ('Sci-Fi', 0.417)], '328': [('Comedy', 0.52), ('Drama', 0.48)], '329': [('Comedy', 0.785), ('Action', 0.215)], '330': [('Drama', 0.791), ('Romance', 0.209)], '331': [('Adventure', 0.514), ('Children', 0.486)], '332': [('Comedy', 0.501), ('Drama', 0.499)], '333': [('Drama', 0.723), ('Romance', 0.277)], '334': [('Drama', 0.604), ('Comedy', 0.396)], '335': [('Drama', 0.717), ('Thriller', 0.283)], '336': [('Comedy', 0.706), ('Romance', 0.294)], '337': [('Drama', 0.617), ('Comedy', 0.383)], '338': [('Drama', 0.63), ('Comedy', 0.37)], '339': [('Action', 0.54), ('Drama', 0.46)], '340': [('Crime', 0.591), ('Drama', 0.409)], '341': [('Drama', 0.792), ('Comedy', 0.208)], '342': [('Drama', 0.654), ('Comedy', 0.346)], '343': [('Comedy', 0.536), ('Action', 0.464)], '344': [('Action', 0.553), ('Drama', 0.447)], '345': [('Drama', 0.768), ('Romance', 0.232)], '346': [('Comedy', 0.679), ('Drama', 0.321)], '347': [('Drama', 0.779), ('Comedy', 0.221)], '348': [('Drama', 0.644), ('Thriller', 0.356)], '349': [('Drama', 0.551), ('Thriller', 0.449)], '350': [('Adventure', 0.512), ('Fantasy', 0.488)], '351': [('Thriller', 0.68), ('Drama', 0.32)], '352': [('Drama', 0.699), ('Comedy', 0.301)], '353': [('Thriller', 0.534), ('Action', 0.466)], '354': [('Drama', 0.539), ('Comedy', 0.461)], '355': [('Thriller', 0.601), ('Drama', 0.399)], '356': [('Drama', 0.53), ('Comedy', 0.47)], '357': [('Drama', 0.683), ('Comedy', 0.317)], '358': [('Drama', 0.509), ('Comedy', 0.491)], '359': [('Drama', 0.539), ('Comedy', 0.461)], '360': [('Drama', 0.604), ('Comedy', 0.396)], '361': [('Drama', 0.635), ('Thriller', 0.365)], '362': [('Drama', 0.61), ('Crime', 0.39)], '363': [('Horror', 0.577), ('Comedy', 0.423)], '364': [('Comedy', 0.568), ('Drama', 0.432)], '365': [('Comedy', 0.547), ('Drama', 0.453)], '366': [('Drama', 0.512), ('Comedy', 0.488)], '367': [('Drama', 0.707), ('Romance', 0.293)], '368': [('Comedy', 0.502), ('Drama', 0.498)], '369': [('Drama', 0.552), ('Comedy', 0.448)], '370': [('Thriller', 0.571), ('Action', 0.429)], '371': [('Drama', 0.679), ('Thriller', 0.321)], '372': [('Comedy', 0.708), ('Drama', 0.292)], '373': [('Action', 0.514), ('Comedy', 0.486)], '374': [('Drama', 0.615), ('Adventure', 0.385)], '375': [('Drama', 0.697), ('Comedy', 0.303)], '376': [('Drama', 0.564), ('Comedy', 0.436)], '377': [('Drama', 0.596), ('Comedy', 0.404)], '378': [('Drama', 0.782), ('Romance', 0.218)], '379': [('Drama', 0.595), ('Romance', 0.405)], '380': [('Comedy', 0.555), ('Drama', 0.445)], '381': [('Thriller', 0.549), ('Drama', 0.451)], '382': [('Drama', 0.556), ('Romance', 0.444)], '383': [('Comedy', 0.511), ('Drama', 0.489)], '384': [('Drama', 0.562), ('Comedy', 0.438)], '385': [('Comedy', 0.653), ('Thriller', 0.347)], '386': [('Drama', 0.733), ('Romance', 0.267)], '387': [('Comedy', 0.551), ('Action', 0.449)], '388': [('Drama', 0.681), ('Thriller', 0.319)], '389': [('Comedy', 0.558), ('Drama', 0.442)], '390': [('Drama', 0.634), ('Comedy', 0.366)], '391': [('Drama', 0.537), ('Crime', 0.463)], '392': [('Fantasy', 0.55), ('Adventure', 0.45)], '393': [('Thriller', 0.599), ('Drama', 0.401)], '394': [('Comedy', 0.512), ('Drama', 0.488)], '395': [('Drama', 0.668), ('Comedy', 0.332)], '396': [('Drama', 0.596), ('Thriller', 0.404)], '397': [('Drama', 0.849), ('Comedy', 0.151)], '398': [('Drama', 0.504), ('Action', 0.496)], '399': [('Drama', 0.726), ('Comedy', 0.274)], '400': [('Drama', 0.617), ('Adventure', 0.383)], '401': [('Drama', 0.625), ('Thriller', 0.375)], '402': [('Drama', 0.571), ('Action', 0.429)], '403': [('Drama', 0.538), ('Thriller', 0.462)], '404': [('Romance', 0.511), ('Comedy', 0.489)], '405': [('Drama', 0.755), ('Thriller', 0.245)], '406': [('Drama', 0.585), ('Comedy', 0.415)], '407': [('Drama', 0.736), ('Thriller', 0.264)], '408': [('Drama', 0.559), ('Thriller', 0.441)], '409': [('Comedy', 0.574), ('Drama', 0.426)], '410': [('Comedy', 0.661), ('Drama', 0.339)], '411': [('Thriller', 0.551), ('Drama', 0.449)], '412': [('Drama', 0.676), ('Comedy', 0.324)], '413': [('Drama', 0.719), ('Comedy', 0.281)], '414': [('Drama', 0.695), ('Thriller', 0.305)], '415': [('Drama', 0.609), ('Thriller', 0.391)], '416': [('Thriller', 0.558), ('Action', 0.442)], '417': [('Drama', 0.723), ('Comedy', 0.277)], '418': [('Drama', 0.592), ('Comedy', 0.408)], '419': [('Drama', 0.591), ('Adventure', 0.409)], '420': [('Comedy', 0.703), ('Drama', 0.297)], '421': [('Drama', 0.698), ('Romance', 0.302)], '422': [('Drama', 0.606), ('Comedy', 0.394)], '423': [('Thriller', 0.505), ('Drama', 0.495)], '424': [('Drama', 0.526), ('Thriller', 0.474)], '425': [('Drama', 0.679), ('Comedy', 0.321)], '426': [('Drama', 0.677), ('Comedy', 0.323)], '427': [('Drama', 0.584), ('Action', 0.416)], '428': [('Action', 0.652), ('Thriller', 0.348)], '429': [('Drama', 0.618), ('Comedy', 0.382)], '430': [('Drama', 0.692), ('Thriller', 0.308)], '431': [('Thriller', 0.685), ('Adventure', 0.315)], '432': [('Action', 0.538), ('Drama', 0.462)], '433': [('Action', 0.595), ('Sci-Fi', 0.405)], '434': [('Drama', 0.767), ('Crime', 0.233)], '435': [('Action', 0.558), ('Thriller', 0.442)], '436': [('Drama', 0.668), ('Comedy', 0.332)], '437': [('Drama', 0.628), ('Thriller', 0.372)], '438': [('Drama', 0.618), ('Comedy', 0.382)], '439': [('Drama', 0.705), ('Romance', 0.295)], '440': [('Comedy', 0.502), ('Drama', 0.498)], '441': [('Action', 0.551), ('Sci-Fi', 0.449)], '442': [('Drama', 0.693), ('Romance', 0.307)], '443': [('Drama', 0.773), ('Romance', 0.227)], '444': [('Drama', 0.582), ('Thriller', 0.418)], '445': [('Drama', 0.7), ('Romance', 0.3)], '446': [('Drama', 0.506), ('Thriller', 0.494)], '447': [('Drama', 0.619), ('Romance', 0.381)], '448': [('Drama', 0.8), ('Thriller', 0.2)], '449': [('Drama', 0.674), ('Crime', 0.326)], '450': [('Drama', 0.691), ('Comedy', 0.309)], '451': [('Drama', 0.542), ('Comedy', 0.458)], '452': [('Action', 0.521), ('Thriller', 0.479)], '453': [('Comedy', 0.596), ('Action', 0.404)], '454': [('Thriller', 0.572), ('Action', 0.428)], '455': [('Comedy', 0.568), ('Drama', 0.432)], '456': [('Action', 0.509), ('Comedy', 0.491)], '457': [('Drama', 0.768), ('Thriller', 0.232)], '458': [('Drama', 0.68), ('Comedy', 0.32)], '459': [('Drama', 0.535), ('Thriller', 0.465)], '460': [('Comedy', 0.55), ('Drama', 0.45)], '461': [('Action', 0.555), ('Drama', 0.445)], '462': [('Comedy', 0.586), ('Thriller', 0.414)], '463': [('Drama', 0.548), ('Comedy', 0.452)], '464': [('Drama', 0.615), ('Comedy', 0.385)], '465': [('Comedy', 0.591), ('Drama', 0.409)], '466': [('Drama', 0.711), ('Action', 0.289)], '467': [('Drama', 0.621), ('Sci-Fi', 0.379)], '468': [('Drama', 0.545), ('Comedy', 0.455)], '469': [('Drama', 0.728), ('Comedy', 0.272)], '470': [('Comedy', 0.709), ('Romance', 0.291)], '471': [('Drama', 0.562), ('Romance', 0.438)], '472': [('Drama', 0.555), ('Fantasy', 0.445)], '473': [('Thriller', 0.57), ('Action', 0.43)], '474': [('Comedy', 0.512), ('Drama', 0.488)], '475': [('Drama', 0.636), ('Comedy', 0.364)], '476': [('Drama', 0.631), ('Crime', 0.369)], '477': [('Drama', 0.519), ('Comedy', 0.481)], '478': [('Drama', 0.562), ('Romance', 0.438)], '479': [('Drama', 0.625), ('Comedy', 0.375)], '480': [('Drama', 0.583), ('Comedy', 0.417)], '481': [('Comedy', 0.815), ('Drama', 0.185)], '482': [('Drama', 0.677), ('Comedy', 0.323)], '483': [('Drama', 0.621), ('Crime', 0.379)], '484': [('Comedy', 0.672), ('Action', 0.328)], '485': [('Romance', 0.526), ('Comedy', 0.474)], '486': [('Drama', 0.517), ('Comedy', 0.483)], '487': [('Comedy', 0.656), ('Romance', 0.344)], '488': [('Drama', 0.793), ('Comedy', 0.207)], '489': [('Thriller', 0.503), ('Action', 0.497)], '490': [('Drama', 0.631), ('Comedy', 0.369)], '491': [('Thriller', 0.514), ('Action', 0.486)], '492': [('Drama', 0.658), ('Comedy', 0.342)], '493': [('Drama', 0.668), ('Comedy', 0.332)], '494': [('Comedy', 0.506), ('Romance', 0.494)], '495': [('Drama', 0.533), ('Comedy', 0.467)], '496': [('Comedy', 0.685), ('Adventure', 0.315)], '497': [('Drama', 0.588), ('Adventure', 0.412)], '498': [('Drama', 0.787), ('Comedy', 0.213)], '499': [('Drama', 0.716), ('Romance', 0.284)], '500': [('Comedy', 0.623), ('Drama', 0.377)], '501': [('Drama', 0.537), ('Comedy', 0.463)], '502': [('Comedy', 0.678), ('Drama', 0.322)], '503': [('Drama', 0.762), ('Comedy', 0.238)], '504': [('Drama', 0.749), ('Crime', 0.251)], '505': [('Drama', 0.559), ('Romance', 0.441)], '506': [('Drama', 0.652), ('Thriller', 0.348)], '507': [('Thriller', 0.543), ('Adventure', 0.457)], '508': [('Drama', 0.527), ('Sci-Fi', 0.473)], '509': [('Comedy', 0.571), ('Drama', 0.429)], '510': [('Comedy', 0.605), ('Drama', 0.395)], '511': [('Action', 0.524), ('Drama', 0.476)], '512': [('Drama', 0.621), ('Action', 0.379)], '513': [('Action', 0.604), ('Thriller', 0.396)], '514': [('Drama', 0.55), ('Action', 0.45)], '515': [('Drama', 0.505), ('Adventure', 0.495)], '516': [('Comedy', 0.548), ('Drama', 0.452)], '517': [('Drama', 0.644), ('Documentary', 0.356)], '518': [('Drama', 0.602), ('Action', 0.398)], '519': [('Drama', 0.512), ('Action', 0.488)], '520': [('Drama', 0.649), ('Action', 0.351)], '521': [('Drama', 0.604), ('Action', 0.396)], '522': [('Romance', 0.512), ('Comedy', 0.488)], '523': [('Drama', 0.54), ('Comedy', 0.46)], '524': [('Action', 0.585), ('Thriller', 0.415)], '525': [('Drama', 0.761), ('Comedy', 0.239)], '526': [('Comedy', 0.659), ('Action', 0.341)], '527': [('Action', 0.525), ('Drama', 0.475)], '528': [('Drama', 0.666), ('Comedy', 0.334)], '529': [('Adventure', 0.507), ('Action', 0.493)], '530': [('Drama', 0.637), ('Comedy', 0.363)], '531': [('Comedy', 0.619), ('Drama', 0.381)], '532': [('Drama', 0.551), ('Comedy', 0.449)], '533': [('Comedy', 0.766), ('Action', 0.234)], '534': [('Drama', 0.553), ('Thriller', 0.447)], '535': [('Adventure', 0.5), ('Action', 0.5)], '536': [('Thriller', 0.536), ('Comedy', 0.464)], '537': [('Drama', 0.683), ('War', 0.317)], '538': [('Comedy', 0.502), ('Drama', 0.498)], '539': [('Comedy', 0.639), ('Drama', 0.361)], '540': [('Comedy', 0.553), ('Thriller', 0.447)], '541': [('Drama', 0.505), ('Action', 0.495)], '542': [('Drama', 0.631), ('Thriller', 0.369)], '543': [('Drama', 0.662), ('Comedy', 0.338)], '544': [('Drama', 0.673), ('Comedy', 0.327)], '545': [('Comedy', 0.546), ('Drama', 0.454)], '546': [('Comedy', 0.509), ('Drama', 0.491)], '547': [('Comedy', 0.632), ('Romance', 0.368)], '548': [('Drama', 0.616), ('Comedy', 0.384)], '549': [('Drama', 0.586), ('Action', 0.414)], '550': [('Drama', 0.784), ('Crime', 0.216)], '551': [('Comedy', 0.5), ('Action', 0.5)], '552': [('Adventure', 0.522), ('Children', 0.478)], '553': [('Comedy', 0.745), ('Drama', 0.255)], '554': [('Drama', 0.512), ('Comedy', 0.488)], '555': [('Drama', 0.605), ('Comedy', 0.395)], '556': [('Thriller', 0.519), ('Action', 0.481)], '557': [('Action', 0.601), ('Drama', 0.399)], '558': [('Drama', 0.624), ('Comedy', 0.376)], '559': [('Drama', 0.602), ('Comedy', 0.398)], '560': [('Comedy', 0.652), ('Drama', 0.348)], '561': [('Comedy', 0.558), ('Drama', 0.442)], '562': [('Action', 0.578), ('Adventure', 0.422)], '563': [('Drama', 0.655), ('Comedy', 0.345)], '564': [('Comedy', 0.588), ('Drama', 0.412)], '565': [('Action', 0.583), ('Comedy', 0.417)], '566': [('Comedy', 0.648), ('Drama', 0.352)], '567': [('Drama', 0.517), ('Comedy', 0.483)], '568': [('Drama', 0.769), ('Comedy', 0.231)], '569': [('Drama', 0.539), ('Comedy', 0.461)], '570': [('Comedy', 0.526), ('Thriller', 0.474)], '571': [('Drama', 0.513), ('Romance', 0.487)], '572': [('Comedy', 0.533), ('Romance', 0.467)], '573': [('Drama', 0.583), ('Thriller', 0.417)], '574': [('Drama', 0.684), ('Documentary', 0.316)], '575': [('Drama', 0.7), ('Comedy', 0.3)], '576': [('Comedy', 0.613), ('Drama', 0.387)], '577': [('Action', 0.555), ('Thriller', 0.445)], '578': [('Comedy', 0.508), ('Drama', 0.492)], '579': [('Drama', 0.569), ('Comedy', 0.431)], '580': [('Comedy', 0.68), ('Drama', 0.32)], '581': [('Romance', 0.541), ('Comedy', 0.459)], '582': [('Sci-Fi', 0.594), ('Action', 0.406)], '583': [('Action', 0.622), ('Thriller', 0.378)], '584': [('Drama', 0.659), ('Comedy', 0.341)], '585': [('Drama', 0.517), ('Thriller', 0.483)], '586': [('Comedy', 0.556), ('Drama', 0.444)], '587': [('Drama', 0.647), ('Comedy', 0.353)], '588': [('Drama', 0.528), ('Comedy', 0.472)], '589': [('Drama', 0.538), ('Comedy', 0.462)], '590': [('Comedy', 0.609), ('Drama', 0.391)], '591': [('Drama', 0.51), ('Action', 0.49)], '592': [('Drama', 0.641), ('Comedy', 0.359)], '593': [('Drama', 0.738), ('Thriller', 0.262)], '594': [('Comedy', 0.593), ('Adventure', 0.407)], '595': [('Drama', 0.5), ('Action', 0.5)], '596': [('Drama', 0.819), ('Comedy', 0.181)], '597': [('Comedy', 0.539), ('Drama', 0.461)], '598': [('Sci-Fi', 0.644), ('Action', 0.356)], '599': [('Action', 0.512), ('Thriller', 0.488)], '600': [('Drama', 0.71), ('Comedy', 0.29)], '601': [('Drama', 0.789), ('Comedy', 0.211)], '602': [('Drama', 0.532), ('Sci-Fi', 0.468)], '603': [('Drama', 0.728), ('Comedy', 0.272)], '604': [('Action', 0.532), ('Drama', 0.468)], '605': [('Drama', 0.686), ('Comedy', 0.314)], '606': [('Drama', 0.693), ('Thriller', 0.307)], '607': [('Drama', 0.691), ('Comedy', 0.309)], '608': [('Comedy', 0.59), ('Action', 0.41)], '609': [('Comedy', 0.65), ('Drama', 0.35)], '610': [('Drama', 0.625), ('Thriller', 0.375)], '611': [('Drama', 0.751), ('Thriller', 0.249)], '612': [('Sci-Fi', 0.681), ('Action', 0.319)], '613': [('Drama', 0.618), ('Thriller', 0.382)], '614': [('Action', 0.615), ('Thriller', 0.385)], '615': [('Drama', 0.698), ('Thriller', 0.302)], '616': [('Comedy', 0.509), ('Drama', 0.491)], '617': [('Drama', 0.715), ('Comedy', 0.285)], '618': [('Drama', 0.704), ('Action', 0.296)], '619': [('Drama', 0.714), ('Thriller', 0.286)], '620': [('Drama', 0.537), ('Comedy', 0.463)], '621': [('Action', 0.573), ('Adventure', 0.427)], '622': [('Action', 0.519), ('Drama', 0.481)], '623': [('Drama', 0.587), ('Comedy', 0.413)], '624': [('Comedy', 0.521), ('Drama', 0.479)], '625': [('Action', 0.621), ('Adventure', 0.379)], '626': [('Romance', 0.511), ('Drama', 0.489)], '627': [('Drama', 0.583), ('Comedy', 0.417)], '628': [('Drama', 0.54), ('Comedy', 0.46)], '629': [('Drama', 0.574), ('Sci-Fi', 0.426)], '630': [('Thriller', 0.595), ('Drama', 0.405)], '631': [('Drama', 0.816), ('Crime', 0.184)], '632': [('Drama', 0.722), ('Comedy', 0.278)], '633': [('Drama', 0.608), ('Comedy', 0.392)], '634': [('Drama', 0.752), ('Comedy', 0.248)], '635': [('Thriller', 0.641), ('Mystery', 0.359)], '636': [('Drama', 0.6), ('Comedy', 0.4)], '637': [('Adventure', 0.507), ('Action', 0.493)], '638': [('Comedy', 0.5), ('Romance', 0.5)], '639': [('Drama', 0.712), ('Crime', 0.288)], '640': [('Comedy', 0.514), ('Drama', 0.486)], '641': [('Action', 0.555), ('Thriller', 0.445)], '642': [('Drama', 0.695), ('Thriller', 0.305)], '643': [('Drama', 0.588), ('Thriller', 0.412)], '644': [('Comedy', 0.588), ('Drama', 0.412)], '645': [('Adventure', 0.625), ('Children', 0.375)], '646': [('Drama', 0.639), ('Romance', 0.361)], '647': [('Comedy', 0.516), ('Crime', 0.484)], '648': [('Drama', 0.581), ('Comedy', 0.419)], '649': [('Action', 0.538), ('Thriller', 0.462)], '650': [('Comedy', 0.685), ('Children', 0.315)], '651': [('Drama', 0.534), ('Comedy', 0.466)], '652': [('Drama', 0.832), ('Romance', 0.168)], '653': [('Comedy', 0.64), ('Drama', 0.36)], '654': [('Action', 0.538), ('Adventure', 0.462)], '655': [('Drama', 0.524), ('Comedy', 0.476)], '656': [('Comedy', 0.577), ('Thriller', 0.423)], '657': [('Comedy', 0.559), ('Sci-Fi', 0.441)], '658': [('Comedy', 0.531), ('Drama', 0.469)], '659': [('Drama', 0.683), ('Thriller', 0.317)], '660': [('Drama', 0.731), ('Comedy', 0.269)], '661': [('Drama', 0.656), ('Thriller', 0.344)], '662': [('Drama', 0.564), ('Comedy', 0.436)], '663': [('Drama', 0.589), ('Thriller', 0.411)], '664': [('Comedy', 0.522), ('Romance', 0.478)], '665': [('Drama', 0.714), ('Thriller', 0.286)], '666': [('Drama', 0.67), ('Comedy', 0.33)], '667': [('Drama', 0.667), ('Comedy', 0.333)], '668': [('Drama', 0.817), ('Thriller', 0.183)]}


# Get the top two genres of each user's genres popularity and their weight, calculate the number of movies recommended by the genres according to the weight. Find the top movies of this genres in the ranking of movies of different genres for recommendation

# In[14]:


def recommend(userid):
    
    if userid not in user_tags:
        return {}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for i in user_tags[userid]:
        genres = i[0]
        #print(genres)
        ratio = i[1]
        #print(ratio)
        num = round(3*ratio) #Calculate the number of movies recommended by the genre according to weight
        if genres not in genres_rating_sort:
            continue
        recom_list = genres_rating_sort[genres][:num]
        #print(recom_list)
        recom_result[userid] += recom_list

    return recom_result


# In[15]:


recommend('120')


# In[ ]:




