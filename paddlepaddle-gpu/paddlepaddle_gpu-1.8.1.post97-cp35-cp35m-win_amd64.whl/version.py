# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '1.8.1'
major           = '1'
minor           = '8'
patch           = '1'
rc              = '0'
istaged         = False
commit          = 'ea1c05d0e61ddb1bd69b9f7fa82898a9c9859126'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
