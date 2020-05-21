from .dataset_upload import DatasetUpload


class DatasetInstance():
    '''

    '''

    def __init__(self, client, datasetInstanceId=None, status=None, datasetId=None, size=None, createdAt=None):
        self.client = client
        self.id = datasetInstanceId
        self.dataset_instance_id = datasetInstanceId
        self.status = status
        self.dataset_id = datasetId
        self.size = size
        self.created_at = createdAt

    def __repr__(self):
        return f"DatasetInstance(dataset_instance_id={repr(self.dataset_instance_id)}, status={repr(self.status)}, dataset_id={repr(self.dataset_id)}, size={repr(self.size)}, created_at={repr(self.created_at)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'dataset_instance_id': self.dataset_instance_id, 'status': self.status, 'dataset_id': self.dataset_id, 'size': self.size, 'created_at': self.created_at}
