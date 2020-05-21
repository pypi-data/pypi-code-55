

class ServiceMappingTelecomCompanies():
    TELECOM_COMPANIES = {
        'Jazztel': 'Jazztel',
        'MasMovil': 'MasMovil',
        'Movistar': 'Movistar',
        'Aire / Nubip': 'Nubip',
        'Orange': 'Orange',
        'Parlem': 'Parlem',
        'PepePhone': 'PepePhone',
        'Vodafone': 'Vodafone',
        'Yoigo': 'Yoigo'
    }

    @classmethod
    def telecom_company(cls, company):
        return cls.TELECOM_COMPANIES.get(company, 'Other')
