# Fields to be used for statistical purposes, no content is loaded
ARTICLE_STATS_FIELDS = ['an', 'company_codes', 'company_codes_about',
                        'company_codes_occur', 'industry_codes', 'ingestion_datetime',
                        'language_code', 'modification_datetime',
                        'publication_datetime', 'publisher_name', 'region_codes',
                        'region_of_origin', 'source_code', 'source_name',
                        'subject_codes', 'title', 'word_count']

# Fields that commonly are empty, or that are deprecated
ARTICLE_DELETE_FIELDS = ['art', 'credit', 'document_type', 'publication_date', 'modification_date']
