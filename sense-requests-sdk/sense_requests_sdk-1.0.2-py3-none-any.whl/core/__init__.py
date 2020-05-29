import os

SENSE_ROOT = os.path.join(os.environ.get('HOME'), '.sense_requests')
SENSE_TMP = os.path.join(SENSE_ROOT, 'tmp')

if not os.path.exists(SENSE_ROOT):
    os.mkdir(SENSE_ROOT)

if not os.path.exists(SENSE_TMP):
    os.mkdir(SENSE_TMP)
