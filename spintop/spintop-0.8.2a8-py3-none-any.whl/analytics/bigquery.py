

from spintop.services.target_bigquery import emit_state, persist_lines_job
from spintop.utils import repr_obj, utcnow_aware

from .base import AbstractSingerTarget, SingerMessagesFactory


class BigQuerySingerTarget(AbstractSingerTarget):
    add_null_to_fields = False

    def __init__(self, project_id, dataset_id, validate_records=True):
        super().__init__()
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.validate_records = validate_records

    def send_messages(self, messages_str):
        state = persist_lines_job(self.project_id, self.dataset_id, messages_str, truncate=False, validate_records=self.validate_records)
        emit_state(state)

    def __repr__(self):
        return repr_obj(self, ['project_id', 'dataset_id'])
