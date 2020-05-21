#--------------------------------------------------------------------------
# Name        : slacki.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
#--------------------------------------------------------------------------

# Libraries
import slacki.utils.check_connection as check_connection
from datetime import datetime
from slacker import Slacker
import traceback
import numpy as np
import time

# %%
class slacki():
    """Python package slacki for reading and posting in slack groups."""

    def __init__(self, channel=None, token=None, response_time=60, verbose=3):
        """Initialize slacki with user-defined parameters."""
        if token is None: raise Exception('Token should be a valid id.')
        # Check internet connection
        check_connection._internet()
        # Check channel name
        channel = get_channel(channel)
        try:
            sc = Slacker(token)
            # check_connection._slack(sc)
        except Exception as e:
            if verbose>1: print(('[slacki] >ERROR: Could not import token: [%s]' % (str(e))))

        # Store in object
        self.sc = sc
        self.channel = channel
        self.channel_id = sc.channels.get_channel_id(channel[1:])
        self.token = token
        self.response_time = response_time
        self.verbose = verbose
        # Make channel if not exists
        make_channel(self.sc, self.channel, verbose=verbose)

    # Retrieve posts
    def retrieve_posts(self, date_from=None, date_to=None, n=None, verbose=3):
        """Retrieve posts

        Parameters
        ----------
        date_from : str: "%Y-%m-%d %H:%M:%S"
            Date From
        date_to : str: "%Y-%m-%d %H:%M:%S"
            Date To
        n : int, default: None
            Retrieve the n latest posts. If set to default=None, all is retrieved.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        list of dict containing posts.

        """
        # Check internet connection
        check_connection._internet()
        oldest = None
        latest = None
        get_posts = []

        # Set date
        if date_from is not None:
            oldest = (datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds()
        if date_to is not None:
            latest = (datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).total_seconds()

        # Retrieve channel IDs of not present yet
        if self.channel_id is None:
            self.channel_id = self.sc.channels.get_channel_id(self.channel[1:])

        # Try to retrieve posts
        try:
            if self.channel_id is None:
                if verbose>=3: print('[slacki] Could not retrieve ID for channel %s. If the channel is set on private, change it to normal and try again.' % (self.channel))
            else:
                # Retrieve History
                GEThistory = self.sc.channels.history(self.channel_id, oldest=oldest, latest=latest, count=n)
                get_posts = GEThistory.body['messages']
        except:
            if verbose>=1: print(traceback.print_exc())

        return(get_posts)

    # Snooze
    def snooze(self, minutes=None, return_status=False, verbose=3):
        """Snooze the slack messages for certain time.

        Parameters
        ----------
        minutes : int, default: None
            Number of minutes to snooze.
        return_status : bool, default: False
            Return the status of the snoozing action.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        status : bool

        """
        try:
            if minutes is not None:
                self.sc.dnd.set_snooze(num_minutes=minutes)        
                if verbose>=3: print('[slacki] >Snoozer for %s is set on %.d minutes' %(self.channel, minutes))
                OK = True
        except Exception as e:
            if verbose>=1: print(('[slacki] >ERROR: [%s]' % (str(e))))
            OK = False

        # Return
        if return_status:
            return(OK)

    # Post message in channel
    def post(self, queries, icon_url=None, return_status=False, verbose=3):
        """Post messages on slack.

        Parameters
        ----------
        queries : list
            list with strings containing messages to be posted.
        icon_url : str
            String with icon url.
        return_status : bool, default: False
            Return the status of the snoozing action.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        status : bool

        """
        if queries is None: raise Exception('Queries should be a string or list with strings.')
        # Check internet connection
        check_connection._internet()
        # Make list if required
        if isinstance(queries, str):
            queries=[queries]
        # Post messages
        try:
            for query in queries:
                self.sc.chat.post_message(self.channel, text=query, username=None, icon_url=None)
                if verbose>=5: print('[slacki] [%s] is posted' %(query))
            postOK = True
        except Exception as e:
            if verbose>1: print(('[slacki] >ERROR: [%s]' % (str(e))))
            postOK = False
        # Return
        if return_status:
            return(postOK)

    # Post file in channel
    def post_file(self, file, query='File upload message', title=None, return_status=False, verbose=3):
        """Post file in slack message.

        Parameters
        ----------
        file : str
            Pathname to the file to be posted in slack.
        query : str
            string containing messages to be posted with the file.
        title : str
            Title of the file to be posted with the file.
        return_status : bool, default: False
            Return the status of the snoozing action.
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        status : bool

        """
        # Check internet connection
        check_connection._internet()
        try:
            self.sc.files.upload(file_=file, channels=self.channel, title=title, initial_comment=query)
            if verbose>=5: print('[slacki] File is posted')
            postOK = True
            # print(obj.successful, obj.__dict__['body']['channel']['id'])
        except Exception as e:
            if verbose>=1: print(('[slacki] >ERROR: [%s]' % (str(e))))
            postOK = False
        # Return
        if return_status:
            return(postOK)

    # Post message in channel
    def info(self, verbose=3):
        """Retrieve user information for the slack-group

        Parameters
        ----------
        verbose : int, optional
            Verbosity. The default is 3.

        Returns
        -------
        list with users.

        """
        # Check internet connection
        check_connection._internet()
        users = dict()
        try:
            # Find all users
            getusers = self.sc.users.list().body
            users['realname'] = list(map(lambda x:x['real_name'], getusers['members']))
            users['name'] = list(map(lambda x:x['name'], getusers['members']))
            for u in getusers['members']:
                # print(f'User: {u["name"]}, Real Name: {u["real_name"]}, Time Zone: {u["tz_label"]}.')
                if verbose>=3: print('User: %s, Real Name: %s, Time Zone: %s.' % (u['name'], u['real_name'], u['tz_label']))
                # print(f'Current Status: {u["profile"]["status_text"]}')
                # Get image data and show
                # Image(user['profile']['image_192'])
            users['info']=getusers
        except Exception as ex:
            if verbose>=1: print(('[slacki] >ERROR: [%s]' % (str(ex))))
        return(users)


    # %%
    def listen(self, date_from=None, date_to=None, n=None, response_time=None, verbose=3):
        if response_time is None: response_time = self.response_time
        get_posts = self.retrieve_posts(date_from=date_from, date_to=date_to, n=n, verbose=verbose)
            
        # Setup questions
        tasks=dict()
        tasks['figure']=False
        tasks['summary']=False
        tasks['status']=False
        tasks['advice']=False
        tasks['last_trade']=False
        
        # Run over all posts
        for post in get_posts:
            if post.get('client_msg_id')!=None:# and post.get('type') == 'message' and not 'subtype' in post.get('type'): # Make sure its not a bot, otherwise it starts singning.
                if '@figure' in post['text']:
                    tasks['figure']=True
                elif '@summary' in post['text']:
                    tasks['summary']=True
                elif '@status' in post['text']:
                    tasks['status']=True
                elif '@advice' in post['text']:
                    tasks['advice']=True
                elif '@last_trade' in post['text']:
                    tasks['last_trade']=True
                elif '@help' in post['text']:
                    if verbose>=3: print('[BOT] My response time is within %d seconds. I listen to: @figure, @summary, @status, @advice, @last_trade, @help' % (response_time))
                else:
                    if verbose>=3: print('[BOT] I can not do <%s>' % (post['text']))

        # Retrieve data or return
        if not np.any([*tasks.values()]):
            return
        else:
            print('Do some stuff')
            return

# %% Create channel
def make_channel(sc, channel, verbose=3):
    """Create channel."""
    try:
        sc.channels.create(channel[1:])
        if verbose>=3: print('[slacki] >Channel [%s] is succesfull created' % (channel))
    except Exception as e:
        if verbose>=3: print('[slacki] >Channel [%s] already exists.' % (channel))


# %% Post message in channel
def get_channel(channel):
    if (channel is None) or (channel=='') or (len(channel)<3): raise Exception('Channel should be a valid name; can not be None or "" or less then 3 chars.')
    if channel[0]!='#':
        channel = '#' + channel
    
    return(channel)
