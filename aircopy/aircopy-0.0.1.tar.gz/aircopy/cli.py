"""The cli interface."""
import os
from typing import Union, List

import fire

import aircopy.io as io
from aircopy.database import DataBase


def aircopy(add_info: dict = None, max_records: int = None, view: int = None, page_size: int = None,
            fields: Union[str, List[str]] = None, sort: List[str] = None, formula: str = None):
    """Transfer the data from Airtbale to Billinge group projecta database.

    It will read the variables 'AIRTABLE_BASE_ID' and 'AIRTABLE_API_TOKEN' inside your environment and connect
    to your airtable database, download the content and parse it into Billinge group database documents and
    write it out to yaml files. The yaml files will be named as "airtable_projecta.yaml", "airtable_contacts.yaml"
    and "airtable_institutions.yaml".

    To use the it, you need to find the base id of your Airtable by visiting the airtable api website (
    https://airtable.com/api) and generate the api token following the instructions on the website (
    https://support.airtable.com/hc/en-us/articles/219046777-How-do-I-get-my-API-key-). Then, export the base id
    and api token to the environment variables.

    $ export AIRTABLE_BASE_ID=***

    $ export AIRTABLE_API_TOKEN=***

    Or you can add these lines in your ~/.bashrc so that you don't need to repeat doing it. Then you can run the
    aircopy.

    $ aircopy

    Aircopy supports the data query options provided by the airtable. For example, if you would like to transfer
    the project with project lead "Songsheng Tao", then you need to add the formula.

    $ aircopy --formula "{Project Lead} = 'Songsheng Tao'"

    For more information, please read the https://airtable.com/api to see how to use the flags.

    Also, you can specify what additional information you would like to include in the projecta docs by passing
    a dictionary to the 'add_info' flag. The keys should be inside the Billinge group projecta schemas. For
    example, you would like your pi_id to be someone else like 'sstao' (default 'sbillinge'), you can use

    $ aircopy --add_info {pi_id:sstao}

    Parameters
    ----------
    add_info : dict
        Additional information for the projecta. The keys must be in the Billinge group
        projecta database schemas.

    max_records : int
        The maximum total number of records that will be returned.

    view : str
        The name or ID of a view.

    page_size : int
        The number of records returned in each request. Must be less than or equal to 100. Default is 100.

    fields : str or list
        Name of field or fields to be retrieved. Default is all fields.

    sort : list
        List of fields to sort by. Default order is ascending.

    formula : str
        Airtable formula.
    """
    if add_info is None:
        add_info = dict()
    options = dict()
    if max_records is not None:
        options.update({'add_info': max_records})
    if view is not None:
        options.update({'view': view})
    if page_size is not None:
        options.update({'page_size': page_size})
    if fields is not None:
        options.update({'fields': fields})
    if sort is not None:
        options.update({'sort': sort})
    if formula is not None:
        options.update({'formula': formula})
    base_id = os.getenv('AIRTABLE_BASE_ID')
    if base_id is None:
        raise EnvironmentError(
            "AIRTABLE_BASE_ID not found in environment. "
            "Please add the environment variable AIRTABLE_BASE_ID"
        )
    api_token = os.getenv('AIRTABLE_API_TOKEN')
    if api_token is None:
        raise EnvironmentError(
            "AIRTABLE_API_TOKEN not found in environment. "
            "Please add the environment variable AIRTABLE_API_TOKEN"
        )
    db = DataBase(base_id, api_token=api_token)
    projects, people, institutions = db.get_projecta(add_info, **options)
    io.write_docs_to_yaml('airtable_projects.yaml', projects)
    io.write_docs_to_yaml('airtable_people.yaml', people)
    io.write_docs_to_yaml('airtable_institutions.yaml', institutions)
    return


def main():
    """Fire aircopy."""
    fire.Fire(aircopy)
