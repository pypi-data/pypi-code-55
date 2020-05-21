from collections import OrderedDict
from pathlib import Path
from typing import Union

import pytest

from aircopy.database import DataBase

DB = {
    'createdTime': '2019-03-04T15:42:21.000Z',
    'fields': {'Blogroll': ['recKm29VrzmM6eyjs'],
               'Collaborators': [{'createdTime': '2019-03-02T15:40:28.000Z',
                                  'fields': {'First Name': 'Randy',
                                             'ID': 'rnangah',
                                             'Institutions': [{'createdTime': '2019-03-04T16:00:32.000Z',
                                                               'fields': {'Address': 'Yaounde, Cameroon',
                                                                          'Collaborators 2': ['rec6VLeAUdItvIqbY'],
                                                                          'Name': 'University of Yaounde'},
                                                               'id': 'recFoBBdAy3cLxwYC'}],
                                             'Last Name': 'Nangah',
                                             'Manuscripts': ['recoZh0EL9qM0ufyD'],
                                             'Projects': ['rec6UVonazWUS1h94']},
                                  'id': 'rec6VLeAUdItvIqbY'}],
               'Grant': ['dmrefcheme16'],
               'Link to Analysis': 'http://gitlab.thebillingegroup.com/analysis/19st_sponge',
               'Link to Paper': 'http://gitlab.thebillingegroup.com/papers/19st_sponge',
               'Manuscripts': ['recoZh0EL9qM0ufyD'],
               'Name': '19st_sponge',
               'Notes': 'I am from Cameroon, currently working as a research '
                        'assistant for the Ministry of Scientific Research and '
                        'Innovation, and doing my PhD at the Department of '
                        'Inorganic Chemistry, University of Yaounde I, Yaounde, '
                        'Cameroon. ',
               'Project Lead': 'Songsheng Tao',
               'Samples': ['rec0Rnl9YH7h8aw33',
                           'recCOTctyb1eJXqG3',
                           'recAC9R3jPzuEn1gJ',
                           'recd8drZvs0yfRUCt'],
               'Start Date': '2019-03-04',
               'Status': '6 Report Sent'},
    'id': 'rec6UVonazWUS1h94'
}

PROJECT = OrderedDict(
    [
        ('begin_date', '2019-03-04'),
        ('collaborators', ['rnangah']),
        ('description', 'I am from Cameroon, currently working as a research '
                        'assistant for the Ministry of Scientific Research and '
                        'Innovation, and doing my PhD at the Department of '
                        'Inorganic Chemistry, University of Yaounde I, Yaounde, '
                        'Cameroon. '),
        ('grants', ['dmrefcheme16']),
        ('group_members', ['sstao']),
        ('lead', 'sstao'),
        ('log_url', ''),
        ('ana_repo_url',
         'http://gitlab.thebillingegroup.com/analysis/19st_sponge'),
        ('man_repo_url',
         'http://gitlab.thebillingegroup.com/papers/19st_sponge'),
        ('milestones',
         [
             OrderedDict([('audience',
                           ['pi', 'lead', 'group members', 'collaborators']),
                          ('due_date', '2019-03-11'),
                          ('name', 'Kick off meeting'),
                          ('objective', 'roll out of project to team'),
                          ('status', 'proposed')]),
             OrderedDict([('audience', ['pi', 'lead', 'group members']),
                          ('due_date', '2019-03-18'),
                          ('name', 'Project lead presentation'),
                          ('objective',
                           'lead presents background reading and initial '
                           'project plan'),
                          ('status', 'proposed')]),
             OrderedDict([('audience', ['pi', 'lead', 'group members']),
                          ('due_date', '2019-04-01'),
                          ('name', 'planning meeting'),
                          ('objective', 'develop a detailed plan with dates'),
                          ('status', 'proposed')]),
             OrderedDict([('audience',
                           ['pi', 'lead', 'group members', 'collaborators']),
                          ('due_date', '2020-03-03'),
                          ('name', 'submission'),
                          ('objective',
                           'submit the paper, release the code, whatever'),
                          ('status', 'proposed')])
         ]
         ),
        ('name', ''),
        ('pi_id', 'sbillinge'),
        ('status', '6 Report Sent')
    ]
)


@pytest.fixture
def fake_db() -> dict:
    return DB


@pytest.fixture
def example_project() -> OrderedDict:
    return PROJECT


LOCAL_TOKEN_FILE = Path(__file__).parent.joinpath('token.json')


def get_real_db_config(token_file: Path = LOCAL_TOKEN_FILE) -> Union[None, dict]:
    if token_file.exists():
        import json
        with token_file.open('r') as f:
            info = json.load(f)
        return info
    return None


@pytest.fixture
def real_db_config() -> Union[None, dict]:
    return get_real_db_config()


@pytest.fixture
def real_db() -> Union[None, DataBase]:
    db_config = get_real_db_config()
    if db_config is not None:
        return DataBase(db_config['base_id'], db_config['tables'], api_token=db_config['api_token'])
    return None
