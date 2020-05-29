# Copyright 2020 Alberto Martín Mateos and Niloufar Shoeibi
# See LICENSE for details.

# Copyright 2019-2020 Alberto Martín Mateos & Niloufar Shoeibi for TWINPICS project
# See LICENSE for details.
# -*- coding: utf-8 -*-

import subprocess
import sys
import warnings
warnings.filterwarnings("ignore")
#---------------------------------------------------------------INSTALLATION---------------------------------------------------------#

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("networkx==2.2")
install("pandas")
install("numpy")
install ("urllib3")
install("requests")
install("matplotlib")
install("tweepy")
install("nltk")
install("textblob")
##----------------------------------------------IMPORTS---------------------------------------------------------------------------#	
import json
import pandas as pd
import numpy as np
import urllib3
import re
import time
import networkx as nx
import requests
import matplotlib.pyplot as plt
import tweepy
from os import path
from datetime import timedelta

#---------------------------------------------NLP-Part-------------------------------------------------------------------------------#
from textblob import TextBlob
import nltk
from nltk import RegexpTokenizer
# some small toolkits to download
nltk.download("wordnet")
nltk.download('brown')
nltk.download('punkt')

def sentiental_analysis_features(data):
	corpus =[]
	polarities=[]
	subjectivities=[]
	for tweet in data.text:
		corpus.append(TextBlob(tweet.lower()))
	for i in range(len(corpus)):
		polarities.append(corpus[i].polarity)
		subjectivities.append(corpus[i].subjectivity)
	data['polarity']= polarities
	data['subjectivity']= subjectivities
	return data

def distribution_sentiment_tweets(data):
	### VISUALIZATION
	plt.rcParams['figure.figsize'] = [50, 40]
	for i in range (len(data)):
		x=data.polarity.iloc[i]
		y=data.subjectivity.iloc[i]
		if x>0.1 : # blue   red
			if y>0.6:  # yellow   green
				plt.scatter(x,y, color='blue')
			else: 
				plt.scatter(x,y, color='pink')
		elif -0.1<=x<=0.1:
			if 0.4<=y<=0.6:  # yellow   green
				plt.scatter(x,y, color='gold')
		else:
			if y>0.6:  # yellow   green
				plt.scatter(x,y, color='purple')
			else: 
				plt.scatter(x,y, color='red')  
	plt.text(x+0.01, y+0.01, 'tweet'+str(i), fontsize=10)
	plt.xlim(-1,1)
	plt.ylim(0,1)
	plt.title('sentiment anaysis',fontsize=20)
	plt.xlabel('<------------------ NEGATIVE ------------------   POLARITY ------------------ POSITIVE ------------------>',fontsize=15)
	plt.ylabel('<----------------- FACTS ------------------ SUBJECTIVITY ------------------ OPINIONS ----------------->',fontsize=15)
	plt.show()

