import pandas as pd

from seeq.sdk import *

from .. import _login


def get_users():
    users_api = UsersApi(_login.client)

def get_acl(item):
    item_id = None
    if isinstance(item, str):
        item_id = item

    items_api = ItemsApi(_login.client)
    acl_output = items_api.get_access_control(id=item_id)  # type: AclOutputV1

    aces = list()
    for ace_output in acl_output.entries:  # type: AceOutputV1
        permissions = ace_output.permissions  # type: PermissionsV1
        aces.append({
            'ID': ace_output.id,
            'Identity ID': ace_output.identity.id,
            'Identity Name': ace_output.identity.name,
            'Identity Type': ace_output.identity.type,
            'Role': ace_output.role,
            'Read': permissions.read,
            'Write': permissions.write,
            'Manage': permissions.manage,
            'Origin ID': ace_output.origin.id,
            'Origin Name': ace_output.origin.name,
            'Origin Type': ace_output.origin.type
        })

    return pd.DataFrame(aces, columns=[
        'ID',
        'Identity ID',
        'Identity Name',
        'Identity Type',
        'Role',
        'Read',
        'Write',
        'Manage',
        'Origin ID',
        'Origin Name',
        'Origin Type'
    ])
