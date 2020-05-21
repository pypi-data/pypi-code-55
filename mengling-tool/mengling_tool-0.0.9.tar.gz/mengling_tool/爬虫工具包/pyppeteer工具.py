import asyncio
from pyppeteer import launch
from mengling_tool.爬虫工具包 import 爬虫工具 as pc
import mengling_tool.异步工具 as yb

'''js_str可以为tag、#id.class、.class、#id等形式'''


# 访问网站page.goto(url,{'waitUntil': 'load'， 'timeout': 10000})
# page.close()
# 需要调用协程运行的方法才能使用
async def getBrowser_Page(**args):
    width = args.get('width', 1920)
    height = args.get('height', 1080)
    proxy = args.get('proxy', None)
    executablePath = args.get('executablePath', 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    headless = args.get('headless', False)
    arglist = ['--enable-automation', '--no-sandbox']
    if proxy != None: arglist.append('--proxy-server=' + proxy)  # 使用代理
    browser = await launch(executablePath=executablePath, headless=headless, args=arglist)
    page = await browser.newPage()
    # 防止反爬虫检测
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }')
    # 增加头文件
    await page.setUserAgent(pc.cro_headers['User-Agent'])
    # 设置窗口尺寸
    await page.setViewport({'width': width, 'height': height})
    return browser, page


async def screenshot(page, filepath):
    await page.screenshot({'path': filepath})


async def sleep(time: int):
    await asyncio.sleep(time)


# 跳转至底部
async def jumpBottom(page):
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')


# 模拟下滑至底部
async def scroll(page):
    await page.evaluate(""" 
        (function () { 
            var y = document.body.scrollTop; 
            var step = 100; 
            window.scroll(0, y); 
            function f() { 
                if (y < document.body.scrollHeight) { 
                    y += step; 
                    window.scroll(0, y); 
                    setTimeout(f, 50); 
                }
                else { 
                    window.scroll(0, y); 
                    document.title += "scroll-done"; 
                } 
            } 
            setTimeout(f, 1000); 
        })(); 
        """)


# 获取元素对象
async def getElements_xpath(element, xpath_str):
    return await element.xpath(xpath_str)


# 获取元素对象
async def getElements_js(element, js_str):
    return await element.querySelectorAll(js_str)


# 批量获取元素属性或文本
async def getAttributesValues(attribute, *elements):
    texts = []
    for element in elements:
        text = await (await element.getProperty(attribute if attribute != 'text' else 'textContent')).jsonValue()
        texts.append(text)
    return texts


# 获取单个元素属性或文本
async def getAttributeValue(attribute, element):
    return await (await element.getProperty(attribute if attribute != 'text' else 'textContent')).jsonValue()


# 获取单个元素属性或文本
# js_str可以为tag、#id.class、.class、#id等形式
async def getAttributeValue_js(element, js_str, attribute):
    return await element.Jeval(js_str, 'node => node.' + (attribute if attribute != 'text' else 'textContent'))


# 获取源码
async def getHtml(page):
    return await page.content()


# 触发输入事件
async def keyInput(page, js_str, value, delay=100):
    await page.type(js_str, value, {'delay': delay})


# 触发点击事件
async def click(page, js_str):
    # 浏览器不能处于最小化，否则会一直等待
    await page.click(js_str)


# 模拟滑块拖动
async def slideDrag(page, js_str, x, delay=1500):
    await page.hover(js_str)  # 不同场景的验证码模块能名字不同。
    await page.mouse.down()
    await page.mouse.move(x, 0, {'delay': delay})
    await page.mouse.up()


# 聚焦元素，便于直接调用鼠标或键盘操作
async def focus(page, js_str):
    page.focus(js_str)


def pyppeteer_tool(urls, n, **args):
    # cookies = pc.getLocalChromeCookieList('.acg18.moe', 'acg18.moe', '.acgget.com')
    html_dict = dict()
    cookies = args.get('cookies', [])
    timeout = args.get('timeout', 30000)
    waitUntils = ['domcontentloaded', 'load', 'networkidle0', 'networkidle2']
    wait_index = args.get('wait_index', 0)
    wait_js_str = args.get('wait_js_str', None)
    wait_xpath_str = args.get('wait_xpath_str', None)
    tns = 0

    async def temp(urls, cookies, timeout, waitUntil):
        nonlocal html_dict
        nonlocal tns
        tn = tns
        tns += 1
        browser, page = await getBrowser_Page()
        await page.setCookie(*cookies)
        for url in urls:
            html = ''
            for ci in range(1, 4):
                try:
                    await page.goto(url, {'waitUntil': waitUntil, 'timeout': timeout})
                    if wait_js_str != None: await page.waitFor(wait_js_str, {'timeout': timeout})
                    if wait_xpath_str != None: await page.waitForXPath(wait_xpath_str, {'timeout': timeout})
                    html = await page.content()
                    break
                except Exception as e:
                    print(e)
                    print('协程', tn, '失败，正在重试...第', ci, '次')
                    await asyncio.sleep(2)

            if html == '': print(url, '访问失败，以跳过')
            html_dict[url] = html
            await asyncio.sleep(1)
        await browser.close()

    tasks_url = yb.getTasks(n, urls)
    tasks = [temp(us, cookies, timeout, waitUntils[wait_index]) for us in tasks_url]
    yb.tasksRun(*tasks)
    # while len(html_dict.keys()) < len(urls):
    #     asyncio.sleep(1)
    return html_dict
