import asyncio
import os
import json
import time
import pyppeteer
import random
import time

from pyppeteer import launch
from pyppeteer_stealth import stealth


# Global variables needed for all kinds of operations
triedAccounts = 0
approvedAccounts = 0
pendingAccounts = []
view_count = 0
BASE_PATH = os.getcwd()
BASE_PATH = os.path.join(BASE_PATH,'ytbot_config')


# Completed
async def run(SETTINGS):
    if not isConfigured():
        help_text = '''

Bot must be configured before using it!
Try 'bot.py configure' and follow instruction. Then after the
configuration is complete, run the bot with 'bot.py run'

'''
        print(help_text)
        raise SystemExit('Bot must be configured before use!')
    else:
        await launchPuppet(SETTINGS)

# Completed
async def launchPuppet(SETTINGS):
    print('\nTo stop, Press Ctrl+c ')
    time.sleep(2)
    accounts = getAccounts()
    links = getLinks()
    SETTINGS['path'] = getExecutablePath()

    try:
        tasks = [asyncio.ensure_future(puppetShow(user,links,SETTINGS)) for user in accounts]
        await asyncio.gather(*tasks)
        print(pendingAccounts)


    except Exception as e:
        print(e)



# Path = 'C:\\Users\\exploit\\Desktop\\chrome-win\\chrome.exe'
# Completed
async def puppetShow(user,links,SETTINGS):
    try:
        while True:
            print('using profile: ')
            print(user)
            print('\n')
            print('forwarded links: ')
            print(links)
            print('\n')
            print('used settings: ')
            print(SETTINGS)
            print('____________________________________________')
            try:
                await asyncio.sleep(random.randint(2,15))
                browser = await launch(
            headless= SETTINGS['headless'],
            executablePath = SETTINGS['path'],
            args = ['--no-sandbox','--disable-setuid-sandbox'],
            ignoreHTTPSErrors = True,
            )
                page = await browser.newPage()
                await stealth(page)
                page.setDefaultNavigationTimeout(80*1000)
                logged_in = await googleLogin(user,page)

                if logged_in:
                    await asyncio.sleep(15)
                    await colabPuppet(links,page)
                else:
                    print('login failed')
            except KeyboardInterrupt as e:
                raise SystemExit('The bot will now shut down...')
            except Exception as e:
                try:
                    await browser.close()
                except:
                    print('browser already closed')
                print(e)

    except KeyboardInterrupt:
        raise SystemExit('Exiting from browser')

    except pyppeteer.errors.TimeoutError as e:
        print(str(e))
        try:
            await browser.close()
        except:
            print('browser already closed')



# Completed
def showInfos():
    # global approvedAccounts
    # global triedAccounts
    # global pendingAccounts

    print('tried accounts ',triedAccounts)
    print('approved accounts ',approvedAccounts)

    if pendingAccounts:
        print('some Accounts are being processed')
    else:
        print('all done!!!')



# NotCompleted
async def colabPuppet(links,page):
    # Infos are displayed for user
    showInfos()

    # This code will be written in the first cell of BotSeed google colab file
    code = f'links = {stringifyList(links)}'

    await setupColab(page = page, code = code)
    try:
        while True:
            '''this loop does factory reset, run all and then sleep '''
            try:
                await colabResetRun(page = page)
            except KeyboardInterrupt as e:
                raise SystemExit('The bot will now shut down...')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

# NotCompleted
async def colabResetRun(page):
    global view_count

    try:
        await page.click('#ok')
    except Exception as e:
        pass
    print('started looping')
    await asyncio.sleep(2)
    await page.waitForSelector('#runtime-menu-button')
    await asyncio.sleep(2)
    print('found runtime button')
    await page.click('#runtime-menu-button')
    await asyncio.sleep(2)
    print('clicked runtime button')
    await page.waitForSelector('div[command="powerwash-current-vm"]')
    await asyncio.sleep(2)
    await page.click('div[command="powerwash-current-vm"]')
    print('clicking factory reset button')
    await page.waitForSelector('#ok')
    await asyncio.sleep(2)
    await page.click('#ok')
    print('clicking confirmation ok button')
    await asyncio.sleep(2)

    try:
        await page.click('#ok')
    except Exception as e:
        pass
    print('checked if another ok button was present')
    await page.waitForSelector('#runtime-menu-button')
    await asyncio.sleep(2)
    await page.click('#runtime-menu-button')
    print('clicking runtime button again!')
    await asyncio.sleep(2)
    await page.waitForSelector('div[command="runall"]')
    await asyncio.sleep(2)
    await page.click('div[command="runall"]')
    await asyncio.sleep(2)
    print('running all pending commands sequently')

    try:
        await page.click('#ok')
    except Exception as e:
        pass


    # Increase view_count
    view_count += 1
    print('A view completed view count: ',view_count)
    await asyncio.sleep(7 * 60) # This is the view time of each video







