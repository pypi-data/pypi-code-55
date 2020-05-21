import aircopy.parser as parser


def test_parse_institution(fake_db):
    record = fake_db.get('fields').get('Collaborators')[0].get('fields').get('Institutions')[0]
    key, value = parser.parse_institution(record)
    assert key == 'uyaounde'
    assert value['name'] == 'University of Yaounde'
    assert value['aka'] == []
    assert value['city'] == 'Yaounde, Cameroon'
    assert value['state'] is None
    assert value['county'] is None


def test_parse_person(fake_db):
    record = fake_db.get('fields').get('Collaborators')[0]
    (key, value), _ = parser.parse_person(record)
    assert key == 'rnangah'
    assert value['aka'] == 'Nangah, Randy'
    assert value['institution'] == 'uyaounde'
    assert value['name'] == 'Randy Nangah'
    assert value['notes'] == []


def test_parse_project(fake_db, example_project):
    record = fake_db
    (key, value), _, _ = parser.parse_project(record, {})
    assert key == '19st_sponge'
    assert value == example_project
