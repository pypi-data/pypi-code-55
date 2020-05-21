import time
import http.client as httplib
from datetime import datetime, timezone

# %%
def _now():
    return datetime.utcnow().replace(tzinfo=timezone.utc)

# %%
def _internet(url='www.google.com', return_status=False, verbose=3):
    # Check whether server is still alive.
    counter=1
    status=False
    sleepinsec=60

    while status is False:
        conn = httplib.HTTPConnection(url, timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            status=True
        except:
            print('[slacki] >ERROR: [%s] No internet connection? Trying again in 60 sec.. [attempt %s]' %(_now().strftime('%d-%m-%Y %H:%M'), counter))
            status=False
            time.sleep(sleepinsec)
            counter=counter+1

    if counter>1:
        if verbose>=3: print('[slacki] >[%s] Internet connection re-established after after %s attempts.' % (_now().strftime('%d-%m-%Y %H:%M'), counter))
    
    if return_status:
        return(status)


#%% Check the connection with slack. Do this only once otherwise it will result in to many requests error
def _slack(sc, return_status=False):
    # Check connection
    counter=1
    status=False
    sleepinsec=60

    while status is False:
        try:
            getconnection=sc.rtm.connect()
            status = getconnection.successful
        except:
            print('[slacki] >ERROR: [%s] No Slack (aka internet) connection? Trying again in 60 sec.. [attempt %s]' %(_now().strftime('%d-%m-%Y %H:%M'), counter))
            status=False
            time.sleep(sleepinsec)
            counter=counter+1

    if counter>1:
        if verbose>=1: print('[slacki] >[%s] Slack connection re-established after after %s attempts.' % (_now().strftime('%d-%m-%Y %H:%M'), counter))

    if return_status:
        return(status)
