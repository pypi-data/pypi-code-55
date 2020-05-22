import logging

from .deltaiterator import GenericDeltaIterator


class MgraphConnectorDriveMixin:
    root_item = None
    drive_id = None

    def open(self, drive_id):
        self.drive_id = drive_id

    def download(self, item_id, fd):  # pylint: disable=invalid-name
        return self.get_binary(f'/drives/{self.drive_id}/items/{item_id}/content', fd=fd)

    def get_root(self):
        root = self.get(f'/drives/{self.drive_id}/root')
        self.root_item = root
        return root

    def get_driveitem(self, item_id):
        return self.get(f'/drives/{self.drive_id}/items/{item_id}')

    def drive_delta_iterator(self, state_db=None, ignore_state=None):
        '''iterator over changes'''
        state = None
        if state_db:
            state = state_db.sync.find_one(drive_id=self.drive_id)
            logging.debug(f'State: {state}')
        if state and not ignore_state:
            deltalink = state['deltalink']
            logging.info(f'Resuming from {deltalink}')
        else:
            deltalink = None
            logging.info('New sync')

        url = f'/drives/{self.drive_id}/root/delta'
        iterator = GenericDeltaIterator(self, url, deltalink=deltalink)
        for delta in iterator:
            yield delta

        deltalink = iterator.get_next_url()
        if deltalink and state_db:  # last page in a set
            logging.debug(f'Got deltalink {deltalink}')
            state_db.sync.upsert(
                dict(drive_id=self.drive_id, deltalink=deltalink),
                ['drive_id']
            )
