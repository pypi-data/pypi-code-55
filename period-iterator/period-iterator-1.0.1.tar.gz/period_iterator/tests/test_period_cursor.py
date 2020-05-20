from ..period_cursor import period_cursor

class test_period_cursor():
    def test_period_begin_end(self):
        cursor = period_cursor('2020-03-04T12:34:56+07:00', 'Asia/Bangkok')
        assert cursor.begin() == '2020-03-04T00:00:00+07:00'
        assert cursor.end() == '2020-03-04T23:59:59+07:00'

    def test_cursor_equal_comparison_ignore_time(self):
        cursor1 = period_cursor('2020-03-04T12:34:56+07:00', 'Asia/Bangkok')
        cursor2 = period_cursor('2020-03-04T13:34:56+07:00', 'Asia/Bangkok')
        assert cursor1 == cursor2

    def test_cursor_greater_or_equal_comparison_ignore_time(self):
        cursor1 = period_cursor('2020-03-04T12:34:56+07:00', 'Asia/Bangkok')
        cursor2 = period_cursor('2020-03-05T13:34:56+07:00', 'Asia/Bangkok')
        assert cursor2 >= cursor1
        assert not (cursor1 >= cursor2)

    def test_tomorrow(self):
        cursor = period_cursor('2020-03-04T12:34:56+07:00', 'Asia/Bangkok')
        tomorrow_cursor = period_cursor('2020-03-05T12:34:56+07:00', 'Asia/Bangkok')
        assert cursor.tomorrow() == tomorrow_cursor