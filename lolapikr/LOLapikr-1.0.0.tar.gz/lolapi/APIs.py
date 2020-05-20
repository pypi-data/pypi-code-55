# -*- coding: utf-8 -*-
"""
Created on Sun May 17 19:56:27 2020

@author: dhk13
"""
import requests
import time
summoner="코코낸내2"

def GetSummonerInfo(summoner_name , api_key):
    res = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +summoner_name +'?api_key=' + api_key
    r = requests.get(res)
    tier_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + r.json()['id'] +'?api_key=' + api_key
    r2  = requests.get(tier_url)
    #print(r2.json())
    if(r2.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return (r2.json())
    elif(r2.status_code==429):
        return False
    else:
        print("Check api key or other problems.")
    
    
#GetSummonerInfo(summoner, api_key)
    
def GetDivInfo(queue="RANKED_SOLO_5X5", tier= "DIAMOND", division=1, api_key=None):
    #[RANKED_SOLO_5x5, RANKED_FLEX_SR, RANKED_FLEX_TT]
    #[DIAMOND, PLATINUM, GOLD, SILVER, BRONZE, IRON]
    #[I, II, III, IV]
    res = "https://kr.api.riotgames.com/lol/league/v4/entries/"+queue+"/"+tier+"/"+division+'?api_key='+api_key
    r=requests.get(res)
    if(r.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return r.json()
    elif(r.status_code==429):
        return False
    else:
        print("Check api key or other problems.")
    #print(r.json())
    
"""
r=GetDivInfo(queue='RANKED_SOLO_5x5', tier= 'BRONZE', division='III',api_key=api_key)
for i in range(len(r)):
    print(r[i]['summonerName'])
"""
    
def GetChallengerDiv(api_key):
    res = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"+'?api_key='+api_key
    r=requests.get(res)
    if(r.status_code==200):
        #print(sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True))
        return sorted(r.json()['entries'], key=lambda summoner:summoner['leaguePoints'], reverse=True)
    elif(r.status_code==429):
        return False
    else:
        print("Check api key or other problems.")
"""
result=GetChallengerDiv(api_key)
for i in result:
    print(i['leaguePoints'])
"""


"""
How To Get Match Data
1. Get Summoner Name that contians Summoner's Id
2. Get Summoner Id that contians Summoner's acc id
3. Get Summoner's encrypted account Id
4. Get Matchlist using account id
5. Get Match Info
"""
#AvdVLfFbT-wZJV2fPrX_uE6l2eZpuFjvKbN1622JMafmRcE
"""
res = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/AvdVLfFbT-wZJV2fPrX_uE6l2eZpuFjvKbN1622JMafmRcE"+'?api_key='+api_key
r=requests.get(res)
#print(r.json())
enc_acc_id=r.json()['accountId']

res = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/"+enc_acc_id+'?api_key='+api_key
r=requests.get(res)
print(r.json()['matches'][0])
res = "https://kr.api.riotgames.com/lol/match/v4/matches/"+str(r.json()['matches'][0]['gameId'])+'?api_key='+api_key
r=requests.get(res)
print(r.json())
"""
