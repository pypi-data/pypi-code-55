# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '2.0.0-alpha0'
major           = '2'
minor           = '0'
patch           = '0-alpha0'
rc              = '0'
istaged         = True
commit          = '32f07216e0ddf551a0e0be5ca5dcbd5fe26a8706'
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
