class FbConstants:

    GRAPH_API_BASE_URL = 'https://graph.facebook.com'

    WABAS_EDGE = 'whatsapp_business_accounts'

    # validate the fields to get (such as status and message throughput)
    WABAS_FIELDS = [
        'verified_name',
        'status',
        'quality_rating',
        'id',
        'display_phone_number'
    ]

    PHONE_NUMBERS_EDGE = 'phone_numbers'
