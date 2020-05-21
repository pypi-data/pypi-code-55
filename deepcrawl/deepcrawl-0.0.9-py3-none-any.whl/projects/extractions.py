from deepcrawl.utils import ImmutableAttributesMixin

extraction_mutable_fields = (
    'label',
    'regex',
    'match_number_from',
    'match_number_to',
    'filter',
    'clean_html_tags'
)


class DeepCrawlExtraction(ImmutableAttributesMixin):
    __slots__ = extraction_mutable_fields

    mutable_attributes = extraction_mutable_fields

    def __init__(self, extraction_data):
        self.label = extraction_data.get('label')
        self.regex = extraction_data.get('regex')
        self.match_number_from = extraction_data.get('match_number_from')
        self.match_number_to = extraction_data.get('match_number_to')
        self.filter = extraction_data.get('filter', '')
        self.clean_html_tags = extraction_data.get('clean_html_tags', False)

        super(DeepCrawlExtraction, self).__init__()
