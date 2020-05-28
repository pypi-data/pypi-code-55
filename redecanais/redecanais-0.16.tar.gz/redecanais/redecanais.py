# -*- coding: utf-8 -*-
#
import re
import sys
import time
import shutil
import webbrowser
import http.server
import socketserver
import threading
import requests
from os import environ
from redecanais.settings import URL_SERVER
from sys import platform as _sys_platform
from redecanais.player import html_player
from bs4 import BeautifulSoup

BASE_URL = URL_SERVER


def _get_platform():
    if 'ANDROID_ARGUMENT' in environ:
        return 'android'
    elif environ.get('KIVY_BUILD', '') == 'ios':
        return 'ios'
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'
    elif _sys_platform == 'darwin':
        return 'macosx'
    elif _sys_platform.startswith('linux'):
        return 'linux'
    elif _sys_platform.startswith('freebsd'):
        return 'linux'
    return 'unknown'


platform = _get_platform()
print(f'Sistema Operacional {platform} suportado!!!')


class SimpleServerHttp:
    handler = http.server.SimpleHTTPRequestHandler

    def __init__(self):
        print('initializing...')
        self.server = socketserver.TCPServer(("0.0.0.0", 9090), self.handler)
        print("Serving at port", 9090)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


class Browser:

    def __init__(self):
        self.request = None
        self.response = None
        self.session = requests.Session()

    def headers(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
        }
        return headers

    def open(self, url, referer=None, is_response=False, **kwargs):
        if referer:
            headers = self.headers()
            headers['referer'] = referer
        else:
            headers = self.headers()
        with requests.session() as s:
            if kwargs:
                payload = kwargs
                self.response = s.post(url=url, data=payload).text
            else:
                self.request = s.get(url, headers=headers)
                self.response = self.request.text
                if is_response:
                    return self.request
        return self.response


