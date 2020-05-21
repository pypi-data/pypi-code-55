"""Parsers that parse the information queried from airtable to a pyhton dictionary following Billinge group
database standard."""
import uuid
from typing import List, Any, Tuple

import aircopy.tools as tools
from aircopy.datatype import Record, Pair

DEFAULT = {
    'pi_id': 'sbillinge',
    'name': '',
    'log_url': ''
}


def _retrieve(add_info: dict, key: str) -> Any:
    """Retrieve information from the dictionary. If not found, use the value in DEFAULT.

    Parameters
    ----------
    add_info : dict
        The addition information provided by the user.

    key : str
        The key to search inside the addition information.

    Returns
    -------
    value : Any
        The value from the add_info or DEFAULT or it is None.
    """
    return add_info.get(key, DEFAULT.get(key))


def parse_project(record: Record, add_info: dict) -> Tuple[Pair, List[Pair], List[Pair]]:
    """Parse the project record in airtable to Billinge group format.

    Return a key-value pair of the project and a list of key-value pairs of the people doc and institution doc
    in the project. The record should be denormalized at first.

    Parameters
    ----------
    record : Record
        The record from the airtable.

    add_info : dict
        A dictionary of the additional information.

    Returns
    -------
    project : tuple
        The key-value pair of project document.

    people : list
        The list of the key-value pairs of the people in the collaborators list.

    institutions : list
        The list of the key-value pairs of the institutions of those collaborators.
    """
    record = tools.get_data(record)
    pairs = list(map(parse_person, record.get('Collaborators', [])))
    people = [pair[0] for pair in pairs if pair[0] is not None]
    institutions = [pair[1] for pair in pairs if pair[1] is not None]
    key = record.get('Name')
    value = {
        'begin_date': record.get('Start Date'),
        'collaborators': tools.get_keys(people),
        'description': record.get('Notes'),
        'grants': record.get('Grant'),
        'group_members': [tools.gen_person_id(record.get('Project Lead'))],
        'lead': tools.gen_person_id(record.get('Project Lead')),
        'log_url': _retrieve(add_info, 'log_url'),
        'ana_repo_url': record.get('Link to Analysis'),
        'man_repo_url': record.get('Link to Paper'),
        'milestones': tools.auto_gen_milestons(record.get('Start Date')),
        'name': _retrieve(add_info, 'name'),
        'pi_id': _retrieve(add_info, 'pi_id'),
        'status': record.get('Status')
    }
    project = (key, value)
    return project, people, institutions


def parse_person(record: Record) -> Tuple[Pair, Pair]:
    """Parse the person information in the People airtable to the contact and institution document.

    Parameters
    ----------
    record : Record
        The record from the airtable.

    Returns
    -------
    contact : tuple
        The key-value pair of the contact document.

    institution : tuple
        The key-value pair of the institution document.
    """
    record = tools.get_data(record)
    institutions = list(map(parse_institution, record.get('Institutions', [])))
    institution = institutions[0] if institutions else None
    key = record.get('ID')
    value = {
        'name': '{} {}'.format(
            record.get('First Name'),
            record.get('Last Name')
        ),
        'aka': '{}, {}'.format(
            record.get('Last Name'),
            record.get('First Name')
        ),
        'institution': institution[0] if institution else None,
        'notes': [],
        'uuid': str(uuid.uuid4())
    }
    tools.tag_date(value)
    contact = (key, value)
    return contact, institution


def parse_institution(record: Record) -> Tuple[str, dict]:
    """Parse the record from the Institutions airtbale to the institution documents.

    Parameters
    ----------
    record : Record
        The record from the airtable.

    Returns
    -------
    institution : tuple
        The key-value pair of the institution document.
    """
    record = tools.get_data(record)
    key = tools.gen_inst_id(record.get('Name', ''), mode='auto')
    value = {
        'aka': [],
        'city': record.get('Address'),
        'state': record.get('State'),
        'county': record.get('County'),
        'name': record.get('Name')
    }
    tools.tag_date(value)
    institution = (key, value)
    return institution
