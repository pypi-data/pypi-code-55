import mengling_tool.爬虫工具包.爬虫工具 as pc
import mengling_tool.爬虫工具包.pyppeteer工具 as pt
import re
import mengling_tool.mysql工具 as sqltools
import mengling_tool.进度工具 as jds


# 获取单位元素字典
def getElementsDict(html_dict, tag_str=None, tag_constraint: dict = {}):
    elementsdict = dict()
    for url in html_dict.keys():
        html = html_dict[url]
        soup = pc.getSoup(html)
        if tag_str != None:
            tags = soup.find_all(tag_str, **tag_constraint)
            if len(tags) == 0: print(url, "文章没有解析对象")
        else:
            tags = [soup]
        elementsdict[url] = tags
    return elementsdict


# 使用单位元素字典获取子属性值字典
def getAttributeValue(element, tag_str, tag_constraint: dict, attribute):
    # 直接访问母元素
    if tag_str == '':
        tags = [element]
    else:
        tags = element.find_all(tag_str, **tag_constraint)
    values = list()
    if len(tags) == 0:
        print(tag_str, tag_constraint, attribute, "子节点没有解析对象")
    for tag in tags:
        if attribute == 'text':
            value = tag.text
        elif attribute == 'content':
            value = str(tag)
        elif attribute == 'string':
            value = tag.string
        else:
            value = tag.attrs.get(attribute, '')
        values.append(value)
    return values


# 项目运行模板函数
def getUrl_values_dict0(getHtml_func, urls, threadnum, titlelementdicts, childtags_dict, **args):
    # 值的格式处理方法
    valueFormat_func = args.get('valueFormat_func', None)
    # 获取源码字典
    html_dict = getHtml_func(urls, threadnum, **args)
    # 获取文章元素
    # titlelementdicts格式：
    # [标签,约束字典]
    elements_dict = getElementsDict(html_dict, titlelementdicts[0], titlelementdicts[1])
    url_values_dict = dict()
    # 获取文章下的自定义数据值
    for url in urls:
        valuedicts = list()
        url_values_dict[url] = valuedicts
        elements = elements_dict[url]
        # 遍历文章
        for element in elements:
            edict = dict()
            valuedicts.append(edict)
            # childtags_dict格式：
            # 名字:[标签,约束字典,需要属性]
            for name in childtags_dict.keys():
                tag_str = childtags_dict[name][0]
                tag_constraint = childtags_dict[name][1]
                attribute = childtags_dict[name][2]
                # 将值进行处理后存入
                if valueFormat_func != None:
                    edict[name] = valueFormat_func(name, getAttributeValue(element, tag_str, tag_constraint, attribute))
                else:
                    edict[name] = getAttributeValue(element, tag_str, tag_constraint, attribute)
    # {链接:[
    #       {标签1:值1,标签2:值2},
    #       {标签1:值3,标签2:值4}
    #       ...
    #       ],
    #  链接:[
    #       {标签1:值5,标签2:值6},
    #       {标签1:值7,标签2:值8}
    #       ...
    #       ]
    #       ...
    # }
    return url_values_dict


def getUrl_values_dict1(getHtml_func, urls, threadnum, childtags_dict, **args):
    # 值的格式处理方法
    valueFormat_func = args.get('valueFormat_func', None)
    # 获取源码字典
    html_dict = getHtml_func(urls, threadnum, **args)
    # 获取元素
    elements_dict = getElementsDict(html_dict)
    url_values_dict = dict()
    # 获取文章下的自定义数据值
    for url in urls:
        edict = dict()
        url_values_dict[url] = edict
        soup = elements_dict[url][0]
        # 直接获取
        for name in childtags_dict.keys():
            tag_str = childtags_dict[name][0]
            tag_constraint = childtags_dict[name][1]
            attribute = childtags_dict[name][2]
            # 将值进行处理后存入
            if valueFormat_func != None:
                edict[name] = valueFormat_func(name, getAttributeValue(soup, tag_str, tag_constraint, attribute))
            else:
                edict[name] = getAttributeValue(soup, tag_str, tag_constraint, attribute)
    # {链接:{标签1:值1,标签2:值2},
    #  链接:{标签1:值5,标签2:值6},
    #       ...
    # }
    return url_values_dict


def insert_mysql(db, table, value_dicts: list, **args):
    tablekey = args.get('tablekey', None)
    otherlie_data_dict = args.get('otherlie_data_dict', {})
    creatable = args.get('creatable', True)
    if len(value_dicts) == 0:
        print('没有数据插入！')
        return None
    if creatable:
        lies = list(otherlie_data_dict.keys())
        lies.extend(list(value_dicts[0].keys()))
        db.createTable(table, lies, noexistcreate=True, key=tablekey)
    jd = jds.progress(len(value_dicts), '数据插入')
    args['creatable'] = True
    for value_dict in value_dicts:
        db.insert_dict(table, {**value_dict, **otherlie_data_dict})
        jd.add()
        jd.printProgressBar()
    db.commit()


def insert_redis(r, name, value_dicts: list, **args):
    for value_dict in value_dicts:
        # 处理值
        for key in value_dict.keys():
            try:
                # 清除多余值
                value_dict[key].remove('')
            except:
                pass
            value_dict[key] = '\n'.join(value_dict[key])
        r.hmset(name, value_dict)


'''----------------------------------------------------------'''


def getUrls(url0, indexs, mark='@@@'):
    return [re.sub(mark, str(i), url0) for i in indexs]


# 值的格式处理
def tempf(name, values):
    value = values[0]
    try:
        if name == 'args':
            t = re.findall('\d+年\d+月\d+日', value)[0]
            eye = re.findall('<i class="fa fa-eye fa-fw"></i>([0-9,]+)</span>', value)[0].replace(',', '')
            value = {'时间': t, '查看数': eye}
    except:
        pass
    return value


def temp(urls, n, **args):
    return pc.getHtml_threadPool(pc.getHtml_open, urls, n, **args)


if __name__ == '__main__':
    获取方法 = pt.pyppeteer_tool  # pc.
    网页模板, 最小页码, 最大页码 = 'https://acg18.moe/category/hanhua/acg/anime/page/@@@', 11, 11
    网页组 = getUrls(网页模板, range(最小页码, 最大页码 + 1))
    线程数 = 5
    文章元素约束字典 = ['li', {'class_': "pl archive-thumb"}]  # [标签,约束字典]
    子节点标签组 = {  # 名字:[标签,约束字典,需要属性]
        'link': ['a', {'href': True}, 'href'],
        'title': ['a', {'href': True}, 'title'],
        'img': ['img', {'src': True}, 'src'],
        'args': ['p', {'class_': "post-meta"}, 'content'],
    }
    加载元素xpath = '//*[@id="main-content"]//ul/li[1]/article/p[3]'
    cookies = pc.getLocalChromeCookieList('.acg18.moe', 'acg18.moe')
    库名, 表名 = 'kk', '幻想次元'

    # url_values_dict = getUrl_values_dict1(获取方法, 网页组, 线程数, 子节点标签组)
    url_values_dict = getUrl_values_dict0(获取方法, 网页组, 线程数, 文章元素约束字典, 子节点标签组,
                                          cookies=cookies, wait_xpath_str=加载元素xpath)
    for url in url_values_dict.keys():
        insert_mysql(sqltools.mysqlExecutor(库名), 表名, url_values_dict[url], key='link')
