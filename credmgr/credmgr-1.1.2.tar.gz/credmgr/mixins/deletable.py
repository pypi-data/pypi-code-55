class DeletableMixin:
    '''Interface for classes that can be edited and deleted.'''

    def delete(self):
        '''Delete the object.

        Example usage:

        .. code:: python

            bot = credmgr.bot(name='name')
            bot.delete()

        '''
        self._credmgr.delete(f'{self._path}/{self.id}')
        del self