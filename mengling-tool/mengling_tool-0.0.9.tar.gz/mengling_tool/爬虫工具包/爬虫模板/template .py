import mengling_tool.爬虫工具包.爬虫工具 as pc
import mengling_tool.爬虫工具包.selenium工具 as sele

if __name__ == '__main__':
    driver = sele.getDriver()
    cookies = pc.getLocalChromeCookieList('.acg18.moe', 'acg18.moe')

    driver.get('https://acg18.moe/category/hanhua/acg/anime')
    [driver.add_cookie(cookie) for cookie in cookies]
    sele.webDriverWait(driver,20,sele.By.CLASS_NAME,'archive-thumb')
    html = driver.page_source
    soup = pc.getSoup(html)
    print(soup.find('p', class_="post-meta"))
