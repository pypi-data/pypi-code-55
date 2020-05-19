import mengling_tool.爬虫工具包.爬虫工具 as pc
import re


def getUrls(url0, indexs, mark='@@@'):
    return [re.sub(mark, str(i), url0) for i in indexs]


# 获取单位元素字典
def getElementsDict(html_dict, tag_str=None, tag_constraint: dict = {}):
    elementsdict = dict()
    for url in html_dict.keys():
        html = html_dict[url]
        soup = pc.getSoup(html)
        if tag_str != None:
            tags = soup.find_all(tag_str, **tag_constraint)
            if len(tags) == 0: print(url, "没有解析对象")
        else:
            tags = [soup]
        elementsdict[url] = tags
    return elementsdict


# 使用单位元素字典获取子属性值字典
def getAttributeValue(element, tag_str, tag_constraint: dict, attribute):
    tags = element.find_all(tag_str, **tag_constraint)
    values = list()
    if len(tags) == 0:
        print(tag_str, tag_constraint, attribute, "没有解析对象")
    for tag in tags:
        if attribute == 'text':
            value = tag.text
        elif attribute == 'content':
            value = tag.content
        elif attribute == 'string':
            value = tag.string
        else:
            value = tag.attrs.get(attribute, '')
        values.append(value)
    return values

# 项目运行模板函数
def getUrl_values_dict0(获取方法, 网页模板, 最小页码, 最大页码, 线程数, 文章元素, 文章元素约束字典, 子节点标签组, **args):
    urls = getUrls(网页模板, range(最小页码, 最大页码 + 1))
    # 获取源码字典
    html_dict = 获取方法(urls, 线程数, **args)
    # 获取文章元素
    elements_dict = getElementsDict(html_dict, 文章元素, 文章元素约束字典)
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
            for name in 子节点标签组.keys():
                tag_str = 子节点标签组[name][0]
                tag_constraint = 子节点标签组[name][1]
                attribute = 子节点标签组[name][2]
                # 将值进行处理后存入
                edict[name] = valueFormatting(name, getAttributeValue(element, tag_str, tag_constraint, attribute))
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