# flake8: NOQA
from .base import *  # NOQA


DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


"""
不加HOST和PORT，虽然可以访问数据库，但会导致页面刷新变慢
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


if DEBUG:
    # django2.0 debug toolbar
    MIDDLEWARE +=[
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'silk.middleware.SilkyMiddleware',
    ]
    INSTALLED_APPS += [
        'debug_toolbar',
        'silk',
    ]

    INTERNAL_IPS = ['127.0.0.1']
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',

    ]
    DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
    # 或把jquery下载到本地然后取消下面这句的注释, 并把上面那句删除或注释掉
    #'JQUERY_URL': '/static/jquery/2.1.4/jquery.min.js',
    'SHOW_COLLAPSED': True,
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }

