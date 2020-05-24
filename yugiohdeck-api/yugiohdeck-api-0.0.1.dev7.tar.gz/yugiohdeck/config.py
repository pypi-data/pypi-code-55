SETTINGS = {
    'baseURL': 'https://yugiohdeck.github.io',
    'verbose': False,
}
def DEBUG(s):
    if SETTINGS['verbose']:
        print('[yugiohdeck.github.io API debug] '+str(s))