# Completed
async def setupColab(page,code):
    await asyncio.sleep(10)
    colab_link = 'https://colab.research.google.com/drive/1Tu7qGmmw3bruw5teb8tnJHmXINchnHC8?usp=sharing'
    await page.goto(colab_link,
                    {'waitUntil':'networkidle2'},
                   )
    await asyncio.sleep(2)
    await page.waitForSelector('#toolbar-open-in-playground',{'timeout':160 * 1000})
    await page.click('#toolbar-open-in-playground')
    await asyncio.sleep(5)
    await page.waitForSelector('div.main-content > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.editor.flex.monaco',
                                {'timeout': 160 *1000}
                                )
    await page.click('div.main-content > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.editor.flex.monaco')
    await asyncio.sleep(5)
    await page.keyboard.type(code,{'delay':50}) # Code is written here
    await asyncio.sleep(5)


# Completed
async def googleLogin(user,page):
    ''' google login via stackoverflow auth '''
    global approvedAccounts
    global triedAccounts
    global pendingAccounts

    triedAccounts += 1
    try:
        await page.goto( 'https://www.stackoverflow.com',
                        {'waitUntil':'networkidle2'},
                       )
        await page.waitForSelector("a[href^='https://stackoverflow.com/users/login?']")
        await page.click("a[href^='https://stackoverflow.com/users/login?']")
        await page.waitForSelector('button[data-provider = "google"]')
        await page.click('button[data-provider = "google"]')
        await page.waitForSelector('input',{'timeout':80*1000})
        await asyncio.sleep(10)
        await page.keyboard.type('\t',{'delay':200})
        await asyncio.sleep(5)
        await page.keyboard.type(user['username'],{'delay':50})
        await asyncio.sleep(5)
        await page.keyboard.type('\n')
        await page.waitForSelector('input[type="password"]',{'timeout':80*1000})
        await asyncio.sleep(5)
        await page.keyboard.type('\t',{'delay':200})
        await asyncio.sleep(5)
        await page.keyboard.type(user['pass'],{'delay':50})
        await asyncio.sleep(5)
        await page.keyboard.type('\n')
        print('Logged in and counting...')
        approvedAccounts += 1
        print('approved user: ', user['username'])
        return True

    except Exception as e:
        pendingAccounts.append(user)
        raise e




# Completed
def stringifyList(given_list):
    ''' takes a string and makes a string out of that list'''
    stringed_list ='['
    for item in given_list:
        stringed_list += f"'{item}',"
    stringed_list += ']'
    return stringed_list


# Completed
def getAccounts():
    ''' retrives saved accounts'''
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')
    with open(acc_path) as f:
        accounts = json.loads(f.read())
        return accounts
# Completed
def getLinks():
    ''' retrives saved links '''
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    with open(vid_path) as f:
        links = []
        for link in f.readlines():
            links.append(link.strip())
        return links

# Completed
def getExecutablePath():
    ''' retrives saved executable path to chromium browser '''
    executable_path = os.path.join(BASE_PATH,'execpath.txt')
    with open(executable_path) as f:
        path = f.read().strip()
        return path

# Completed
def isConfigured():
    ''' checks if the cofig files exist '''
    acc_path = os.path.join(BASE_PATH,'accountInfo.json')
    vid_path = os.path.join(BASE_PATH,'videoLinks.txt')
    executable_path = os.path.join(BASE_PATH,'execpath.txt')
    if os.path.isfile(acc_path) and os.path.isfile(vid_path) and os.path.isfile(executable_path):
        return True
    else:
        return False

