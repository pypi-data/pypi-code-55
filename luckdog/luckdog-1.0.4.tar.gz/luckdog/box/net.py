# -*- coding: utf-8 -*-

from luckdog.net.emnu import HeaderEmnu ,ContentTypeEmnu
from luckdog.net.http import HEADER, COOKIES
from luckdog.net.http import browser
from luckdog.utils.tools import util_json

def box(app,env):
    # browser2 = WBrowser()
    cookies = COOKIES()
    cookies.init("csrftoken=5u0dWiHHwu9l61SUpwt6yAr7KIjRi7kXp58Tds53eQQuLNGLhY3ng7bdpPwsfzGs; sessionid=clthf2aafzvq1kc3rt16tgkv1hby32ek; _ga=GA1.2.448745483.1585635101; ymmoa_passport=U3KGzFNNCjJj9D8NEBecitKiXD5PBtXgStZ9T3-OUaTZt25MQ6rIV2mUq3oCDStfimhj3QmDXGWGf_w6VPDWz1JPTXFgmG2phbmYaXC1T6gF85wgoAn9aA7jYHJRXRn0fcoinmsO-XFxO4CihcshkuXw8K39yv3ugMhGQF3rM8c; ymmoa_user={%22name%22:%22%E8%AF%B7%E4%B8%8D%E8%A6%81%E4%BD%BF%E7%94%A8%E6%AD%A4%20Cookie%22%2C%22avatarUrl%22:%22%22%2C%22departmentName%22:%22%E8%AF%B7%E4%B8%8D%E8%A6%81%E4%BD%BF%E7%94%A8%E6%AD%A4%20Cookie%22%2C%22id%22:9999999%2C%22jobNumber%22:%22Y9999999%22}; qa_passport=KswysbzLZmN6oXGCCNO6NT0b8RieqRZagaqbQTxpCKDWxXkf_Nh0q6klg_iv93f2gLBGEeeYRneU0huh9nrflGBbkyYcmb58rI30XsLEpGA5e-1Ye4Ti5OtzDNyCMt7ZE-WiXip9NaNg4Wj8tz5-EyewbfEi768VuVmtEH_6ubI; _gid=GA1.2.1085347497.1587352093; dev_passport=GWLtPheFKjNPOPSsf08CUZXGbza3zJ5KOaW-DcoFBGC2Sm_eWxHxDGzLxP7zBCdYJ8V47Ca6AXUBnDVd0XEfwq7mKHJismw4qtvYBWm6r3MIcwMiEXHQFVgIFCzxyfljI2JEPFlnupOx62v-yRI9e0i1IWtoubhkMuxMIxpylZM; _ssoSeed=1587370132954")
 
    header = HEADER()
    header.add("Host","docker-beidou.amh-group.com")
    header.add(HeaderEmnu.COOKIES,cookies.cookie())
    header.add(HeaderEmnu.ACCEPT,"*/*")

    browser2 = browser
    browser2.method("get")
    url = "https://docker-beidou.amh-group.com/cloud/api/container/"+app+"."+env+"/"
    browser2.url(url)
    browser2.header(header.get_headers())
    # print(header.get_headers())
    browser2.visit()
    
    print("*"*100)
    Response2 = browser2.visit() 
    # print(Response2)
    # print(Response2.text)
     
    src_dict = util_json.json_loads(Response2.text)
    keypath="container->ip@[0]"
    keypath="container->ip@[*]"
    dist = util_json.get_element_by_keypath(keypath, src_dict)
    print(dist)
    print(",".join(dist))

# box()



def getname(name):
    # browser2 = WBrowser()
    cookies = COOKIES()
    cookies.init("csrftoken=5u0dWiHHwu9l61SUpwt6yAr7KIjRi7kXp58Tds53eQQuLNGLhY3ng7bdpPwsfzGs; sessionid=clthf2aafzvq1kc3rt16tgkv1hby32ek; _ga=GA1.2.448745483.1585635101; ymmoa_passport=U3KGzFNNCjJj9D8NEBecitKiXD5PBtXgStZ9T3-OUaTZt25MQ6rIV2mUq3oCDStfimhj3QmDXGWGf_w6VPDWz1JPTXFgmG2phbmYaXC1T6gF85wgoAn9aA7jYHJRXRn0fcoinmsO-XFxO4CihcshkuXw8K39yv3ugMhGQF3rM8c; ymmoa_user={%22name%22:%22%E8%AF%B7%E4%B8%8D%E8%A6%81%E4%BD%BF%E7%94%A8%E6%AD%A4%20Cookie%22%2C%22avatarUrl%22:%22%22%2C%22departmentName%22:%22%E8%AF%B7%E4%B8%8D%E8%A6%81%E4%BD%BF%E7%94%A8%E6%AD%A4%20Cookie%22%2C%22id%22:9999999%2C%22jobNumber%22:%22Y9999999%22}; qa_passport=KswysbzLZmN6oXGCCNO6NT0b8RieqRZagaqbQTxpCKDWxXkf_Nh0q6klg_iv93f2gLBGEeeYRneU0huh9nrflGBbkyYcmb58rI30XsLEpGA5e-1Ye4Ti5OtzDNyCMt7ZE-WiXip9NaNg4Wj8tz5-EyewbfEi768VuVmtEH_6ubI; _gid=GA1.2.1085347497.1587352093; dev_passport=GWLtPheFKjNPOPSsf08CUZXGbza3zJ5KOaW-DcoFBGC2Sm_eWxHxDGzLxP7zBCdYJ8V47Ca6AXUBnDVd0XEfwq7mKHJismw4qtvYBWm6r3MIcwMiEXHQFVgIFCzxyfljI2JEPFlnupOx62v-yRI9e0i1IWtoubhkMuxMIxpylZM; _ssoSeed=1587370132954")
 
    header = HEADER()
    header.add("Host","docker-beidou.amh-group.com")
    header.add(HeaderEmnu.COOKIES,cookies.cookie())
    header.add(HeaderEmnu.ACCEPT,"*/*")

    browser2 = browser
    browser2.method("get")
    browser2.url("https://docker-beidou.amh-group.com/deploy/api/project/?ns=com.ymm&query=40&page=1&search="+name+"")
    browser2.header(header.get_headers())
    # print(header.get_headers())
    browser2.visit()
    
    print("*"*100)
    Response2 = browser2.visit() 
    # print(Response2)
    # print(Response2.text)
     
    src_dict = util_json.json_loads(Response2.text)
    keypath="container->ip@[0]"
    keypath="results->project@[0]->ns"
    dist = util_json.get_element_by_keypath(keypath, src_dict)
    print(dist)
    return dist
# qa zh 
box(getname("truck-iov-app"),"qa")