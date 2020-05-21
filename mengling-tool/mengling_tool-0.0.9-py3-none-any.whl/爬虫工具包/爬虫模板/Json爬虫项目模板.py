import mengling_tool.爬虫工具包.爬虫工具 as pc
import time
import mengling_tool.mysql工具 as sqltools
import ssl
import redis
import mengling_tool.进度工具 as jds
import mengling_tool.爬虫工具包.selenium工具 as sele
import re


def getJsonStr_post(url0, data, datapage: str, pages: list, **args):
    json_str_dict = dict()
    ci = args.get('ci', 3)
    timenum = args.get('timenum', 1)
    jd = jds.progress(len(pages))
    driver = args.get('driver', None)
    for page in pages:
        for i in range(ci):
            try:
                data[datapage] = page
                url = url0 + '?' + '&'.join([(line[0] + '=' + str(line[1])) for line in data.items()])
                if driver != None:
                    driver.get(url)
                    json_str = driver.page_source
                else:
                    json_str = pc.getHtml_open(url, **args)
                key = str(page)
                json_str_dict[key] = json_str
                break
            except Exception as e:
                print(e)
                print('获取页码：', page, '数据失败！')
                print('休息', timenum, 's')
                time.sleep(timenum)
                if i < ci: print('开始重试...第', i + 1, '次')
                continue
        jd.add()
        jd.printProgressBar()
    return json_str_dict


# 获取json字符串数据格式处理后的字典数据
def getJsonHandle(json_str_dict):
    json_pagedict = dict()
    try:
        for page in json_str_dict.keys():
            # 相关格式处理
            json_str = jsonStrHandle(json_str_dict[page])
            # 相关数据选择
            jsondata = jsonDictHandle(pc.getJson(json_str))
            json_pagedict[page] = jsondata
    except Exception as e:
        print(e)
        print('json字符串数据格式处理出错')
    return json_pagedict


# 相关json字符串格式处理
def jsonStrHandle(json_str):
    json_str = re.findall('<body>(.+?)</body>', json_str)[0]
    return json_str


# 相关数据选择json数据格式处理
def jsonDictHandle(json_dict):
    rows = json_dict.get('rows', [])
    for row in rows:
        for key in row.keys():
            if type(row[key]) != str:
                row[key] = ''
    return rows


def insert_mysql(db, table, value_dicts: list):
    sqltool = sqltools.mysqlExecutor(db)
    for value_dict in value_dicts:
        sqltool.insert_dict(table, value_dict)
    sqltool.commit()
    sqltool.close()


def run(url, data, datapage: str, pages: list, **args):
    json_str_dict = getJsonStr_post(url, data, datapage, pages, **args)
    json_pagedict = getJsonHandle(json_str_dict)
    return json_pagedict
    # insert_mysql(db, table, [datadict])


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, db=3)
    r2 = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, db=0)
    driver = sele.getDriver()
    for name in r.keys():
        # name = '招标/资格预审公告'
        try:
            url = r.hget(name, '链接')
            # 获取最大页码
            ye = int(r.hget(name, '页数'))
            if ye % 2 == 1:
                maxye = int(ye / 2) + 1
            else:
                maxye = int(ye / 2)
            print(maxye)
            data = {'page': 1, 'rows': 20}
            pages = range(1, maxye)
            json_pagedict = run(url.replace('Init.do', '.do'), data, 'page', pages, headers={'Host': 'www.whzbtb.com'},
                                driver=driver)
            for line in json_pagedict.items():
                rows = line[1]
                for row in rows:
                    r2.hmset(name + "_" + row['id'], row)
        except Exception as e:
            print(e)
            print()
    # r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    # r.delete(*r.keys('0_*'))
