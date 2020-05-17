from credmgr.models.utils import camelToSnake


class EditableMixin:
    _editableAttrs = []

    def edit(self, **kwargs):
        payload = []

        for attr in self._editableAttrs:
            if attr in kwargs:
                payload.append({'op': 'replace', 'path': f'/{camelToSnake(attr)}', 'value': kwargs[attr]})
        self.__dict__.update(self._credmgr.patch(f'{self._path}/{self.id}', data=payload).__dict__)
        return self