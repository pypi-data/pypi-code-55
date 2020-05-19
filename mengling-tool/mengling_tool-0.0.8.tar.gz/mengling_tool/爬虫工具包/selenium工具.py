from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import mengling_tool.异步工具 as yb
import mengling_tool.进度工具 as jds


# 获取浏览器模拟对象，用于获取动态网页的原始源码
# 模拟浏览器访问操作，需要根据google浏览器版本下载chromedriver.exe
# driver.get(url)模拟进行网址访问
# driver.page_source获取网页源码，需要一定时间解析动态网址，提前获取会出现源码没有全部的原始数据的情况
# driver.close()关闭模拟浏览器
def getDriver(**args):
    ip_porn = args.get('ip_porn', None)
    min_window = args.get('min_window', False)
    max_window = args.get('max_window', False)
    headless = args.get('headless', False)
    options = Options()
    # 设置代理
    if ip_porn != None: options.add_argument(('--proxy-server=' + ip_porn))
    # 设置打开模式为非开发人员模式_无效
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    if headless: options.add_argument("--headless")
    # chromedriver的绝对路径
    path = "D:/python36/chromedriver.exe"
    # 初始化一个driver，并且指定chromedriver的路径
    driver = webdriver.Chrome(executable_path=path, options=options)
    script = '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            '''
    # 设置打开模式为非开发人员模式
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
    if min_window:
        driver.minimize_window()  # 浏览器窗口最小化
    elif max_window:
        driver.maximize_window()  # 浏览器窗口最大化
    return driver


def getHuohuDriver(**args):
    ip_porn = args.get('ip_porn', None)
    min_window = args.get('min_window', False)
    max_window = args.get('max_window', False)
    options = Options()
    # 设置代理
    if ip_porn != None: options.add_argument(('--proxy-server=' + ip_porn))
    # 设置打开模式为非开发人员模式
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    path = r"D:\huohu\geckodriver.exe"
    driver = webdriver.Firefox(executable_path=path, options=options)
    if min_window:
        driver.minimize_window()  # 浏览器窗口最小化
    elif max_window:
        driver.maximize_window()  # 浏览器窗口最大化
    return driver


# 发送get请求
def request_get(driver, url):
    driver.execute_script("""
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '%s', true);
        window.text=-1;
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            window.text= this.responseText;
        };
        xhr.send();
    """ % url)


# 发送post请求
def request_post(driver, url, data):
    if type(data) == dict:
        data = '&'.join(["{key}={value}".format(key=key, value=data[key]) for key in data.keys()])
    driver.execute_script("""
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '%s', true);
        window.text=-1;
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            window.text= this.responseText;
        };
        xhr.send(%s);
    """ % (url, data))


# 等待获取发送后的返回值
def wait_getResponse(driver, maxci=10, mintime=0.5):
    for i in range(maxci):
        time.sleep(mintime)
        text = driver.execute_script("return window.text;")
        if text == None:
            print("没有进行发送请求，无返回值")
            return ""
        if text != -1: return text;
    print('等待时间已过，没有获取到返回值...')
    return ""


# 等待元素加载
def webDriverWait(driver, timeout, constraint, constraint_class='xpath', onetime=0.5):
    if constraint_class == 'xpath':
        constraint_class = By.XPATH
    elif constraint_class == 'id':
        constraint_class = By.ID
    elif constraint_class == 'class':
        constraint_class = By.CLASS_NAME
    elif constraint_class == 'tag':
        constraint_class = By.TAG_NAME
    else:
        print(constraint_class, '约束类型出错，该元素等待方法无效！')
        return None
    if constraint == None: return None
    locator = (constraint_class, constraint)
    WebDriverWait(driver, timeout, onetime).until(EC.presence_of_element_located(locator))


# 模拟输入
def keyin(driver, id, str):
    # driver.execute_script("document.getElementById('" + id + "').value=" + str)
    driver.find_element_by_id(id).send_keys(str)


