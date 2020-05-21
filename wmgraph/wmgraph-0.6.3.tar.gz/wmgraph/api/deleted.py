class MgraphConnectorDeletedMixin:
    def list_deleted_users(self, **kwargs):
        '''
        iterator over all deleted graph users.
        '''
        return self.get_paged(f'/directory/deletedItems/microsoft.graph.user', **kwargs)

    def list_deleted_groups(self, **kwargs):
        '''
        iterator over all deleted graph groups.
        '''
        return self.get_paged(f'/directory/deletedItems/microsoft.graph.group', **kwargs)

    def list_deleted_applications(self, **kwargs):
        '''
        iterator over all deleted graph applications.
        '''
        return self.get_paged(f'/directory/deletedItems/microsoft.graph.application', **kwargs)

    def get_deleted_item(self, object_id):
        '''
        get a deleted item by object_id
        '''
        return self.get(f'/directory/deletedItems/{object_id}')
