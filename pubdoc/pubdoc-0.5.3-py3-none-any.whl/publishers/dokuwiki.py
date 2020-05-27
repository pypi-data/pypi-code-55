
from collections import namedtuple
import pathlib
import os
import dokuwiki
import sys
import logging
import ssl

document = namedtuple("Record", ['file_path', 'publish_path', 'dokuwiki_path', 'original_path'])


class DokuWikiPub:

    dokuwiki_supported_input_format_file = ['md', 'MD']

    def __init__(self, log, target, username, password, root_namespace):
        super().__init__()
        self.target = target
        self.username = username
        self.password = password
        self.root_namespace = root_namespace
        self.docs = list()
        self.log = log

    def from_dir(self, path, mask):
        self.log.info(" Loading documents from %s" % str(path))
        docs = list()
        root = pathlib.Path(path)
        for data_file in root.glob(mask):
            if data_file.is_file():

                relpath = os.path.relpath(data_file, path)
                file_path = os.path.realpath(data_file)

                # Skiop file If file extension not in suppoted format
                extension = file_path.split('.')[-1]
                if extension not in self.dokuwiki_supported_input_format_file:
                    self.log.debug(" Skip %s" % data_file)
                    continue

                self.log.info(" Loaded %s" % str(data_file))

                delimeter = '/'
                if sys.platform.startswith('win'):
                    delimeter = '\\'
                lnk = relpath.split(delimeter)
                for i in range(len(lnk[:-2])):
                    lnk[i] = lnk[i].replace('.', '_')
                original_path = ':'.join(lnk)
                lnk.insert(0, self.root_namespace)
                publish_path = ':'.join(lnk)

                
                self.docs.append(document(file_path=file_path,
                                          publish_path=publish_path,
                                          dokuwiki_path=publish_path.lower().replace(' ', '_'),
                                          original_path=original_path))
        return docs

    def publish(self):
        try:
            self.log.info("Connect to %s as %s" % (self.target, self.username))
            wiki = dokuwiki.DokuWiki(self.target, self.username, self.password)
        except (dokuwiki.DokuWikiError, Exception) as err:
            self.log.error('Unable to connect: %s' % err)
            exit(1)

        # Delete unused page
        self._delete_unused_pages(wiki)

        # Send pages on dokuwiki
        for doc in self.docs:
            with open(doc.file_path, 'r', encoding='utf-8') as fread:
                data = fread.read()
                wiki.pages.set(doc.publish_path, data)

    def _delete_unused_pages(self, wiki):
        unused_pages = self._get_unused_pages(wiki)
        self.log.debug("Unused pages - %s" % str(unused_pages))
        if unused_pages:
            for page in unused_pages:
                wiki.pages.set(page, "")

    def _get_unused_pages(self, wiki):
        pages = wiki.pages.list(self.root_namespace)
        self.log.debug("Pages - %s" % str(self.docs))
        unused_pages = list()
        if pages:
            pages_for_publish = list(map(lambda x : x.dokuwiki_path, self.docs))
            for page in pages:
                if page['id'] not in pages_for_publish:
                    unused_pages.append(page['id'])   
        return unused_pages