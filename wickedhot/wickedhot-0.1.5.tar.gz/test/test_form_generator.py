from wickedhot.form_generator import encoder_package_to_html_page


def test_form_generation():

    stats = {'weight': {'median': 160.5, 'min': 55.0, 'max': 564.2},
             'height': {'median': 6.0,  'min': 4.5, 'max': 7.5}}

    # can also try with stats = None
    # stats = None

    packaged = {'max_levels_default': 10000,
                'numeric_cols': ['weight', 'height'],
                'numeric_stats': stats,
                'categorical_n_levels_dict': {'animal': 2, 'color': 1},
                'one_hot_encoder_dicts': {'animal': {'cat': 0, 'mouse': 1}, 'color': {'blue': 0}}}

    index_html = encoder_package_to_html_page(packaged)

    assert isinstance(index_html, str)
    assert "<html" in index_html

    # ensure default URL is not public
    assert "http://httpbin.org/post" not in index_html

    index_html = encoder_package_to_html_page(packaged, post_url='PUBLIC')

    assert isinstance(index_html, str)
    assert "<html" in index_html
    # ensure default URL is using public debugging option
    assert "http://httpbin.org/post" in index_html

    write_page = True
    if write_page:
        filename = 'junk_index.html'
        fp = open(filename, 'w')
        fp.write(index_html)
        fp.close()

        print("wrote: %s" % filename)


