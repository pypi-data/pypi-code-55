import pkg_resources

from . __version__ import __version__

JQUERY_MIN = 'jquery.min.js'
JQUERY = 'jquery.js'
DEST_PATH = '/static/jquery/'

def load_package(site):
    f = site.config.getbool('/', 'jquery_compressed')
    jquery = JQUERY_MIN if f else JQUERY
    src_path = 'externals/'+jquery
    
    jscontent = pkg_resources.resource_string(__name__, src_path)
    site.files.add_bytes("binary", DEST_PATH + jquery, jscontent )
    site.config.add('/', {'jquery_path': DEST_PATH+jquery})

    site.add_template_module('jquery', 'miyadaiku_theme_jquery!macros.html')
