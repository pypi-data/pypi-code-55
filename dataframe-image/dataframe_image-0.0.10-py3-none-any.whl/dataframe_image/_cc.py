import aiohttp

import json
import asyncio
import base64

from _screenshot import get_chrome_path
from subprocess import Popen


args = [get_chrome_path(),
    '--headless',
    '--disable-gpu', 
    '--run-all-compositor-stages-before-draw',
    '--remote-debugging-port=9222'
]
p = Popen(args=args)

async def handler(ws, data, key=None, p=None):
    await ws.send_json(data)
    async for msg in ws:
        print(type(msg))
        try:
            print('trying to get json')
            msg_json = msg.json()
        except Exception as e:
            print('error is ' ,e)
            print(msg)
            p.kill()
            raise Exception('fuck')

        if 'result' in msg_json:
            result = msg_json['result'].get(key)
            break
    return result

async def main(url):    
    async with aiohttp.ClientSession() as session:
        connected = False
        await asyncio.sleep(3)
        for i in range(10):
            try:
                print(f'attempt {i}')
                resp = await session.get('http://localhost:9222/json')
                data = await resp.json()
                page_url = data[0]['webSocketDebuggerUrl']
                connected = True
            except:
                await asyncio.sleep(1)
            if connected:
                break
        if not connected:
            p.kill()
            raise Exception('Could not connect to chrome server')

        async with session.ws_connect(page_url, receive_timeout=1, max_msg_size=0) as ws:
            # first - navigate to html page
            params = {'url': url}
            data = {'id': 1, 'method': 'Page.navigate', 'params': params}
            frameId = await handler(ws, data, 'frameId', p)
            
            # second - enable page
            data = {'id': 2, 'method': 'Page.enable'}
            await handler(ws, data, p=p)

            # third - get html
            params = {'frameId': frameId, 'url': url}
            data = {'id': 3, 'method': 'Page.getResourceContent', 'params': params}
            await handler(ws, data, 'content', p=p)

            # fourth - get pdf
            await asyncio.sleep(1)
            params = {'displayHeaderFooter': False, 'printBackground': True}
            data = {'id': 4, 'method': 'Page.printToPDF', 'params': params}
            pdf_data = await handler(ws, data, 'data', p=p)
            pdf_data = base64.b64decode(pdf_data)
            print(len(pdf_data))
            return pdf_data


url = 'file:///Users/Ted/Google%20Drive/Github%20Repos/dexplo/dataframe_image/notebooks/tempdir/nb.html'
pdf_data = asyncio.run(main(url))
with open('notebooks/tester_aiohttp.pdf', 'wb') as f:
    f.write(pdf_data)

p.kill()