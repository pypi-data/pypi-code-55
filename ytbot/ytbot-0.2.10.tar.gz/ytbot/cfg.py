import os
import json

# global variables
BASE_PATH = os.getcwd()
BASE_PATH = os.path.join(BASE_PATH,'ytbot_config') # Changing base path to config folder

if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)


def reset():
    '''

        This function is used to delete the configuration files
        created before
        deletes 'accountInfo.json' and
        'videoLinks.txt' from BASE_PATH

    '''
    acc_info = os.path.join(BASE_PATH, 'accountInfo.json')
    video_info = os.path.join(BASE_PATH, 'videoLinks.txt')  
    executable_info = os.path.join(BASE_PATH,'execpath.txt')
    
    if os.path.isfile(video_info):
        os.remove(video_info)

    if os.path.isfile(acc_info):
        os.remove(acc_info)

    if os.path.isfile(executable_info):
        os.remove(executable_info)    

    help_text = '''
Everything has been reset to Zero.
Try 'ytbot configure' to configure before running again

'''
    print(help_text)





def configure(SETTINGS):
    acc_info = os.path.join(BASE_PATH, 'accountInfo.json')
    video_info = os.path.join(BASE_PATH, 'videoLinks.txt')
    executable_info = os.path.join(BASE_PATH,'execpath.txt')
    accounts = []
    videos = []
    path_to_browser = ''


    # check if files exist >> using 'and' operator because if only one exists it will delete that file 
    # and start anew
    if os.path.isfile(acc_info) and os.path.isfile(video_info):
        with open(acc_info) as fa:
            accounts = json.loads(fa.read())
        
        with open(video_info) as fv:
            for line in fv.readlines():
                videos.append(line.strip())
    
    # ask for browser path if the path entered is empty and there is a previously saved path 
    # bot will use that instead 
    # otherwise it will show error
    path_to_browser = askForPath()
    if path_to_browser.strip() == '':
        if os.path.isfile(executable_info):
            with open(executable_info) as fe:
                path_to_browser = fe.read().strip()
        else:
            print('Fetal error!')
            print('No executable path means no browser automation. So script wont work')
    
    # Now we ask for new accounts and video urls
    accounts = askForAccounts(accounts)
    videos = askForVideos(videos)
    
    
    # Now we save credentials and video urls
    with open(acc_info,'w') as fa:
        fa.write(json.dumps(accounts))
    
    with open(video_info,'w') as fv:
        for vid in videos:
            fv.write(vid+'\n')
    
    with open(executable_info, 'w') as fe:
        fe.write(path_to_browser)
    
    success = '''
    
    
Success!!!
Informations are saved. Now to run the bot,
Try 'ytbot run' to start the bot'''
    print(success)




def askForPath():
    help_text = ''' 
    
    
 executable path is needed so the script can use that browser and automate things
. Without a browser executable path, this script won't even run.
 Which browser? -> chromium browser
 Which version? -> developer channel (Keep in mind, stable version or the beta version will not work)
 How to install the browser? -> search on google :)

 '''
    print(help_text)
    path = input('NOW!!!! Please Enter path: ')
    return path


def askForAccounts(acc):
    try:
        help_text = '''
        
        
Hi There! thanks for using this script :)
We need some infos to get going. Give us some disposable 
Google account credentials. Read the Readme.md to know why.
Add atleast 3 accounts. There is no upper limit. 

Press Ctrl+c to stop adding

___________________________________________________________________________
'''
        print(help_text)

        while True:
            newAcc = dict()
            newAcc['username'] = input('Gmail username: ')
            newAcc['pass'] = input('Gmail password: ')      
            acc.append(newAcc)
            print('Account Added!')
            print()
        

    except KeyboardInterrupt as e:
        print('\nExit from google account add Mode!!!')
        return acc


def askForVideos(videos):
    try:
        help_text = '''
Now we need to add youtube video urls. These videos are going to get views

Press Ctrl+c to stop adding

___________________________________________________________________________
'''
        
        print(help_text)
        
        while True:
            newVideo = input('Add yt video Url: ')
            videos.append(newVideo)
            print('Video Added!')
            print()
           
    except KeyboardInterrupt as e:
        print('\nExit from yt video Url Add mode!!!')
        return videos








        
