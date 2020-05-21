import aircopy.tools as tools


def test_gen_person_id():
    assert tools.gen_person_id('Hahaha LaLaLa') == 'hlalala'
    assert tools.gen_person_id('Songsheng Tao') == 'sstao'


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
