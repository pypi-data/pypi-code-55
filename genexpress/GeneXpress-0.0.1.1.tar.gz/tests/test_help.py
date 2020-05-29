import pytest
from ExpressionTools import helpers

gsms = ['GSM1849516',
        'GSM1849517',
        'GSM1849518',
        'GSM1849519',
        'GSM1849520',
        'GSM1849521',
        'GSM1849522',
        'GSM1849523',
        'GSM1849524',
        'GSM1849525',
        'GSM1849526',
        'GSM1849527',
        'GSM1849528',
        'GSM1849530',
        'GSM1849531',
        'GSM1849532',
        'GSM1849533',
        'GSM1849534',
        'GSM1849535']
numbers_1 = ['ID 1', 'ID 2', 'ID 3', 'ID 4', 'ID 5', 'ID 6', 'ID 7',
             'ID 8', 'ID 9', 'ID 10', 'ID 11', 'ID 12', 'ID 13', 'ID 14', 'ID 15']
numbers2 = ['44', '45', '46', '47', '48', '49', '50', '51']
numbers2_1 = ['42', '43', '44', '45', '46', '47', '48', '49']
numbers3 = ['124', '125', '126', '127', '128', '129', '130', '131']
numbers3_1 = ['142', '143', '144', '145', '146', '147', '148', '149']
numbers3_long = ['142', '143', '144', '145', '146', '147', '148', '149',
                 '150', '151', '152', '153', '154', '155', '156', '157',
                 '158', '159', '160', '161', '162', '163', '164', '165']
numbers4 = ['2124', '2125', '2126', '2127', '2128', '2129', '2130', '2131']


class TestSearchNumRange:

    def test_search_num_range_empty_or_wrong(self):
        with pytest.raises(TypeError) as e:
            helpers.search_num_range(22, 30, dict())
            helpers.search_num_range(dict(), bool(), numbers3)
        assert True if helpers.search_num_range(25, 25, numbers3) is None else False
        assert helpers.search_num_range(24, 24, numbers3_1) is None
        assert helpers.search_num_range(500, 5000, numbers3_1) is None

    def test_search_num_range_1digit(self):
        result = helpers.search_num_range(1, 5, numbers_1)
        assert result == numbers_1[:5]
        result = helpers.search_num_range(1, 12, numbers_1)
        assert result == numbers_1[:12]
        # Does not support single digit numbers only with no other text
        # result = helpers.search_num_range(1, 5, [i.split(" ")[1] for i in numbers_1])
        # assert result == [i.split(" ")[1] for i in numbers_1[:5]]
        # result = helpers.search_num_range(1, 12, [i.split(" ")[1] for i in numbers_1])
        # assert result == [i.split(" ")[1] for i in numbers_1[:12]]

    def test_search_num_range_2digits(self):
        result = helpers.search_num_range(45, 50, numbers2)
        assert result == numbers2[1:-1]
        result = helpers.search_num_range(45, 49, numbers2)
        assert result == numbers2[1:-2]
        result = helpers.search_num_range(43, 47, numbers2_1)
        assert result == numbers2_1[1:-2]
        result = helpers.search_num_range(125, 130, numbers3)
        assert result == numbers3[1:-1]
        result = helpers.search_num_range(125, 129, numbers3)
        assert result == numbers3[1:-2]
        result = helpers.search_num_range(25, 30, numbers3)
        assert result == numbers3[1:-1]
        result = helpers.search_num_range(25, 29, numbers3)
        assert result == numbers3[1:-2]
        result = helpers.search_num_range(24, 30, numbers4)
        assert result == numbers4[:-1]
        result = helpers.search_num_range(24, 29, numbers4)
        assert result == numbers4[:-2]
        result = helpers.search_num_range(26, 29, numbers4)
        assert result == numbers4[2:-2]
        # test on live data starting with 3 digit (first digit same)
        result = helpers.search_num_range(521, 530, gsms)
        assert result == gsms[5:-5]
        result = helpers.search_num_range(21, 30, gsms)
        assert result == gsms[5:-5]

    def test_search_num_range_3_plus_digits(self):
        result = helpers.search_num_range(521, 530, gsms)
        assert result == gsms[5:-5]
        result = helpers.search_num_range(1849521, 1849530, gsms)
        assert result == gsms[5:-5]


class TestSearchTerms:
    pass
    # def test_
