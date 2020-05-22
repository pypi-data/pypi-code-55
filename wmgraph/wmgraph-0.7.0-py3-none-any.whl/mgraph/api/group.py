from .cache import memoized


class MgraphConnectorGroupMixin:
    def list_groups(self, **kwargs):
        '''https://docs.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0'''
        url = f'/groups'
        search = kwargs.get('search')
        if search is not None:
            del kwargs['search']
            url += f"?$filter=startswith(displayName,'{search}')"
        return self.get_paged(url, **kwargs)

    @memoized
    def get_group(self, group_id):
        '''returns a group'''
        return self.get(f'/groups/{group_id}')

    def list_group_members(self, group_id):
        '''returns directoryObjects'''
        return self.get_paged(f'/groups/{group_id}/members')

    def get_directoryobject(self, object_id):
        return self.get(f'/directoryObjects/{object_id}')

    def list_group_owners(self, group_id):
        return self.get_paged(f'/groups/{group_id}/owners')

    def get_group_drive(self, group_id):
        return self.get(f'/groups/{group_id}/drive')

    def get_group_drives(self, group_id):
        return self.get(f'/groups/{group_id}/drives')
