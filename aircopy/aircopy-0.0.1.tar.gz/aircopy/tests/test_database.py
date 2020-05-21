import aircopy.database as database


def test_denormalize_project(real_db):
    if real_db is None:
        return
    record = real_db.Projects.get('rec6UVonazWUS1h94')
    people = getattr(real_db, 'People')
    institutions = getattr(real_db, 'Institutions')
    assert database.denormalize_project(record, people, institutions, inplace=False)
    assert database.denormalize_project(record, people, institutions, inplace=False, only_data=True)


def test_get_projecta(real_db):
    if real_db is None:
        return
    assert real_db.get_projecta({}, formula="{Name} = '19st_TiO2B'")
