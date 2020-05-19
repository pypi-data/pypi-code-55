"""
This program validates a URL
Input: http://www.google.com/mail/user=fulano
If it is ok, then the output will be
Output:
    protocolo: http
    host: www
    domínio: google.com
    path: mail
    parâmetros: user=fulano
"""
point = 1
result = {}
while point == 1:
    url = input('Digite una URL: \n')
    if url[-1:] == '/':
        url = url[:-1]
    newurl = url.split('//')
    if newurl[0] == 'http:' or 'https:':
        result['protocolo'] = newurl[0][:-1]
        newurl = newurl[1].split('/')
        if 'www' in newurl[0]:
            result['host'] = newurl[0][:3]
            if '.com' in newurl[0]:
                result['dominio'] = newurl[0][4:]
                result['path'] = newurl[1]
                result['parameters'] = newurl[2]
                point = 0
            else:
                print('Dominio no reconocido')
                break
        else:
            print('Debe digitar el www')
            break
    else:
        print("URL Incorrecta, digite o protocolo")
        break

if __name__ == '__main__':
    for key, value in result.items():
        print(key, ': ', value)
