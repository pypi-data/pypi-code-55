# -*- coding: utf-8 -*-
from ${appname}.${modular}.common import *
def inter(id='',title=""):
    data={
        'title':title,
        'id':id
    }
    return successjson(data)