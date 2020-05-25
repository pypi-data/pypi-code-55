from robotstxt import is_valid_url, get_url_path

def test_is_valid_url():
    assert is_valid_url('https://www.example.com')
    assert is_valid_url('www.example.com') == None

def test_get_url_path():
    assert get_url_path('https://www.example.com/') == '/'
    assert get_url_path('https://www.example.com/a_path?params=123') == '/a_path?params=123'
