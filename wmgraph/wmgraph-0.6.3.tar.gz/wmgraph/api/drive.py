import logging
from urllib.parse import urlparse, parse_qs


class MgraphConnectorDriveMixin:
    root_item = None
    drive_id = None

    def open(self, drive_id):
        self.drive_id = drive_id

    def download(self, item_id, fd): #pylint: disable=invalid-name
        return self.get_binary(f'/drives/{self.drive_id}/items/{item_id}/content', fd=fd)

    def get_root(self):
        root = self.get(f'/drives/{self.drive_id}/root')
        self.root_item = root
        return root

    def get_driveitem(self, item_id):
        return self.get(f'/drives/{self.drive_id}/items/{item_id}')

    def __parse_deltaurl(self, url):
        url_parts = urlparse(url)
        query = parse_qs(url_parts.query)
        token = None
        if 'token' in query:
            token = query['token']
        if token:
            token = token[0]
        return token

    def __get_delta_chunk(self, drive_id, token=None):
        url = f'/drives/{drive_id}/root/delta'
        if token is not None:
            url += f"?token='{token}'"
        logging.debug(f'get_delta_chunk({url})')
        return self.get(url)

    def drive_delta_iterator(self, ignore_state=False):
        '''iterator over changes'''
        tokens_seen = {}
        state_db = self.database

        state = state_db.sync.find_one(drive_id=self.drive_id)
        logging.debug(f'State: {state}')
        if state and not ignore_state:
            token = state['token']
            logging.info(f'Resuming from {token}')
        else:
            token = None
            logging.info('New sync')

        while True:
            try:
                delta = self.__get_delta_chunk(self.drive_id, token=token) # FIXME fails on deleted drives
            except Exception as ex:
                logging.error(f"get delta exception {ex}")
                return
            # status 200 ok
            # status 410 gone:
            #   resyncChangesApplyDifferences Replace any local items with the server's version (including deletes) if you're sure that the service was up to date with your local changes when you last sync'd. Upload any local changes that the server doesn't know about.
            #   resyncChangesUploadDifferences Upload any local items that the service did not return, and upload any files that differ from the server's version (keeping both copies if you're not sure which one is more up-to-date).
            #   check Location header containing a new nextLink

            deltanext = delta.get('@odata.nextLink')
            deltalink = delta.get('@odata.deltaLink')
            value = delta.get("value", [])
            for v in value: # pylint: disable=invalid-name
                yield v

            if deltalink: # last page in a set
                token = self.__parse_deltaurl(deltalink)
                logging.debug(f'Got deltalink {token} {deltalink}')
                state_db.sync.upsert(
                    dict(drive_id=self.drive_id, deltalink=deltalink, token=token),
                    ['drive_id']
                )
                break

            if deltanext: # there are more pages
                logging.debug(f'Got deltanext {deltanext}')
                # https://graph.microsoft.com/v1.0
                # /drives/b!edsxy_Z5eEGwX_1XwPTeTMw3qRNusSdKoxH1k8HgnQ_nl7H6J8PfRLZq170BWA32
                #   /root/delta?token=...
                token = self.__parse_deltaurl(deltanext) # FIXME do not parse, use the url as it is!
                if token in tokens_seen:
                    logging.error(f'Token already seen {token}')
                    break
                tokens_seen[token] = True
            else:
                token = None
            if not token:
                break
