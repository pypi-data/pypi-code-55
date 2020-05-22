class MgraphConnectorUserContactMixin:
    def mk_url(self, uid=None, folder=None):
        url = '/contacts'
        if uid is not None:
            url = f'/users/{uid}/contacts'
        if folder is not None:
            url = f'/users/{uid}/contactFolders/{folder}/contacts'
        return url

    def get_contact(self, uid=None, folder=None, contact_id=None):
        url = self.mk_url(uid, folder)
        url += f'/{contact_id}'
        return self.get(url)

    def list_contacts(self, uid=None, folder=None):
        url = self.mk_url(uid, folder)
        return self.get(url)

    def create_contact(self, uid=None, folder=None, data=None):
        url = self.mk_url(uid, folder)
        return self.post(url, data)

    def update_contact(self, uid=None, cid=None, data=None):
        url = f'/users/{uid}/contacts/{cid}'
        return self.patch(url, data)
