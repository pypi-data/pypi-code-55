import aircopy.tools as tools


def test_gen_person_id():
    assert tools.gen_person_id('Hahaha LaLaLa') == 'hlalala'
    assert tools.gen_person_id('Songsheng Tao') == 'sstao'


def test_auto_gen_milestons():
    milestones = tools.auto_gen_milestons('2020-01-01')
    assert milestones[0]['due_date'] == '2020-01-08'
    assert milestones[1]['due_date'] == '2020-01-15'
    assert milestones[2]['due_date'] == '2020-01-29'
    assert milestones[3]['due_date'] == '2020-12-31'


def test_tag_date():
    record = dict()
    tools.tag_date(record)
    assert set(record.keys()) == {'day', 'month', 'year', 'updated'}


def test_get_keys():
    assert tools.get_keys([('k', 'v'), ('k', 'v')]) == ['k', 'k']
    assert tools.get_keys([]) == []


def test_gen_inst_id():
    assert tools.gen_inst_id('University of Hahaha', 'auto') == 'uhahaha'
    assert tools.gen_inst_id('Department of Hahaha, University of Hahaha', 'auto') == 'hahaha,universityofhahaha'
    assert tools.gen_inst_id('School of Hahaha, University of Hahaha', 'auto') == 'hahaha,universityofhahaha'


def test_get_data(fake_db):
    assert isinstance(tools.get_data(fake_db), dict)
