# Setup your slack account with a token:
# Make token as following:
#   1. https://api.slack.com/custom-integrations/legacy-tokens
#   2. Scroll down a bit untill you see 'create token'
#   3. Click on 'create token'

# %%
import slacki as slacki
print(dir(slacki))
print(slacki.__version__)

# %%
from slacki import slacki
token='xoxp-123234234235-123234234235-123234234235-adedce74748c3844747aed48499bb'

# %%
sc = slacki(channel='new_channel', token=token)

# Get some info about the users
users = sc.info()

 # Send messages
queries=['message 1','message 2']
sc.post(queries)

# Snoozing
sc.snooze(minutes=1)

# Post file
sc.post_file(file='./data/slack.png', title='Nu ook met figuren uploaden :)')

# listen (retrieve only last message)
out = sc.retrieve_posts(n=3)

# %% listen (retrieve only last message)
sc.listen()
