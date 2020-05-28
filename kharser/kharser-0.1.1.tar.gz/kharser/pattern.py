import re

#courtesy : https://code.tutsplus.com/tutorials/8-regular-expressions-you-should-know--net-6149
URL = re.compile('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?')
EMAIL = re.compile('([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})')
DIGIT = re.compile('\\b\d{1}\\b')
DIGITS = re.compile('\\b\d{2,}\\b')
#Phone nb
PHONE_E164 ='(?P<prefix>\+\d{1,3}) ?(:?\(\d\))?(?P<local>([0-9][ |.]?){6,14}[0-9])' 
#to match something like tel:+336 12 54 69 87, with `tel` => kind
PHONE_KIND ='(?P<kind>[A-zzA]+)?[:#]? *'
RE_PHONE_E164=re.compile(PHONE_KIND+PHONE_E164) 
RE_PHONE_FR = re.compile(PHONE_KIND+'(?P<phone>(\d{2} ?){5})')
#TODO:
#see if there is any intersting example here : 
#https://github.com/lk-geimfari/expynent/blob/master/expynent/patterns.py
#jour de la semaine e.g. lundi 29 juin 2015
mois = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
str_mois = '|'.join(mois)
jour = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
str_jour_semaine = '|'.join(jour)
RE_DATE_FR= re.compile(f"(?P<jour_semaine>{str_jour_semaine}) (?P<jour>[0-9]{{1,2}}) (?P<mois>{str_mois}) (?P<annee>[0-9]{{4}})")