class ChannelsNetwork(Browser):

    def __init__(self):
        super().__init__()

    def search(self, parameter=None):
        if parameter:
            film_name = parameter
        else:
            film_name = input('Digite o nome do filme que deseja assistir: ')
        # url_search = f'{BASE_URL}/search.php?keywords={film_name.replace(" ", "+")}&video-id='
        data = {"queryString": film_name}
        url_search = f'{BASE_URL}/ajax_search.php'
        return self.search_filmes(url_search, **data)

    def get_links_categories(self, url, category):
        info_category = self.categories(url, category['category'].capitalize() + ' ')[0]
        html = self.open(BASE_URL + info_category['url'])
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find('div', {'class': 'row pm-category-header-subcats'})
        films = tags.find_all('li')
        categories_list = []
        for info in films:
            result = info.a['href']
            categories_list.append(result)
        return categories_list

    def films(self, url, category, page=None):
        if type(category) is dict:
            categories_list = self.get_links_categories(url, category)
            for item in categories_list:
                if category['genre'] in item.lower():
                    pages = re.compile(r'videos-(.*?)-date').findall(item)[0]
                    url_category_films = BASE_URL + item.replace(pages, str(category['page']))
                    return self.films_per_category(url_category_films)
        else:
            info_category = self.categories(url, category.capitalize() + ' ')[0]
            pages = re.compile(r'videos(.*?)date').findall(info_category['url'])[0]
            if page is not None:
                url_category_films = BASE_URL + info_category['url'].replace(pages, '-' + str(page) + '-')
            else:
                url_category_films = BASE_URL + info_category['url'].replace(pages, str(category['page']))
            return self.films_per_category(url_category_films)

    def films_per_category(self, url):
        html = self.open(url)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find('ul', {'class': 'row pm-ul-browse-videos list-unstyled'})
        try:
            films = tags.find_all('div', {'class': 'pm-video-thumb'})
            films_list = []
            for info in films:
                result = info.find_all('a')[1]
                if 'https' not in result.img['data-echo']:
                    img = BASE_URL + result.img['data-echo']
                else:
                    img = result.img['data-echo']
                description = self.get_description(BASE_URL + result['href'])
                dict_films = {'title': result.img['alt'], 'url': BASE_URL + result['href'], 'img': img, 'description': description}
                films_list.append(dict_films)
            return films_list
        except:
            info_warning = soup.find('div', {'class': 'col-md-12 text-center'}).text
            print(info_warning)
            sys.exit()

    def search_filmes(self, url, **kwargs):
        url_genre = url
        html = self.open(url_genre, **kwargs)
        soup = BeautifulSoup(html, 'html.parser')
        films = soup.find_all('li')
        films_list = []
        for info in films:
            if not ' - Episódio' in info.a.text:
                result = info.a
                description = self.get_description(BASE_URL + result['href'])
                dict_films = {'title': result.text, 'url': BASE_URL + result['href'], 'img': '', 'description': description}
                films_list.append(dict_films)
        return films_list

    def films_per_genre(self, url, category=None, genre=None):
        url_genre = url
        html = self.open(url_genre)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find('ul', {'class': 'row pm-ul-browse-videos list-unstyled'})
        films = tags.find_all('div', {'class': 'pm-video-thumb'})
        films_list = []
        for info in films:
            result = info.find_all('a')[1]
            if 'https' not in result.img['data-echo']:
                img = BASE_URL + result.img['data-echo']
            else:
                img = result.img['data-echo']
            description = self.get_description(BASE_URL + result['href'])
            dict_films = {'title': result.img['alt'], 'url': BASE_URL + result['href'], 'img': img, 'description': description}
            films_list.append(dict_films)
        return films_list

    def categories(self, url, category=None):
        html = self.open(url)
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('li', {'class': 'dropdown-submenu'})[0]
        tags.ul.unwrap()
        new_html = str(tags).replace('dropdown-submenu', '').replace('</a>\n', '</a> </li>')
        new_soup = BeautifulSoup(new_html, 'html.parser')
        new_tags = new_soup.find_all('li')
        category_list = []
        for info in new_tags:
            if category is not None:
                if category == info.text.replace('ç', 'c'):
                    category_dict = {'category': info.text, 'url': info.a['href']}
                    category_list.append(category_dict)
            else:
                category_dict = {'category': info.text, 'url': info.a['href']}
                category_list.append(category_dict)
        return category_list

    def get_description(self, url):
        html = self.open(url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            tags = soup.find('div', {'id': 'content-main'})
            films = tags.find_all('div', {'itemprop': 'description'})
            if not films:
                result = 'Conteúdo sem descrição!!!'
                return result
            else:
                for info in films:
                    result = info.text.replace('\n', '')
                    return result
        except:
            return 'Conteúdo sem descrição!!!'

    def get_player(self, url):
        html = self.open(url)
        iframe = BeautifulSoup(html, 'html.parser')
        url_player = iframe.find('div', {'id': 'video-wrapper'}).iframe['src']
        embed = iframe.find('meta', {'itemprop': 'embedURL'})['content']
        get_link = self.check_link(url_player, embed=BASE_URL + embed)
        if get_link is not None:
            url_player.replace(BASE_URL, '')
            url_player_dict = {'embed': url_player, 'player': get_link}
        else:
            print('Algo deu errado, nenhum player de vídeo encontrado...')
            url_player_dict = {}
        return url_player_dict

    def check_link(self, url, embed):
        for i in range(1, 10):
            split_link = url.split('?')
            # player_link = f'{BASE_URL}/player{i}/serverf{i}-bk3.php?{split_link[1]}'
            player_link = f'{BASE_URL}/player{i}/serverf{i}.php'
            test_url = self.open(player_link, referer=embed, is_response=True)
            if test_url.status_code == 200:
                return player_link
            else:
                player_link.replace('.php', 'playerfree.php')
                test_url = requests.get(player_link)
                if test_url.status_code == 200:
                    return player_link

    def get_stream(self, url=None, referer=None):
        if '&' in url['uri']:
            match = re.compile("vid=(.+?)&gplusid.*?").findall(url['uri'])
            number = ''
            id = match[0]
        else:
            match = re.compile("serverf(.*).*?php.*?vid=(.*)").findall(url['uri'])
            number = match[0][0].replace('.', '')
            id = match[0][1]
        url = f'https://player.ec.cx/player3/serverf{number}hlb.php?vid={id}'
        print(url)
        html = self.open(url, referer)
        soup = BeautifulSoup(html, 'html.parser')
        url_stream = soup.find('div', {'id': 'instructions'}).source['src']
        return url_stream

    def download(self, url):
        filename = url.split('/')[-1].replace('?attachment=true', '')
        print('Downloading...' + filename)
        with requests.get(url, stream=True) as r:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def select_film(self, films, play=False):
        print('\n')
        for index, film in enumerate(films):
            print(str(index) + ' == ' + film['title'])
        print('\n')
        selected = input('Digite o número correspondente ao filme que deseja assistir: ')
        if selected.isalpha():
            print('\nOpção inválida, tente novamente!!!')
            time.sleep(3)
            return self.select_film(films)
        else:
            selected = int(selected)
        try:
            print(films[selected]['url'])
        except:
            print('Esse filme não existe')
            self.select_film(films)
        filme = films[selected]['url']
        title = films[selected]['title']
        img = films[selected]['img']
        description = films[selected]['description']
        player_url = self.get_player(filme)
        video_url = None
        try:
            if 'cometa.top' in player_url:
                video_url = self.get_stream(url=f"https://cometa.top{player_url['player']}", referer=f"https://cometa.top{player_url['embed']}")
            else:
                #video_url = rede.get_stream(url=f"{player_url['player']}", referer=f"{BASE_URL}{player_url['embed']}")
                video_url = self.get_stream(url={'uri': player_url['embed']}, referer='https://dietafitness.fun/')
            print(video_url)
        except:
            print('Desculpe não encontramos o link do filme escolhido,tente novamente inserindo o nome real do filme.')
            films = self.search()
            self.select_film(films)
        if video_url and play:
            self.play(video_url, title, img, description)
        return

    def play(self, url, title=None, img=None, description=None):
        dict_details = {"url": url,
                        "title": title,
                        "img": img,
                        "description": description
                        }
        with open('player.html', 'w') as f:
            f.write(html_player % dict_details)
        simple_server = SimpleServerHttp()
        simple_server.start()
        webbrowser.open('http://localhost:9090/player.html')
        print('Starting video')
        time.sleep(3600)
        simple_server.stop()
        return 'Exiting...'
