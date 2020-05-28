import requests
from requests.auth import HTTPBasicAuth


def get_cdo_id(pyelq_bulk_connection, cdo_name):
    """
    When you only know the external name of the Eloqua CDO, you can get the CDO ID# using this.
    :param pyelq_bulk_connection: pyeloqua Bulk object
    :param cdo_name: str - CDO name
    :return: the id of the CDO
    """
    bulk_exp = pyelq_bulk_connection
    return bulk_exp.GetCdoId(cdo_name)


def get_field_names(pyelq_bulk_connection, elq_object, obj_id=None, act_type=None):
    """
    Returns all the external and internal reference field names for a given Eloqua CDO.
    Structured as {external: internal}.
    :param pyelq_bulk_connection: pyeloqua Bulk object
    :param elq_object: str - typically 'customobjects'
    :param obj_id: int - the id of the object
    :param act_type: str - (usually optional)
    :return type: list
    """
    bulk_exp = pyelq_bulk_connection
    field_dicts = bulk_exp.get_fields(elq_object=elq_object, obj_id=obj_id, act_type=act_type)
    return {field['name']: field.get('internalName') for field in field_dicts}


def get_asset_ids(pyelq_bulk_connection, asset_type, asset_name=''):
    """
    get ids that match a string (name of asset) for any of these assets: lists, segments, filters
    if unsure, just give something you know is in the name
    spaces seem to break the search if not exact match?

    example:
    r = get_asset_ids(
         elq_conn,
         asset_type='filters',
         asset_name='MANAGEMENT_Segmentations_')

    :param pyelq_bulk_connection: pyeloqua Bulk object
    :param asset_type: 'lists', 'segments', or 'filters'
    :param asset_name: str - get names that have this string value in it
    :return: all name of asset_type that have asset_name in them
    """

    query = 'contacts/{asset}?q=name=*'.format(asset=asset_type)
    r = requests.get(
        url=''.join([pyelq_bulk_connection.bulkBase, query, asset_name, '*'*bool(asset_name)]),
        auth=HTTPBasicAuth(*pyelq_bulk_connection.auth))
    r = r.json()['items']
    return {filterdict['name']: filterdict['uri'][filterdict['uri'].rfind('/')+1:] for filterdict in r}
