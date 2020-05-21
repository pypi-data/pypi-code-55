import os
from tempfile import TemporaryDirectory

import aircopy.cli as cli


def test_aircopy(real_db_config):
    if real_db_config is not None:
        with TemporaryDirectory() as d:
            os.chdir(d)
            os.environ['AIRTABLE_BASE_ID'] = real_db_config['base_id']
            os.environ['AIRTABLE_API_TOKEN'] = real_db_config['api_token']
            cli.aircopy(formula="{Name} = '19st_TiO2B'")
