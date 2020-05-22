from .cache import memoized


class MgraphConnectorUserMixin:

    def list_users(self, **kwargs):
        '''
        iterator over all graph users.
        '''
        return self.get_paged(f'/users', **kwargs)

    @memoized
    def get_user(self, user_id):
        '''
        iterator over all graph users.
        '''
        # return [self.get(f'/users/f05885f7-1690-4ac3-99c1-1f69d874bc3c')]
        return self.get(f'/users/{user_id}')

    def get_user_licensedetails(self, user_id):
        return self.get(f'/users/{user_id}/licenseDetails')['value']

    def get_user_member_groups(self, user_id):
        return self.post_paged(f'/users/{user_id}/getMemberGroups',
                               data={'securityEnabledOnly': False})

    def delete_user(self, user_id):
        return self.delete(f'/users/{user_id}')
