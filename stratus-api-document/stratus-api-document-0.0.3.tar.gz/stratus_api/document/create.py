def create_object(collection_name, unique_keys: list, attributes: dict, hash_id=False, batch=None,
                  message_formatter=None, user_id=None, full_collection_name=False):
    from stratus_api.core.common import generate_random_id, generate_hash_id
    from stratus_api.document.utilities import generate_collection_firestore_name
    from stratus_api.document.base import create_db_client
    from stratus_api.document.get import get_objects
    from datetime import datetime
    from copy import deepcopy
    db = create_db_client()
    now = datetime.utcnow()
    attributes = deepcopy(attributes)
    if 'id' in attributes:
        other_unique_fields = [i for i in unique_keys if i != 'id']
        existing_objects = []
        if other_unique_fields:
            existing_objects += get_objects(
                collection_name=collection_name, active=False, full_collection_name=full_collection_name,
                **{"eq_{0}".format(i): attributes[i] for i in other_unique_fields}
            )
        existing_objects += get_objects(
            collection_name=collection_name, active=False, full_collection_name=full_collection_name,
            eq_id=attributes['id']
        )
        if existing_objects:
            raise ValueError("Conflict: object already exists")
        object_id = attributes['id']
    elif hash_id:
        object_id = generate_hash_id(data={i: attributes[i] for i in unique_keys})
    else:
        existing_objects = get_objects(
            collection_name=collection_name, full_collection_name=full_collection_name, active=True,
            **{"eq_{0}".format(i): attributes[i] for i in unique_keys}
        )
        if existing_objects:
            raise ValueError("Conflict: object already exists")
        object_id = generate_random_id()
    attributes['id'] = object_id
    attributes['created'] = now
    attributes['updated'] = now
    attributes['active'] = True
    collection_name = generate_collection_firestore_name(collection_name=collection_name,
                                                         full_collection_name=full_collection_name)
    doc_ref = db.collection(collection_name).document(attributes['id'])
    if batch is not None:
        batch.set(doc_ref, attributes, merge=True)
    else:
        doc_ref.set(attributes, merge=True)
    if batch is not None:
        return attributes, batch
    else:
        return attributes