import requests 
from bs4 import BeautifulSoup
import lxml
def get_lyrix(url):
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'lxml')
    lyrix = soup.find('div', class_="lyrics").text
    print(lyrix)

get_lyrix("https://genius.com/F8l-skyfall-lyrics")