def general_pieChart(data):
	p=0 # positive
	n=0 # Negative
	o=0 # neutral
	for i in range(len(data)):
		if data['polarity'].iloc[i]>0.1:
			p+=1
		elif data['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	kn=0
	for i in range(len(data)):
	  if data['subjectivity'].iloc[i]>0.6:
		  op+=1
	  elif data['subjectivity'].iloc[i]<0.4:
		  f+=1
	  else:
		  kn+=1
	plt.rcParams['figure.figsize'] = [10,5]
	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['blue','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice

	labels2='Opinion','Fact','Neutral'
	sizes2=[f,op,kn]
	colors2=['pink','red','gold']
	explode2=(0,0,0)

	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('The General Sentiment Analysis of all The tweets of ')
	plt.axis('equal')
	plt.show()
	
def tokenize_tweets(data):
	sample_data_tokenized=[]  
	tokenizer=RegexpTokenizer(r'\w+')
	for tweets in data.text:
		sample_data_tokenized.append(tokenizer.tokenize(tweets.lower()))
	return sample_data_tokenized
	
def keywords_score(data,sample_data_tokenized, keyword_corpus):
	scores = []
	for i in range(len(sample_data_tokenized)):
		score=0
		for c in keyword_corpus.keywords:
			for t in sample_data_tokenized[i]:
				if c==t:
					score+=1
		try:
			scores.append(score/len(sample_data_tokenized[i]))
		except ZeroDivisionError:
			scores.append(0)
	data['keyword_score']=scores
	return data

def hashtag_score(data, sample_data_tokenized, hashtag_corpus):
	scores = []
	for i in range(len(sample_data_tokenized)):
		score=0
		for c in hashtag_corpus.hashtags:
			for t in sample_data_tokenized[i]:
				if c==t:
					score+=1
		try:
			scores.append(score)
		except ZeroDivisionError:
			scores.append(0)
	data['hashtags_score'] = scores
	data['index'] = [i for i in range(len(data))]
	data['names']= ['TWEET '+str(i) for i in range(len(data))]
	return data	
	
def terrorist_keywords_belonging(data):
	temp = data[data['keyword_score']>0].reset_index(drop=True)
	# Draw plot
	fig, ax = plt.subplots(figsize=(36,8), dpi= 80)
	ax.vlines(x=temp.index, ymin=0, ymax=temp.keyword_score, color='firebrick', alpha=0.7, linewidth=2)
	ax.scatter(x=temp.index, y=temp.keyword_score, s=75, color='firebrick', alpha=0.7)
	# Title, Label, Ticks and Ylim
	ax.set_title('Lollipop Chart for The belonging each tweet to the Terroristic Cluster', fontdict={'size':22})
	ax.set_ylabel('Belonging Score of each tweet to the cluster1' )
	ax.set_xticks(temp.index)
	ax.set_xticklabels(temp.names.str.upper(), rotation=90, fontdict={'horizontalalignment': 'right', 'size':12})
	ax.set_ylim(0, 1)
	# Annotate
	for row in temp.itertuples():
		ax.text(row.Index, row.keyword_score+0.15,rotation=90, s=round(row.keyword_score, 2), horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
	plt.show()
	
def pie_chart_keywords_terrorist(data):
	data_terr = data[data['keyword_score']>0].reset_index(drop=True)
	p=0
	n=0
	o=0
	for i in range(len(data_terr)):
		if data_terr['polarity'].iloc[i]>0.1:
			p+=1
		elif data_terr['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	for i in range(len(data_terr)):
		if data_terr['subjectivity'].iloc[i]>0.5:
			op+=1
		else:
			f+=1
	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['yellowgreen','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice
	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['lightblue','yellow']
	explode2=(0,0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('from '+str(len(data))+' tweets, '+ str(len(data_terr))+' tweets are belonging to Terroristic contents')
	plt.axis('equal')
	plt.show()
	

def terrorist_hashtags_belonging(data):
	temp = data[ data['hashtags_score']>0].reset_index(drop=True)
	# Draw plot
	fig, ax = plt.subplots(figsize=(36,24), dpi= 80)
	ax.vlines(x=temp.index, ymin=0, ymax=temp.hashtags_score, color='firebrick', alpha=0.7, linewidth=2)
	ax.scatter(x=temp.index, y=temp.hashtags_score, s=75, color='firebrick', alpha=0.7)
	# Title, Label, Ticks and Ylim
	ax.set_title('Lollipop Chart for The belonging each tweet to the Terrorist Hashtag Network', fontdict={'size':22})
	ax.set_ylabel('Number of Terrorist Hashtags' )
	ax.set_xticks(temp.index)
	ax.set_xticklabels(temp.names.str.upper(), rotation=90, fontdict={'horizontalalignment': 'right', 'size':12})
	ax.set_ylim(0, 30)
	# Annotate
	for row in temp.itertuples():
		ax.text(row.Index+0.01, row.hashtags_score+0.15,rotation=90, s=round(row.hashtags_score, 2), horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
	plt.show()

def pie_chart_hashtags_terrorist(data):
	temp = data[data['hashtags_score']>0].reset_index(drop=True)  
	p=0
	n=0
	o=0
	for i in range(len(temp)):
		if temp['polarity'].iloc[i]>0.1:
			p+=1
		elif temp['polarity'].iloc[i]<-0.1:
			n+=1
		else:
			o+=1
	f=0
	op=0
	for i in range(len(temp)):
		if temp['subjectivity'].iloc[i]>0.5:
			op+=1
		else:
			f+=1

	labels = 'Positive', 'Negative','Neutral'
	sizes = [p,n,o]
	colors = ['yellowgreen','red', 'gold'] #, 'yellowgreen', 'lightcoral','lightskyblue',
	explode = (0, 0,0)  # explode 1st slice
	labels2='Opinion','Fact'
	sizes2=[f,op]
	colors2=['lightblue','yellow']
	explode2=(0,0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	# Plot
	ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
	ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
	plt.title('from '+str(len(data))+' tweets, '+ str(len(temp))+' tweets are following Terroristic Hashtags')
	plt.axis('equal')
	plt.show()  

#----------------------------------------FUNCTIONS-----------------------------------------------------------------------------#

def load_file(df):
    df = pd.read_json(df)
    return df

def merge_dataframes(df1, df2):
    df_final = pd.merge(df1, df2, on = ["screen_name"])
    return df_final

#----------------------------------Structure for the graph-----------------------------------------#
def profile_connections (data_tweets):    
    screen_name = []
    screen_name_mention = []
    data = pd.DataFrame()
    data_tweets = data_tweets.rename(columns = {"created_at": "created_at_tw"})
    data_tweets = pd.concat([data_tweets.drop(['user'], axis=1), data_tweets['user'].apply(pd.Series)],
                            axis=1).drop_duplicates().reset_index(drop=True)
    if(data_tweets.empty == False):
        for i in range(len(data_tweets)):
            screen_name.append(data_tweets["screen_name"][i])
            if "@" in (data_tweets["text"][i]):
                split_text = data_tweets["text"][i].split()
                check = "@"
                screen_name_mention1 = [idx for idx in split_text if idx.lower().startswith(check.lower())]
                #Consider that @ is from a email or another words that is not the screen_name
                if not screen_name_mention1:
                    screen_name_mention.append(["Empty"])
                else:
                    screen_name_mention1 = re.sub("[\[\]\'\"!@?¿#$:….,]", '',str(screen_name_mention1)).split(", ")  
                    if(data_tweets["text"][i].startswith('RT',0)):
                        screen_name_mention.append([screen_name_mention1[0]])                    
                    else:
                        screen_name_mention.append(re.sub("[\[\]\'\"!@?¿#$:….,]", '',str(screen_name_mention1)).split(" "))
            else:
                screen_name_mention.append(["Empty"])
    data["screen_name"] = screen_name    
    data["screen_name_mention"] = screen_name_mention  
    #Agruping
    lst_col = "screen_name_mention"
    data = data[["screen_name","screen_name_mention"]]
    data_ext =pd.DataFrame({col:np.repeat(data[col].values, data[lst_col].str.len())for col in data.columns.difference(
        [lst_col])}).assign(**{lst_col:np.concatenate(data[lst_col].values)})[data.columns.tolist()]
    data1_ext = pd.DataFrame({'self_loop_iteration' : data_ext.groupby(data_ext.columns.tolist(),as_index=False).size().sort_values(
                                                                        ascending = False)}).reset_index()
    return data1_ext

#--------------------------------------Graph building functions---------------------------

def building_node_list(df):

    node_list = pd.DataFrame()
    n = []
    for i in range(len(df)):
        n.append(df['screen_name'].iloc[i])
        n.append(df['screen_name_mention'].iloc[i])
    node_list['screen_name']= n
    node_list = node_list.drop_duplicates()
    node_list = node_list[node_list["screen_name"] !="Empty"].reset_index()
    return list(node_list["screen_name"])

def building_DiGraph(node_list, df):
    DiG = nx.DiGraph()
    DiG.add_nodes_from(node_list)
    for i in range(len(df)):
        if(df['screen_name_mention'].iloc[i] !="Empty"):
            DiG.add_edge(df['screen_name'].iloc[i],df['screen_name_mention'].iloc[i])
    return DiG


def self_loop_iteration_nodes(df):
    df_self_loop_iteration_nodes = pd.DataFrame()
    n = []
    self_loop_iteration = []
    for i in range(len(df)):
        if(df["screen_name"].iloc[i] ==df["screen_name_mention"].iloc[i]):
            n.append(df['screen_name'].iloc[i])
            self_loop_iteration.append(df["self_loop_iteration"].iloc[i])            
        else:
            n.append(df['screen_name'].iloc[i])
            n.append(df['screen_name_mention'].iloc[i])
            self_loop_iteration.append(0)
            self_loop_iteration.append(0)
    df_self_loop_iteration_nodes['screen_name']= n
    df_self_loop_iteration_nodes['self_loop_iteration']= self_loop_iteration
    df = pd.DataFrame({'times': df_self_loop_iteration_nodes.groupby(["screen_name","self_loop_iteration"]).size().sort_values(
    ascending=False)}).reset_index().drop_duplicates(["screen_name"],keep="first")
    del df["times"]
    return df
	
def DiGraph_visualization (DiG):
    plt.figure(figsize=(30,18))
    nx.draw(DiG, with_labels=True, node_size=10, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=4)
    plt.show()

#---------------------------------Graph features functions ----------------------
def in_degree_centrality(DiG, output):
    l = []
    l = nx.in_degree_centrality(DiG)
    sc = []
    indegcent = []
    for k, v in l.items():
        indegcent.append(v)
        sc.append(k)
    output['in_degree_centrality']=indegcent
    output["screen_name"] = sc    
    return output

def out_degree_centrality(DiG, output):
    l=[]
    l=nx.out_degree_centrality(DiG)
    sc=[]
    outd=[]
    for k, v in l.items():
        outd.append(v)
    output['outdegree_centrality']=outd
    return output

def degree_centrality(DiG,output):
    l=[]
    l=nx.degree_centrality(DiG)
    deg=[]
    for k, v in l.items():
        deg.append(v)
    output['degree_centrality']=deg
    return output

def in_degree(DiG, output):
    indegs=[]
    for i in range(len(list(DiG.nodes))):
        indegs.append(DiG.in_degree(list(DiG.nodes)[i]))
    output['in_degree']=indegs
    return output

def out_degree(DiG, output):
    outdegs=[]
    for i in range(len(list(DiG.nodes))):
        outdegs.append(DiG.out_degree(list(DiG.nodes)[i]))
    output['out_degree']=outdegs
    return output

def degree(DiG, output):
    degs=[]
    for i in range(len(list(DiG.nodes))):
        degs.append(DiG.degree(list(DiG.nodes)[i]))
    output['degree']=degs
    return output

def self_loops(DiG, output):
    SL = list(DiG.nodes_with_selfloops())
    output['self_loop']= False
    l=[]
    for i in range(len(SL)):
        for j in range(len(output)):
            if SL[i]==output['screen_name'].iloc[j]:
                output.self_loop.iloc[j]=True
    return output


def graph_features(DiG,df):

    output = pd.DataFrame()
    output = in_degree_centrality(DiG, output)
    output = out_degree_centrality(DiG, output)
    output = degree_centrality(DiG, output)
    output = in_degree(DiG, output)
    output = out_degree(DiG, output)
    output = degree(DiG, output)
    output = self_loops(DiG, output)
    df_nodes_self_loop_iteration = self_loop_iteration_nodes(df)
    output = merge_dataframes(output, df_nodes_self_loop_iteration)
    return output

def user_timeline_extraction (node_list, consumerKey, consumerSecret,accessToken,accessTokenSecret, iter_tw, fichero):
    # get_user Returns the 20 most recent statuses posted from the authenticating user or the user specified. 
    profile_iter = len(node_list)
    k=0
    auth = tweepy.OAuthHandler(consumerKey[0], consumerSecret[0])
    auth.set_access_token(accessToken[0], accessTokenSecret[0])
    api = tweepy.API(auth)
    nc= 0
    ultima = 0
    origen1 = time.time()
    while ((k<= (len(node_list)+profile_iter)) & (ultima !=2) ):
      tweets_user=[]
      list_users_noInfo = []
      origen2 = time.time()
      i=0
      if ((len(node_list)>= k) & ((len(node_list)-profile_iter) <=k)):
        node_list1 = node_list[k:len(node_list)]
        ultima = 1
      else:
        node_list1 = node_list[k:k+profile_iter]
      while(i <(len(node_list1))):         
        pri = 0
        itera=0
        max_id=""
        intentos = 0
        while itera != iter_tw:
          try:
            if pri ==0:
              user=api.user_timeline(node_list1[i], count=200,tweet_mode="extended")      
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              pri=1
              itera = itera+1
            else:
              user=api.user_timeline(node_list1[i], count=200,tweet_mode="extended", max_id=max_id)
              tweets_user.append(user)
              max_id = str(tweets_user[len(tweets_user)-1][len(tweets_user[len(tweets_user)-1])-1]._json["id_str"])
              itera = itera+1
              intentos=0 # Para si justo es el primero el que no se puede extraer y no es problema de agotar claves
          except:
            nc = nc+1
            n_clave = len(consumerKey)
            if(nc == n_clave):
              nc= 0
            auth = tweepy.OAuthHandler(consumerKey[nc], consumerSecret[nc])
            auth.set_access_token(accessToken[nc], accessTokenSecret[nc])
            api = tweepy.API(auth)
            intentos = intentos + 1
            if(intentos == 2):         
              list_users_noInfo.append(node_list1[i])
              intentos = 0
              itera=iter_tw
        i = i+1       
      destino2 = time.time()
      aux=[]
      for i in range( len(tweets_user)):
        for j in range(len(tweets_user[i])):          
            aux.append(tweets_user[i][j]._json)     
      if(len(aux) != 0):  
        df = pd.DataFrame(aux)
        df = df.rename(columns = {"created_at": "created_at_tw"})
        df= df.rename(columns = {"lang": "lang_tw"})
        df = pd.concat([df.drop(['user'], axis=1), df['user'].apply(pd.Series)], axis=1)
        df = df.rename(columns={"followers_count": "followers",
                              "friends_count": "followees",
                              "retweet_count": "retweets",
                              "favorite_count": "favorites",
                              "favourites_count": "favorites_count",
                              "full_text": "text"})
        df2 = metadata_extraction(df)
        if path.exists("/content/"+ fichero):
          df2.to_csv(fichero,mode="a", index=False, header=False)
        else:
          df2.to_csv(fichero,index=False)         
        if len(list_users_noInfo) !=0:
          nodes = pd.DataFrame()
          nodes["nodos"] = list_users_noInfo
          if path.exists("/content/node_without_"+fichero):
            nodes.to_csv("node_without_"+ fichero, mode ="a",index=False, header=False)          
          else:
             nodes.to_csv("node_without_"+ fichero, index=False)
        k = k+profile_iter        
        if ultima ==1:          
          ultima =2
      else:
        print("Repetimos")
    print("Lista de usuarios sin metadata")
    print(list_users_noInfo)
    destino1 = time.time()
    return df2, list_users_noInfo


#----------------------------------Extract metadata-----------------------------------------------------------#
def metadata_extraction (df_users):
    
    users = df_users["screen_name"].unique()
    count_users=0
    df = pd.DataFrame() 
    for i in range(len(users)):
        data_tweets = df_users[df_users["screen_name"]==users[i]].reset_index()
        
        data = pd.DataFrame()              
        if(data_tweets.empty == False):       
            count_users = count_users + 1
            print("Usuarios: %f" % count_users)
            [screen_name_mention_user,seasonalityDF,tweets_urlDF,mentionsDF,text_tweetsDF,
             fav_twDF_list,ret_twDF_list,fav_twDF,ret_twDF,RT_tw,ntwPro_DF,minu_tw,tw_per_days_list,
             text_tweets_days_list,tweet_date_days_list,duplicated,minu_tw_answer,
             tw_day_list] = text_tweets_features_extraction(data_tweets)
            data["screen_name_mention_user"] = screen_name_mention_user
            data["screen_name"] = data_tweets["screen_name"].iloc[0]  
            data["created_at"] = data_tweets["created_at"].iloc[0]
            data["following"] = data_tweets["followees"].iloc[0]
            data["followers"] = data_tweets["followers"].iloc[0]
            data["statuses_count"] = data_tweets["statuses_count"].iloc[0]
            data["default_profile"] = data_tweets["default_profile"].iloc[0]
            data["default_profile_image"] = data_tweets["default_profile_image"].iloc[0]
            data["biography_profile"] = data_tweets["description"].iloc[0]
            data["listed_count"] = data_tweets["listed_count"].iloc[0]    
            data["favourite_count"] = data_tweets["favorites_count"].iloc[0]
            data["seasonality"] = seasonalityDF    
            data["tweets_url"] = tweets_urlDF    
            data["mentions"] = mentionsDF 
            data["text_tweets_days_list"] = text_tweets_days_list
            data["tweet_date_days_list"] = tweet_date_days_list   
            data["text_tweets"] = text_tweetsDF
            data["favorite_tweets_list"] = fav_twDF_list
            data["retweet_tweets_list"] = ret_twDF_list
            data["favorite_tweets_count"] = fav_twDF
            data["retweet_tweets_count"] = ret_twDF
            data["RT"] = RT_tw
            data["num_ownTw"] = ntwPro_DF    
            data["time_btw_tw"] = minu_tw
            data["tw_day_list"] = tw_day_list
            data["tw_per_day_list"] = tw_per_days_list
            data["tw_duplicated"] = duplicated
            data["minu_tw_answer"] = minu_tw_answer
            data["profile_type"] = data_tweets["verified"].iloc[0]
            data["screen_name_mention_user"] = data["screen_name_mention_user"].astype(str)
            probably_fake = []
            for j in range(len(data)):
                if data["biography_profile"].any()==False:# Si se lee el dataframe
                #if len(data["biography_profile"][j]) == 0:# Si se hace la extraccion antes de guardar los datos
                    data["biography_profile"][j] = 1
                else:
                    data["biography_profile"][j] = 0
                if data["following"].iloc[j] == 2001:
                    probably_fake.append(1)
                else:
                    probably_fake.append(0)
            data["probably_fake"] = probably_fake
            df = df.append(data, ignore_index=True)
    df =df.loc[df.astype(str).drop_duplicates().index].reset_index()
    
    df = time_twitter_account(df)
    df = time_series_tw(df)

    return df



def text_tweets_features_extraction(data_tweets):
   
    seasonalityDF = []
    tweets_urlDF = []
    mentionsDF = []
    text_tweetsDF = []
    fav_twDF= []
    ret_twDF = []
    ret_twDF_list = []
    fav_twDF_list = []
    ntwPro_DF= []
    RT_tw = []
    minu_tw = []
    minu_tw_answer = []
    tw_duplicated = []
    duplicated = []
    tw_per_day_list= []
    screen_name_mention_user = []
    tweets = []
    tweets_url = 0
    num_tw_day = 1
    is_RT=0
    is_RT_list= []
    screen_name_mention = []
    RT = []
    retweet_list = []
    favorite_list = []
    mentions = 0
    time_btw_tw = []
    tw_answer = []
    num_tw_days = []
    text_duplicated = []
    tw_day_list = []
    text_tweets_day = []
    text_tweets_days = []
    text_tweets_days_list = []
    #Almacenar la fecha entera de los tweets para si hay que consultar las horas de ese dia
    tweet_date_day = []
    tweet_date_days = []
    tweet_date_days_list = []
    lang_text_tweet = list(data_tweets["lang_tw"])
    text_tweets_user= list(data_tweets["text"])
    print(len(text_tweets_user))
    favorites= list(data_tweets["favorites"])
    retweets = list(data_tweets["retweets"])
    tweets_date= pd.to_datetime(data_tweets["created_at_tw"])
    for j in range(len(text_tweets_user)): #Comprobamos cuantos tweets han sido escritos por el usuario 
        if(text_tweets_user[j].startswith('RT',0)):
            RT.append(text_tweets_user[j])
            is_RT = 1
        else:
            is_RT=0          
            #Tweets with url from users
            if "http" in text_tweets_user[j]:
                tweets_url = tweets_url + 1
            #Tweets with mentions from users
            if "@" in text_tweets_user[j]:
                mentions = mentions + 1                        
            else:
                #Time of the answer of a tweet(tw --> @)
                if(j!=(len(text_tweets_user)-1)):
                    if ("@" in text_tweets_user[j+1]):
                        tw_answer.append((tweets_date[j] - tweets_date[j+1]) / np.timedelta64(1,'m'))
                #Found duplicated tweets where the only change the photo  that the users publish
                text_sinHttp = " ".join(filter(lambda x:x[0:4]!='http', text_tweets_user[j].split()))
                text_sinMencion = " ".join(filter(lambda x:x[0]!='@', text_sinHttp.split()))
                text_duplicated.append(text_sinMencion)
            tweets.append({"text":text_tweets_user[j], "lang": lang_text_tweet[j], "RT": 0})
            retweet_list.append(int(retweets[j]))
            favorite_list.append(int(favorites[j]))
        is_RT_list.append(is_RT)                                
        if(j!=0):
          #Time between tweets (RT + propios)
          time_btw_tw.append((tweets_date[j-1] - tweets_date[j]) / np.timedelta64(1,'m'))
          #Found if tweets are the same day
          #Second condition if all the tweets are the same day          
          if((tweets_date[j-1].date() == tweets_date[j].date()) & (j!=(len(text_tweets_user)-1))):
                            
              num_tw_day = num_tw_day + 1
              #Create a list with the tweets of a day
              text_tweets_day.append({"text": text_tweets_user[j-1],"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
              text_tweets_day.append({"text": text_tweets_user[j],"lang": lang_text_tweet[j], "RT": is_RT_list[j]})              
              tweet_date_day.append(tweets_date[j-1])
              tweet_date_day.append(tweets_date[j])                         
          else:
              if(j==(len(text_tweets_user)-1)):                  
                  if(tweets_date[j-1].date() == tweets_date[j].date()):                     
                      text_tweets_day.append({"text": text_tweets_user[j-1],"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
                      text_tweets_day.append({"text": text_tweets_user[j],"lang": lang_text_tweet[j], "RT": is_RT_list[j]})              
                      tweet_date_day.append(tweets_date[j-1])
                      tweet_date_day.append(tweets_date[j])
                      num_tw_day = num_tw_day + 1
                      num_tw_days.append(num_tw_day)
                      text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]] )
                      tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
                      num_tw_day = 1 
                      text_tweets_day = []
                      tweet_date_day = []
                  else:                      
                      text_tweets_day.append({"text": text_tweets_user[j-1],"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})                                   
                      tweet_date_day.append(tweets_date[j-1]) 
                      num_tw_days.append(1)                     
                      text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]])
                      tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
                      text_tweets_day = []
                      tweet_date_day = []
                      
                      tweet_date_day.append(tweets_date[j])                     
                      text_tweets_day.append({"text": text_tweets_user[j],"lang": lang_text_tweet[j], "RT": is_RT_list[j]}) 
                      num_tw_days.append(1)
                      text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]] )
                      tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))
                      num_tw_day = 1 
                      text_tweets_day = []
                      tweet_date_day = []
                      
              else:
                  if(num_tw_day ==1):
                    text_tweets_day.append({"text": text_tweets_user[j-1],"lang": lang_text_tweet[j-1],"RT": is_RT_list[j-1]})
                    tweet_date_day.append(tweets_date[j-1])
                  #+1 because dont sum the last interation
                  num_tw_days.append(num_tw_day)
                  text_tweets_days.append([i for n, i in enumerate(text_tweets_day) if i not in text_tweets_day[n + 1:]] )
                  tweet_date_days.append(list(dict.fromkeys(tweet_date_day)))           
                  num_tw_day = 1 
                  text_tweets_day = []
                  tweet_date_day = []
        if "@" in (text_tweets_user[j]):
            split_text = text_tweets_user[j].split()
            check = "@"
            screen_name_mention1 = [idx for idx in split_text if idx.lower().startswith(check.lower())] 
            if not screen_name_mention1:
                    screen_name_mention.append(["Empty"])
            else:
                screen_name_mention1 = re.sub("[\[\]\'\"!@?¿#$:….,]", '',str(screen_name_mention1)).split(", ")
                if(text_tweets_user[j].startswith('RT',0)):
                    screen_name_mention.append([screen_name_mention1[0]])                    
                else:
                    screen_name_mention.append(screen_name_mention1)
        else:
            screen_name_mention.append(["Empty"])

    if(len(set(text_duplicated)) != len((text_duplicated))):
        duplicated.append(len(text_duplicated) - len(set(text_duplicated)))
    else:
        duplicated.append(0)
    
    #Maximun tweets for user
    if not num_tw_days:
        text_tweets_days_list.append([{"text":"Empty", "lang":"und","RT":2}])
        tweet_date_days_list.append(["Empty"])
        tw_per_day_list.append([0])
    else:
        text_tweets_days_list.append(text_tweets_days)
        tweet_date_days_list.append(tweet_date_days)
        tw_per_day_list.append(num_tw_days)
   
    tw_day_list.append(list(sorted(set(tweets_date.dt.date), reverse=True)))
    screen_name_mention_user.append(screen_name_mention)
    seasonalityDF.append(np.std(time_btw_tw))
    tweets_urlDF.append(tweets_url)
    mentionsDF.append(mentions)
    text_tweetsDF.append(tweets)
    fav_twDF_list.append(favorite_list)
    ret_twDF_list.append(retweet_list)
    fav_twDF.append(int(sum(favorite_list)))
    ret_twDF.append(int(sum(retweet_list)))
    ntwPro_DF.append(int(len(tweets)))
    RT_tw.append(int(len(RT)))
    minu_tw.append(int(sum(time_btw_tw)))
    #Time between tweets and its answer
    if not tw_answer:
        minu_tw_answer.append(0)
    else:   
        minu_tw_answer.append(int(sum(tw_answer))/len(tw_answer))
        
    return [screen_name_mention_user,seasonalityDF,tweets_urlDF,mentionsDF,text_tweetsDF,
            fav_twDF_list,ret_twDF_list,fav_twDF,ret_twDF,RT_tw,ntwPro_DF,minu_tw,tw_per_day_list,
            text_tweets_days_list,tweet_date_days_list,duplicated,minu_tw_answer,tw_day_list]

def time_twitter_account(df):

    anio_actual = time.strftime("%Y")
    df["creation_day"] = 0
    df["twitter_years"] = 0
    for i in range(len(df)):
        df["creation_day"][i] = df.iloc[i]["created_at"].split(' ')[-1]
        df["twitter_years"][i] = int(anio_actual) - int(df['creation_day'][i]) + 1
    return df

def time_series_tw (df):
    for index, row in df.iterrows():
        restart=True
        while restart == True:
            restart=False
            for k in range(len(df.loc[index, "tw_day_list"])-1):
                if(int((df.loc[index, "tw_day_list"][k] - df.loc[index,"tw_day_list"][k+1]).days))>1:
                    times = int((df.loc[index, "tw_day_list"][k] - df.loc[index,"tw_day_list"][k+1]).days)
                    for j in range(times-1):
                        df.loc[index,"tw_per_day_list"].insert(k+1,0)
                        df.loc[index, "tweet_date_days_list"].insert(k+1,["Empty"])
                        df.loc[index,"text_tweets_days_list"].insert(k+1, [{"text":"Empty","lang": "und","RT":2}])
                        df.loc[index, "tw_day_list"].insert(k+j+1, (df.loc[index,"tw_day_list"][k] - timedelta(days=j+1)))
                    restart = True
    return df 

#-------------------------------------------Ratios and other advanced features----------------------------------#
def advanced_features(data):

    #Posible bot
    data["screen_name_bot"] = 0 
    data["days_with_tw"] = 0
    data["max_fav_tw"] = 0
    data["max_ret_tw"] = 0
    data["follow_rate"] = 0
    data["max_tw_day"] = 0
    data["index_max_day_tw"]=0
    for i in range(len(data)):
        if (len(data.iloc[i]["screen_name"]) > 4):
            if((data.iloc[i]["screen_name"][-1].isdigit()) & (data.iloc[i]["screen_name"][-2].isdigit()) & 
                (data.iloc[i]["screen_name"][-3].isdigit()) &(data.iloc[i]["screen_name"][-4].isdigit())):
                data["screen_name_bot"].iloc[i] = 1
        else:
            data["screen_name_bot"].iloc[i] = 1   

        if(data.iloc[i]["following"]== 0):
            data["follow_rate"].iloc[i] = 0
        else:
            data["follow_rate"].iloc[i] = (data.iloc[i]["following"] / data.iloc[i]["followers"])
        
        #ast.literal_eval cuando se leen los datos del csv porque no recoge bien la lista de valores
        #Favorites and Retweets in their published tweets
        if not ((data["favorite_tweets_list"].iloc[i])):
            data["max_fav_tw"].iloc[i] = 0
        else:
            data["max_fav_tw"].iloc[i] = max((data["favorite_tweets_list"].iloc[i]))
        
        if not ((data["retweet_tweets_list"].iloc[i])):
            data["max_ret_tw"].iloc[i] = 0
        else:
            data["max_ret_tw"].iloc[i] = max((data["retweet_tweets_list"].iloc[i]))

        data["max_tw_day"].iloc[i] =max((data["tw_per_day_list"].iloc[i]))
        data["days_with_tw"].iloc[i] = len(data["tw_per_day_list"].iloc[i])
        data["index_max_day_tw"].iloc[i] = data["tw_per_day_list"].iloc[i].index(data["max_tw_day"].iloc[i])
        data["follow_rate"][data["followers"]== 0] = np.median(data["follow_rate"])
        data["num_userTw"]= data["num_ownTw"] + data["RT"]
        data["tw_RT_rate"] = ((((data["num_ownTw"]))) / (data["num_userTw"])).replace([np.inf, -np.inf], np.nan).fillna(0)
        data["sum_fav_RT_ownTw"] = (data["retweet_tweets_count"] + data["favorite_tweets_count"]).replace([np.inf, -np.inf], np.nan).fillna(0)
        data["iter_fav_RT_rate"] = (data["sum_fav_RT_ownTw"] / data["num_ownTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
        data["tw_year_rate"] = ((data["statuses_count"]) / (data["twitter_years"])).replace([np.inf, -np.inf], np.nan).fillna(0)
        data["time_tw_rate"] = (data["time_btw_tw"] / data["num_userTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
        data["seasonality"] = data["seasonality"].replace([np.inf, -np.inf], np.nan).fillna(0)
        data["fake_sum"] = data["default_profile_image"] + data["biography_profile"]+ data["screen_name_bot"]
        data["fake_rate"] = ((data["tweets_url"] + data["mentions"]) /data["num_ownTw"]).replace([np.inf, -np.inf], np.nan).fillna(0)
    data = trend_tweets_features(data) 
        
    return data

def trend_tweets_features(data):
    data["num_anom"] = 0
    data["trend"] = 0
    data["anom_rate"] = 0
    for i in range(len(data)):
        #trend rates
        if len(data.iloc[i]["tw_per_day_list"]) >4:
            df_aux= pd.DataFrame(data.iloc[i]["tw_per_day_list"])
            df_aux["floor"] = df_aux[0].mean() - 1.33 * df_aux[0].std()
            df_aux["roof"] = df_aux[0].mean() + 1.33 * df_aux[0].std() 
            df_aux["anom"] = df_aux.apply(lambda row: row[0] if (row[0]<= row["floor"] or 
                                                                 row[0]>= row["roof"]) else 0, axis =1) 
            data["num_anom"].iloc[i] = len(list(filter(lambda x: x != 0, df_aux["anom"])))
            data["anom_rate"].iloc[i] = data["num_anom"].iloc[i] / len(data["tw_per_day_list"].iloc[i])
            if (data["num_anom"].iloc[i] ==1):
                if max(df_aux["anom"])== data["max_tw_day"].iloc[i]:
                    data["trend"].iloc[i] = 0
                else:
                    data["trend"].iloc[i]=1                    
            else:
                if data["max_tw_day"].iloc[i] in list(filter(lambda x: x != 0, df_aux["anom"])):                    
                    data["trend"].iloc[i] = 0
                else:
                    data["trend"].iloc[i]=1  
        else:
            data["trend"].iloc[i] =2 
            data["num_anom"].iloc[i] =0
            data["anom_rate"].iloc[i]=0
    return data
#----------------------------------------------Filters-------------------------------------------------------#



def filter_possible_irregular_profiles(data_join):
    data_join["evaluate_NLP"] ="No"   
    
    
    #Profiles old spreader
    data_join["evaluate_NLP"][(data_join["index_max_day_tw"] >=30) & (data_join["profile_type"]==False) &
                  (data_join["max_tw_day"]>60)] ="NLP-F0"  
    
    #Profiles with low number of tweets but with a high iteration
    data_join["evaluate_NLP"][(data_join["trend"] == 0) & (data_join["profile_type"]==False) &
                  (data_join["max_tw_day"]<40) & (data_join["tw_RT_rate"]<0.2) &
                 ((data_join["max_ret_tw"]>500) | (data_join["max_fav_tw"]>500))] ="NLP-F1"
    
    #Profiles with a high number of RT in a especific day (try to spread information)
    data_join["evaluate_NLP"][(data_join["trend"] == 0) & (data_join["profile_type"]==False) &
                  (data_join["max_tw_day"]>150) & (data_join["tw_RT_rate"]<0.1) & 
                (data_join["evaluate_NLP"]=="No")] = "NLP-F2"
    
    #Possible influencer profile
    data_join["evaluate_NLP"][(data_join["trend"]==1) & (data_join["profile_type"]==False) &
             (data_join["in_degree"]>=5) & (data_join["followers"]>=3000) &
             (data_join["evaluate_NLP"]=="No")] = "NLP-F3"
    
    #Possible constant spreader
    data_join["evaluate_NLP"][(data_join["trend"]==1) & (data_join["profile_type"]==False) &
             (data_join["out_degree"]>=2) & (data_join["following"]>=3000) & (data_join["evaluate_NLP"]=="No")] = "NLP-F4"                

    #Possible new account with a high activity last days
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) &
             (data_join["twitter_years"]==1) & (data_join["max_tw_day"]>180) &
              (data_join["evaluate_NLP"]=="No")] = "NLP-F5"                     

    #Possible fake behaviour profile in the last days
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) &
             (data_join["fake_sum"]>=2) & (data_join["evaluate_NLP"]=="No")] = "NLP-F6" 
    
    #Possible influencers profile in the last days with a high activity
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) &
             ((data_join["max_ret_tw"]>500) | (data_join["max_fav_tw"]>500)) &
                  (data_join["max_tw_day"]>180) &  (data_join["evaluate_NLP"]=="No")] = "NLP-F7"
    
    #Profiles BOT (more than tweet or RT each 5 minutes the 24 hours)
    data_join["evaluate_NLP"][(data_join["max_tw_day"]>288) &(data_join["profile_type"]==False) &
                             (data_join["evaluate_NLP"]=="No")] ="NLP-8"
    
    data_join["evaluate_NLP"][(data_join["trend"]==2) & (data_join["profile_type"]==False) & 
                              (data_join["max_tw_day"]>180) & (data_join["evaluate_NLP"]=="No")] = "More Data"

    return data_join

def NLP_analysis(data, keyword_corpus, hashtag_corpus):
	tweets = data["text_tweets_days_list"]
	tweets_join = [j for i in tweets for j in i]
	tweets_df = pd.DataFrame(tweets_join)
	tweets_df = tweets_df[tweets_df["RT"] !=2].reset_index(drop=True)
	tweets_df = sentiental_analysis_features(tweets_df)
	sample_data_tokenized = tokenize_tweets(tweets_df)
	tweets_df = keyword_score(tweets_df, sample_data_tokenized,keyword_corpus)
	tweets_df = hashtag_score(tweets_df, sample_data_tokenized,hashtag_corpus)	
	tweets_df["terrorist_suggestion"] = 0
	tweets_df["terrorist_suggestion"][(tweets_df["hashtag_score"]>0) | (tweets_df["keyword_score"]>0)] = 1
	data["per_hash_key"] = len(tweets_df[tweets_df["terrorist_suggestion"]==1]) / len(tweets_df[tweets_df["terrorist_suggestion"]==0])
	tweets_df["terrorist_suggestion"][(tweets_df["terrorist_suggestion"]==1) & (tweets_df["polarity"] < -0.1) & (tweets_df["subjectivity"]>0.6)]= 2
	data["per_terr_hash_key"] = len(tweets_df[tweets_df["terrorist_suggestion"]==2]) / len(tweets_df[tweets_df["terrorist_suggestion"]==1])
	data["suggestion"] = "No terrorist"
	data["suggestion"][((data["per_terr_hash_key"]) >0.7) & (data["per_hash_key"]>0.15))] = "Terrorist"
	
	return data,tweets_df
	
def more_tweets_required(df,consumerKey,consumerSecret,accessToken,accessTokenSecret):
	df_evaluate = df[(df["evaluate_NLP"] !="No") & (df["evaluate_NLP"] !="More Data")]
	node_list_moreData = list(df[df["evaluate_NLP"]=="More Data"]["screen_name"])
	if len(node_list_moreData) >0:
		df_metadata_moreData, list_more_Data_noData = user_timeline_extraction(node_list_moreData,consumerKey,consumerSecret,accessToken,accessTokenSecret,5,"fichero_guardar_noData.csv")
		df_metadata_moreData = filter_possible_irregular_profiles(df_metadata_moreData)
		df_metadata_moreData = df_metadata_moreData[(df_metadata_moreData["evaluate_NLP"] !="No") & (df_metadata_moreData["evaluate_NLP"] !="More Data")]
		df_evaluate = df_evaluate.append(df_metadata_moreData, ignore_index=True)
	return df_evaluate

	
def evaluate_NLP_profiles(data,keyword_corpus, hastag_corpus):	
	for i in range(len(data)):
		profile_evaluated, tweets_df = NLP_analysis(data.iloc[i], keyword_corpus, hashtags_corpus)
		data.iloc[i] = profile_evaluated	
	return data