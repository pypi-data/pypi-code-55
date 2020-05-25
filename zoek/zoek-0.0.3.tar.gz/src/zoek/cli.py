import click
from os import getcwd

from zoek.file_iterator_from_path import file_iterator_from_path
from zoek.attach_filters_to_iterable_of_files import attach_filters_to_iterable_of_files
from zoek.print_file_iterator import print_file_iterator
import zoek.text as text


@click.command()
@click.argument('path', default=getcwd())
@click.option('--depth', '-d', type=int, default=1, help=text.depthHelp)
@click.option('--showpath', '-P', is_flag=True, help=text.showpathHelp)
@click.option('--startswith', '-s', type=str, help=text.startswithHelp)
@click.option('--contains', '-c', type=str, help=text.containsHelp)
@click.option('--minsize', '-m', type=int, help=text.minsizeHelp)
@click.option('--datecreated', '-dc', type=int, help=text.datecreatedHelp)
@click.option('--datemodified', '-dm', type=int, help=text.datemodifiedHelp)
def fetch(depth, path, showpath, startswith, minsize, contains, datecreated, datemodified):
    # put below in function
    files = file_iterator_from_path(path, max_depth=depth)
    files = attach_filters_to_iterable_of_files(files,
                                                depth,
                                                showpath,
                                                startswith,
                                                minsize,
                                                contains,
                                                datecreated,
                                                datemodified)

    print_file_iterator(files, showpath)


if __name__ == '__main__':
    fetch()
