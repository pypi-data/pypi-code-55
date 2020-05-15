def generate_collection_firestore_name(collection_name, prefix='', full_collection_name=False):
    from stratus_api.core.settings import get_app_settings
    app_settings = get_app_settings()
    if full_collection_name:
        return collection_name
    return "{0}-{1}-{2}{3}".format(app_settings['service_name'], app_settings['environment'], prefix, collection_name)


def manage_retries(partial_function, handled_exceptions, propagate_exceptions, retries, backoff=True):
    from logging import getLogger
    logger = getLogger()
    from time import sleep
    success = False
    attempts = 0
    results = None
    delay = 1
    while attempts < retries and not success:
        try:
            results = partial_function()
        except handled_exceptions as e:
            attempts += 1
            if retries == attempts and propagate_exceptions:
                raise e
            else:
                logger.warning(e)
                if backoff:
                    sleep(delay)
                    delay *= 2
        else:
            success = True
    return results
