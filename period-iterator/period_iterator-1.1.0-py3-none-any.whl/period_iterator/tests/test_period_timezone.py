from ..period_timezone import period_timezone

class test_period_timezone():
    def test_period_timezone_format_2_positive_digits(self):
        tzfmt = period_timezone()
        assert tzfmt.format('+07') == '+07:00'

    def test_period_timezone_format_2_negative_digits(self):
        tzfmt = period_timezone()
        assert tzfmt.format('-07') == '-07:00'

    def test_period_timezone_format_default(self):
        tzfmt = period_timezone()
        assert tzfmt.format('-07aa') == '-07aa'