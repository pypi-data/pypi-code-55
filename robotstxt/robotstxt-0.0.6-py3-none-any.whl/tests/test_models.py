from robotstxt import RobotsFile
test_robots = '''
# some more comments
some uncommented comments

user-agent: bingbot
user-agent: googlebot
Allow: /same_length_allow_beats_disallow
Disallow: /same_length_allow_beats_disallow
Allow: /longer_allow_beats_disallow*
Disallow: /longer_allow_beats_disallow
Disallow: /something # inline comment
Disallow: missing_leading_slash
Disallow: *leading_wildcard
Disallow: /multiple*wildcards*test
Disallow: *unencoded|
Disallow: *encoded%40 # @ symbol

user-agent: googlebot
Disallow: /split_block_test

user-agent: googlebot-images
Disallow: /negative_fallback_test

user-agent: *
Disallow: /default_token


Sitemap: https://www.domain.com/sitemap.xml
sitemap: https://www.domain.com/lower_case.xml
SITEMAP: https://www.domain.com/upper_case.xml
sitemap: www.domain.com/missing_protocol.xml
sitemap: missing_domain.xml
sitemap: https://www.domain.com/has_comment.xml #comment
  Sitemap: https://www.domain.com/leading_whitespace.xml
Sitemap: https://www.domain.com/trailing_whitespace.xml   
Sitemap:    https://www.domain.com/rule_leading_whitespace.xml   

'''


def test_RobotsFile():
    robots = RobotsFile(test_robots)
    robots_size_exceeded = RobotsFile('x' * 900000)

    #assert robots.byte_size == 652 #todo uncomment this when tests finalized
    assert robots.size_exceeded == False
    assert robots_size_exceeded.size_exceeded == True

    assert robots.sitemaps[0].url == 'https://www.domain.com/sitemap.xml'
    assert robots.sitemaps[1].url == 'https://www.domain.com/lower_case.xml'
    assert robots.sitemaps[2].url == 'https://www.domain.com/upper_case.xml'
    assert robots.sitemaps[3].url == 'www.domain.com/missing_protocol.xml'
    assert robots.sitemaps[4].url == 'missing_domain.xml'
    assert robots.sitemaps[5].url == 'https://www.domain.com/has_comment.xml'
    assert robots.sitemaps[6].url == 'https://www.domain.com/leading_whitespace.xml'
    assert robots.sitemaps[7].url == 'https://www.domain.com/trailing_whitespace.xml'
    assert robots.sitemaps[8].url == 'https://www.domain.com/rule_leading_whitespace.xml'

    assert robots.sitemaps[0].valid_url == True
    assert robots.sitemaps[3].valid_url == False
    assert robots.sitemaps[4].valid_url == False

    assert robots.test_url('https://www.example.com/something', 'googlebot')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/something', 'GOOGLEBOT')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/split_block_test', 'googlebot')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/something?url_query_test', 'googlebot')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/missing_leading_slash', 'googlebot')['results'] == 'allowed'
    assert robots.test_url('https://www.example.com/default_token', 'some_token')['results'] == 'disallowed'

    assert robots.test_url('https://www.example.com/something', 'googlebot-news')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/negative_fallback_test', 'googlebot-images')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/something', 'googlebot-images')['results'] == 'allowed'
    assert robots.test_url('https://www.example.com/something/leading_wildcard', 'googlebot')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/something/default_trailing_wildcard', 'googlebot')['results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/same_length_allow_beats_disallow', 'googlebot')['results'] == 'allowed'
    assert robots.test_url('https://www.example.com/longer_allow_beats_disallow', 'googlebot')['results'] == 'allowed'
    assert robots.test_url('https://www.example.com/multiple__wildcards__test__', 'googlebot')['results'] == 'disallowed'

    assert robots.test_url('https://www.example.com/encoded%40', 'googlebot')[
               'results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/encoded@', 'googlebot')[
               'results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/unencoded|', 'googlebot')[
               'results'] == 'disallowed'
    assert robots.test_url('https://www.example.com/unencoded%7C', 'googlebot')[
               'results'] == 'disallowed'


def test_Sitemap():
    sitemap_result = Sitemap('https://www.example.com/sitemap.xml')
    assert sitemap_result.valid_url == True
    assert sitemap_result.url == 'https://www.example.com/sitemap.xml'

    sitemap_result = Sitemap('ttps://www.example.com/sitemap.xml')
    assert sitemap_result.valid_url == False

print('something')