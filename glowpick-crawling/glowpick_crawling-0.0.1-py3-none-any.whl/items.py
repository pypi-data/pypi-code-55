import json
import requests
import pandas as pd

class glowpick_items():

    def __init__(self, authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnbG93cGljay53ZWIiLCJpYXQiOjE1OTAwMzg1NjgsInN1YiI6Imdsb3dwaWNrLWF1dGgiLCJpc3MiOiJnbG93ZGF5eiIsImV4cCI6MTU5MDEyNDk2OCwiYXVkIjoiSTRXWmlNbTg1YmppUDlaTzI4VUJndDg1WmljRUM4S09iRG9vUEMyb3FKQkF4dVQ1SzJNLzhqUTFtalpoT29QL05wMW9BZVpWZG80bC8xeTBmS0t4N1E9PSJ9.BphqoxydaQfPtCO5n72HcakWEfEM_S8aNPZicV9zRJs'):
        self.authorization = authorization
        self.datas = self.GetId()
        item_df = self.GetDetailInfo()
        item_df['RANK'] = item_df['RANK'].replace(0,'-')
        item_df['PRICE'] = item_df['PRICE'].fillna(0).astype(int)
        self.item_df = item_df

    def GetId(self):

        urls_ls = []
        item_ls = []
        authorization = self.authorization
        headers = ({
            'authorization' : authorization,
            'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'referer' : 'https://www.glowpick.com/beauty/ranking?id=1&level=3',
            })

        for id in range(1,5):
            for cursor in range(1,6):
                offset = (cursor - 1) * 20
                url = f'https://api-j.glowpick.com/api/ranking/category/3/{id}?cursor={cursor}&id={id}&idBrandCategory=&order=rank&limit=20&level=3&offset={offset}'
                urls_ls.append(url)

        for url in urls_ls:
            req = requests.get(url, headers = headers)
            data = json.loads(req.text)
            item_ls.append(data)

        return item_ls

    def GetDetailInfo(self):
        
        items = []
        for i in range(len(self.datas)):
            try:
                for data in self.datas[i]['products']:
                    items.append({
                        'ID' : data['idProduct'],
                        'RANK' : data['productRank'],
                        'BRAND' : data['brand']['brandTitle'],
                        'NAME' : data['productTitle'],
                        'VOLUME' : data['volume'],
                        'PRICE' : data['price'],
                        'RATE' : data['ratingAvg'],
                    })
            except:
                pass

        return pd.DataFrame(items)


def glowpick_json(authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnbG93cGljay53ZWIiLCJpYXQiOjE1OTAwMzg1NjgsInN1YiI6Imdsb3dwaWNrLWF1dGgiLCJpc3MiOiJnbG93ZGF5eiIsImV4cCI6MTU5MDEyNDk2OCwiYXVkIjoiSTRXWmlNbTg1YmppUDlaTzI4VUJndDg1WmljRUM4S09iRG9vUEMyb3FKQkF4dVQ1SzJNLzhqUTFtalpoT29QL05wMW9BZVpWZG80bC8xeTBmS0t4N1E9PSJ9.BphqoxydaQfPtCO5n72HcakWEfEM_S8aNPZicV9zRJs'):
    ID_data = pd.read_csv('glowpick_items_data.csv', encoding='utf-8')
    # ID_data = pd.read_csv('glowpick_items_data_lv2.csv', encoding='utf-8') 데이터가 2개
    ID_list = list(ID_data['ID'])
    category = []
    name = []
    keywords = []
    ID = []
    error = []

    for idx, x in enumerate(ID_list):
        url = 'https://api-j.glowpick.com/api/product/{}'.format(x)
        headers = {
        'authority': 'api-j.glowpick.com',
        'method': 'GET',
        'path': '/api/product/{}'.format(x),
        'scheme': 'https',
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization':authorization,
            # 오류나는 경우 authorization 값 부터 수정
        'cache-control': 'no-cache',
        'origin': 'https://www.glowpick.com',
        'pragma': 'no-cache',
        'referer': 'https://www.glowpick.com/product/{}'.format(x),
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        print('{} 중 {}'.format(len(ID_list), idx))

        if response.text == '{"message":null}':
            error.append(x)
            print("error : ", x)
            continue
        else:
            cat = response.json()['data']['categoryInfo'][0]['secondCategoryText']
            name_ = response.json()['data']['productTitle']
            keyword = response.json()['data']['keywords']
            ID.append(x)
            category.append(cat)
            name.append(name_)
            keywords.append(keyword)

    data = {
    'ID':ID,
    'category':category,
    'name':name,
    'keywords':keywords
    }
    error = {
        'error':error
    }

    return pd.DataFrame(data), pd.DataFrame(error)
        


def main_json(authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnbG93cGljay53ZWIiLCJpYXQiOjE1OTAwMzg1NjgsInN1YiI6Imdsb3dwaWNrLWF1dGgiLCJpc3MiOiJnbG93ZGF5eiIsImV4cCI6MTU5MDEyNDk2OCwiYXVkIjoiSTRXWmlNbTg1YmppUDlaTzI4VUJndDg1WmljRUM4S09iRG9vUEMyb3FKQkF4dVQ1SzJNLzhqUTFtalpoT29QL05wMW9BZVpWZG80bC8xeTBmS0t4N1E9PSJ9.BphqoxydaQfPtCO5n72HcakWEfEM_S8aNPZicV9zRJs'):
    
    data_df, error_df = glowpick_json(authorization=authorization)
    return data_df, error_df


def main_items(authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnbG93cGljay53ZWIiLCJpYXQiOjE1OTAwMzg1NjgsInN1YiI6Imdsb3dwaWNrLWF1dGgiLCJpc3MiOiJnbG93ZGF5eiIsImV4cCI6MTU5MDEyNDk2OCwiYXVkIjoiSTRXWmlNbTg1YmppUDlaTzI4VUJndDg1WmljRUM4S09iRG9vUEMyb3FKQkF4dVQ1SzJNLzhqUTFtalpoT29QL05wMW9BZVpWZG80bC8xeTBmS0t4N1E9PSJ9.BphqoxydaQfPtCO5n72HcakWEfEM_S8aNPZicV9zRJs'):
    item_data = glowpick_items().item_df
    return item_data
