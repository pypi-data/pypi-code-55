import argparse
from wikisearch import Wiki

def main():

    arg = argparse.ArgumentParser()

    # Add arguments
    arg.add_argument('-l', '--lang', default='EN', help='Language you are looking in (default: EN)')
    arg.add_argument('search', type=str, help='Word you are searching for')

    options = arg.parse_args()

    input_lang = options.lang
    input_search = options.search

    # Initialize Wikipedia search
    if input_lang == 'EN':
        wiki = Wiki(input_search)
    else:
        wiki = Wiki(input_search, input_lang)

    wiki.search_meaning()
    wiki.print_all()


if __name__ == '__main__':

    main()
