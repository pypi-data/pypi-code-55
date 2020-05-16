__db_client__ = None


def create_db_client(refresh=False):
    """Convenience function to create a document client

    :return: document client
    """
    from stratus_api.core.settings import get_app_settings
    from google.cloud import firestore

    app_settings = get_app_settings()
    global __db_client__
    if not __db_client__ or refresh:
        __db_client__ = firestore.Client(project=app_settings['project_id'])
    return __db_client__


def define_indices(collections, app_settings):
    from stratus_api.document.utilities import generate_collection_firestore_name
    indices = list()
    for collection in collections.values():
        for index in collection.get('indices', []):
            indices.append(
                {
                    "collectionGroup": generate_collection_firestore_name(collection_name=collection['name']),
                    "queryScope": "COLLECTION",
                    "fields": [
                        dict(fieldPath=k, order=v) for k, v in index.items()
                    ]
                }
            )
    return indices


def create_compound_indices(app_settings, collections):
    import json, os
    with open('.firebaserc', 'wt') as f:
        json.dump(dict(projects=dict(default=app_settings['project_id'])), f)
    indices = define_indices(collections=collections, app_settings=app_settings)
    with open('document.indexes.json', 'wt') as f:
        json.dump({"indexes": indices}, f)
    os.system("/apps/deployment/firebase-tools-linux deploy --only document:indexes --token {0}".format(
        app_settings['firebase_token']))
    return indices
