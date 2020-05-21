import aircopy.autogen as autogen


def test_auto_gen_milestons():
    milestones = autogen.auto_gen_milestons('2020-01-01')
    assert milestones[0]['due_date'] == '2020-01-08'
    assert milestones[1]['due_date'] == '2020-01-15'
    assert milestones[2]['due_date'] == '2020-01-29'


def test_auto_gen_deliverable():
    dilverable = autogen.auto_gen_deliverable('2020-01-01')
    assert dilverable['due_date'] == '2020-12-31'