# 模拟点击
def click(driver, id):
    # driver.execute_script("document.getElementById('" + id + "').onlick")
    driver.find_element_by_id(id).click()


# 模拟浏览器下滑至底部
def scroll(driver):
    driver.execute_script(""" 
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
            setTimeout(f, 500); 
        })(); 
        """)


# 构造移动轨迹
# 不好用，暂时保留
def __get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


# 跳转嵌套页面
def changeFrame_id(driver, iframe_id):
    iframe = driver.find_element_by_id(iframe_id)
    driver.switch_to.frame(iframe)  # 切换到iframe


# 跳转嵌套页面
def changeFrame_xpath(driver, iframe_xpath):
    iframe = driver.find_element_by_xpath(iframe_xpath)
    driver.switch_to.frame(iframe)  # 切换到iframe


# 跳转至最外层页面
def parentFrame(driver):
    driver.switch_to.default_content()


# # 模拟滑块拖动
# def slideDrag_id(driver, x, id):
#     # 一般需要跳转嵌套页面-changeFrame
#     button = driver.find_element_by_id(id)
#     __slideDrag(driver, button, x)


# # 模拟滑块拖动
# def slideDrag_xpath(driver, x, xpath):
#     # 一般需要跳转嵌套页面-changeFrame
#     button = driver.find_element_by_xpath(xpath)
#     __slideDrag(driver, button, x)
#
#
# # 模拟滑块拖动
# def __slideDrag(driver, button, x):
#     action = ActionChains(driver)  # 实例化一个action对象
#     action.click_and_hold(button).perform()  # perform()执行ActionChains中存储的行为
#     action.reset_actions()  # 清除之前的action
#     # for g in __get_track(x):
#     action.move_by_offset(x, 0).perform()  # 移动滑块
#     action.reset_actions()
#     time.sleep(0.5)
#     action.release().perform()  # 松开
#     # 此后进行是否成功的判断
#     # 未完成可以改变x值再次调用
#     # 成功后driver将会跳转至主页面


def slideDragAction(driver, button_element, x, **kwargs):
    """
        滑块解锁
        :param button_element: 滑块元素对象
        :param x: 移动距离
    """
    ci = kwargs.get('ci', 3)
    from selenium.webdriver import ActionChains
    action = ActionChains(driver)  # 实例化一个action对象
    action.click_and_hold(button_element).perform()  # perform()执行ActionChains中存储的行为
    action.move_by_offset(x / ci, 0).perform()  # 移动滑块
    for i in range(ci - 1):
        action.move_by_offset(0, 0).perform()  # 继续执行
        time.sleep(0.5)
    action.reset_actions()


def selenium_tool(urls, n, **args):
    # cookies = pc.getLocalChromeCookieList('.acg18.moe', 'acg18.moe', '.acgget.com')
    html_dict = dict()
    cookies = args.get('cookies', [])
    timeout = args.get('timeout', 15)
    wait_xpath_str = args.get('wait_xpath_str', None)

    @yb.retryFunc
    def urlget(driver, url, timeout):
        driver.get(url)
        [driver.add_cookie(cookie) for cookie in cookies]
        webDriverWait(driver, timeout, wait_xpath_str)
        return driver.page_source

    def urlsget(xci, urls, timeout):
        driver = getDriver(**args)
        for url in urls:
            # 重试机制
            html = urlget(driver, url, timeout, index='线程' + str(xci))
            if html == None:
                html = ''
                print(url, '访问失败，以跳过')
            html_dict[url] = html
        driver.quit()

    tasks_url = yb.getTasks(n, urls)
    tasks = [[i, tasks_url[i], timeout] for i in range(len(tasks_url))]
    # 监听进度
    jd = jds.progress(len(urls), '获取网页源码')
    jd.thread_Listening(html_dict)
    yb.threads_run(urlsget, tasks)
    return html_dict
