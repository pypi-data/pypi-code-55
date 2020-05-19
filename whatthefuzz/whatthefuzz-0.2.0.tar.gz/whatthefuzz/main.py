from whatthefuzz import wtfuzz_core
from mitmproxy_api import mitmproxy_api

verb = 'GET'
# host = 'http://docker.hackthebox.eu:39112/administrat/index.php'
# m = mitmproxy_api(host, 'testzap.txt')
# m.getDataFile()
# folders = m.getFolders()
# filename = 'fuzzlist.txt'
# wtf = whatthefuzz()

folders = ['http://192.168.1.12:8081/', 'http://192.168.1.12:8081/WEB-INF/classe', 'http://192.168.1.12:8081/WEB-INF', 'http://192.168.1.12:8081/challenge1']

# wtf.config(host, filename)
# wtf.fuzzInteger('value')

filename = 'actuatortest.txt'
wtf = wtfuzz_core.wtfuzz()
wtf.config(filename=filename)
a = wtf.sendFullRequest_report(verb, folders)
print (a)
#
# verb = 'GET'
#
# wtf.setUrl('https://www.example.org')
# wtf.getPayloads('actuatortest.txt')
# for url in wtf.payloads:
#     wtf.sendFullRequest(url, verb)
