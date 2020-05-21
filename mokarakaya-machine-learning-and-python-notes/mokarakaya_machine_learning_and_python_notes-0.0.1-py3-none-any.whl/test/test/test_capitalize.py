from python_notes.test.source import capitalize



def test_capital_case():
    assert capitalize.capital_case('semaphore') == 'Semaphore'