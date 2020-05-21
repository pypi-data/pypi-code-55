"""The tools for data operation and the wrapper for the airtable database."""
import copy
from typing import Union, List, Tuple, Generator

from airtable import Airtable

import aircopy.parser as parser
import aircopy.tools as tools
from aircopy.datatype import Record


def query(db: Airtable, uid: str, only_data: bool):
    """Query the data by the unique id from airtable.

    Parameters
    ----------
    db : Airtable
        The airtable client.

    uid : str
        The airtbale style uid.

    only_data : bool
        If True, only the value for the 'fields' in record will be returned. Otherwise, return whole record.

    Returns
    -------
    record : Record or Fields
        The dictionary of the data.
    """
    record = db.get(uid)
    if only_data:
        return record.get('fields')
    return record


def denormalize_project(project: Record, people: Airtable, institutions: Airtable, only_data: bool = False,
                        inplace: bool = False) -> Union[None, dict]:
    """Denormalize the project record from airtbale.

    Parameters
    ----------
    project : Record
        The record the project.

    people : Airtable
        The airtable client of 'People'.

    institutions : Airtable
        The airtable client of 'Institutions'.

    only_data : bool
        If True, only the value for the 'fields' in record will be returned. Otherwise, return whole record.

    inplace : bool
        If True, demoralization is done inplace. Otherwise, return the denormalized copy of the project record.

    Returns
    -------
    project : None or dict
        If inplace == False, return the denormalized record. Otherwise, denormalize inplace and return None.
    """
    if not inplace:
        project = copy.deepcopy(project)
    project = tools.get_data(project)
    if 'Collaborators' in project:
        project['Collaborators'] = [
            query(people, uid, only_data=only_data)
            for uid in project['Collaborators']
        ]
        for collaborator in project['Collaborators']:
            fields = tools.get_data(collaborator) if not only_data else collaborator
            if 'Institutions' not in fields:
                fields['Institutions'] = []
            else:
                fields['Institutions'] = [
                    query(institutions, uid, only_data=only_data)
                    for uid in fields['Institutions']
                ]
    if not inplace:
        return project
    return


def get_projecta_docs(projects: Airtable, people: Airtable, institutions: Airtable, add_info: dict,
                      **options) -> Generator:
    """Generate the projecta documents and the documents of contacts and institutions from airtbale database.

    Parameters
    ----------
    projects : Airtable
        The Projects database.

    people : Airtable
        The People database.

    institutions : Airtable
        The institutions database.

    add_info : dict
        A dictionary of the additional information.

    options : dict
        The view and filter options. Include
            max_records (``int``, optional): The maximum total number of
                records that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            page_size (``int``, optional ): The number of records returned
                in each request. Must be less than or equal to 100.
                Default is 100. See :any:`PageSizeParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Airtable formula.
                See :any:`FormulaParam`.

    Yields
    ------
    project : tuple
        The key-value pair of project document.

    people : list
        The list of the key-value pairs of the people in the collaborators list.

    institutions : list
        The list of the key-value pairs of the institutions of those collaborators.
    """
    for page in projects.get_iter(**options):
        for record in page:
            denormalize_project(record, people, institutions, inplace=True)
            _project, _people, _institutions = parser.parse_project(record, add_info)
            yield _project, _people, _institutions


class DataBase:
    """A collection of airtables at the same base."""

    def __init__(self, base_id: str, tables: List[str] = ('Projects', 'People', 'Institutions'),
                 api_token: str = None):
        """
        Initiate the class. Attributes will be added as the name of the table and its corresponding Airtable
        object.

        Parameters
        ----------
        base_id : str
            The base id for the airtables.

        tables : list
            The name of the tables.
        """
        for table in tables:
            self.__setattr__(table, Airtable(base_id, table, api_key=api_token))

    def get_projecta(self, add_info: dict, **options) -> Tuple[dict, dict, dict]:
        """Generate the projecta documents and the documents of contacts and institutions from airtbale database.

        Parameters
        ----------
        add_info : dict
            A dictionary of the additional information.

        options : kwargs
            The view and filter options. Include
                max_records (``int``, optional): The maximum total number of
                    records that will be returned. See :any:`MaxRecordsParam`
                view (``str``, optional): The name or ID of a view.
                    See :any:`ViewParam`.
                page_size (``int``, optional ): The number of records returned
                    in each request. Must be less than or equal to 100.
                    Default is 100. See :any:`PageSizeParam`.
                fields (``str``, ``list``, optional): Name of field or fields to
                    be retrieved. Default is all fields. See :any:`FieldsParam`.
                sort (``list``, optional): List of fields to sort by.
                    Default order is ascending. See :any:`SortParam`.
                formula (``str``, optional): Airtable formula.
                    See :any:`FormulaParam`.

        Returns
        -------
        project : dict
            The dictionary of project documents.

        people : dict
            The dictionary of the people in the collaborators list.

        institutions : dict
            The dictionary of the institutions of those collaborators.
        """
        gen = get_projecta_docs(
            getattr(self, 'Projects'), getattr(self, 'People'), getattr(self, 'Institutions'), add_info, **options
        )
        projects, people, institutions = dict(), dict(), dict()
        for _project, _people, _institutions in gen:
            projects.update([_project])
            people.update(_people)
            institutions.update(_institutions)
        return projects, people, institutions
