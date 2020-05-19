# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:56:16 2020

@author: INFiNIE
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:49:35 2020

@author: Kowsher
"""

from pathlib import Path
script_location = Path(__file__).absolute().parent
punc_loc = script_location / "punctuation.yaml"
sw_loc = script_location / "stop_words.yaml"


with open(punc_loc,'r',encoding = 'utf-8') as punctuation_corpus:
    pun_words = [word for line in punctuation_corpus for word in line.split()]
    pun_words_len = len(pun_words)

swords = []
with open(sw_loc,'r',encoding = 'utf-8') as st_corpus:   
    for word in st_corpus:
        swords.append(word)



def remove_punc(inpu):

    inpu_len = len(inpu)
    
    inpu_clean = ""
    for i in range(inpu_len):
        if inpu[i] not in pun_words:
            inpu_clean = inpu_clean + " ".join(inpu[i])
        
        
    return inpu_clean



def remove_sw(target):
    
    target = target.split(' ')
    string=""
    for word in target:
        com = word
        word=word+"\n"
        
        if word not in swords:
            string = string+' '+com
        
    return string.lstrip()
    
