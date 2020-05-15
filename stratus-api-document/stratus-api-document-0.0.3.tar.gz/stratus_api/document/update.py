def format_update_message(attributes):
    update = dict()
    for k, v in attributes.items():
        if isinstance(v, dict):
            for key, value in format_update_message(v).items():
                update['{0}.{1}'.format(k, key)] = value
        else:
            update[k] = v
    return update


def update_object(collection_name: str, object_id, attributes: dict, batch=None, message_formatter=None,
                  user_id=None, upsert=False, override=False, overwrite_updated=False, full_collection_name=False):
    from stratus_api.document.base import create_db_client
    from stratus_api.document.utilities import generate_collection_firestore_name
    from datetime import datetime
    from copy import deepcopy
    collection_name = generate_collection_firestore_name(collection_name=collection_name,
                                                         full_collection_name=full_collection_name)
    db = create_db_client()
    doc_ref = db.collection(collection_name).document(object_id)
    now = datetime.utcnow()
    attributes = deepcopy(attributes)
    if not overwrite_updated:
        attributes['updated'] = now

    if not override:
        attributes = format_update_message(attributes=attributes)

    if batch is not None:
        if upsert:
            batch.set(doc_ref, attributes, merge=True)
        else:
            batch.update(doc_ref, attributes)
    else:
        if upsert:
            doc_ref.set(attributes, merge=True)
        else:
            doc_ref.update(attributes)
    if not batch:
        attributes = doc_ref.get().to_dict()
    else:
        return attributes, batch
    return attributes


def delete_object(collection_name, object_id, batch=None, user_id=None, full_collection_name=False):
    attributes = dict(id=object_id, active=False)
    results = update_object(collection_name=collection_name, object_id=object_id, attributes=attributes, batch=batch,
                            full_collection_name=full_collection_name)
    return results