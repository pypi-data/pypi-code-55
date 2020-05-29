from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode
from sys import argv,exit
from os import path
import json
import signal

def get():
    if len(argv) > 1:
        app = argv[1]
        print("(Ptyhon)请输入要查找的APP: {}".format(app))
    else:
        app = input("(Ptyhon)请输入要查找的APP: ")
    base_url = 'https://itunes.apple.com/search?'
    parmas = {'term': app,
              'country': 'us',
              'media': 'software',
              'entity': 'software',
              'limit': '10'}
    url = base_url + urlencode(parmas)
    response = urlopen(url)
    jsonObj = json.load(response)
    count = jsonObj["resultCount"]
    if count == 0:
        print("查无此项")
    else:
        for index, item in enumerate(jsonObj['results']):
            print("{} : {}".format(index, item["trackCensoredName"]))
        select_num = input("请输入要查找的项目(0到{}): ".format(index))
        size = ["60x60", "100x100", "512x512"]
        for index, item in enumerate(size):
            print("{} : {}".format(index, item))
        select_size = input("请选择要下载的大小(0到{}): ".format(index))
        image_link = jsonObj['results'][int(select_num)]["artworkUrl{}".format(size[int(select_size)].split("x")[0])]
        image_name = jsonObj['results'][int(select_num)]["trackCensoredName"]
        dir_desktop = path.expandvars('$HOME') + "/Desktop/"
        filename = "{}{}-{}.jpg".format(dir_desktop, image_name, size[int(select_size)])
        urlretrieve(image_link, filename=filename)
        print("🍺 下载完成")

def main():
    try:
        get()
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    # signal.signal(signal.SIGINT, exit(1))
    main()