import argparse
import shutil
import zipfile
from si_wg_docgen import ttl2md, md2word, get_template


def generate():
    # build a parser for the command line arguments
    parser = argparse.ArgumentParser()

    # sample additional option to load/store from/to the expanded graph
    parser.add_argument(
        "ttl", type=str, nargs="+", help="turtle files to load",
    )

    args = parser.parse_args()

    # remove old sample/ directory
    shutil.rmtree('./sample/', ignore_errors=True)

    # unzip template docx into sample/ directory
    template = get_template()
    zipped = zipfile.ZipFile(template)
    zipped.extractall(path='./sample/')

    # generate the markdown from the ttl file
    generated_md = ttl2md.main(args.ttl)

    # generate docx from markdown
    md2word.main(generated_md, './sample/word/document.xml')

    shutil.make_archive('generated.docx', 'zip', './sample')
    shutil.move('generated.docx.zip', 'generated.docx')


if __name__ == '__main__':
    generate()
