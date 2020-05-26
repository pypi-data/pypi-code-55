def rename_id_field(objs):
    """
    rename_id_field rename field "_id" to "id"

    :param objs: dict with filed
    :return: new objs
    """
    new_objs = []
    for i, c in enumerate(objs):
        new_objs.append({('id' if k == '_id' else k): v for k, v in c.items()})
    return new_objs


def filter_meta_fields(objs):
    """
    filter_meta_fields filters dict from internal fields (this one has _ preffix)

    :param objs: dict with filed
    :return: new objs
    """
    new_objs = []
    for c in objs:
        new_c = {}
        for k, v in c.items():
            if k[0] == '_':
                continue
            new_c[k] = v
        new_objs.append(new_c)
    return new_objs
