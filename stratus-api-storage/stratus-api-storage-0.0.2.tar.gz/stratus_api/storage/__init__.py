from os.path import isdir

STORAGE_UPLOAD_FOLDER = '/apps' if isdir('/apps') else 'tests/mocks'
