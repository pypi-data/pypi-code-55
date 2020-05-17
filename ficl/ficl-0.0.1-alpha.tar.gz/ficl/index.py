from argparse import RawDescriptionHelpFormatter
from textwrap3 import dedent

import argparse
import os


def main():
    available_commands = dedent('''
    available subcommands:
    \tclean              clean files out
    \trename             rename files
    '''.expandtabs(2))
    parser = argparse.ArgumentParser(prog='ficl', description='batch file transformer.', 
        epilog=available_commands, formatter_class=RawDescriptionHelpFormatter)
    
    parser.add_argument('subcommand', type=str, help='subcommand to run')
    parser.add_argument('path', type=str, help='path to target directory')

    parser.add_argument('-v', '--verbose', 
                        action='store_true', help='increase output verbosity')
    parser.add_argument('-r', '--recursively', 
                        action='store_true', help='include subdirectories')
    parser.add_argument('-n', '--no-special-files', 
                        action='store_false', help='exclude files that start with a dot')
    parser.add_argument('-p', '--prefix', metavar='',
                        type=str, help='filename prefix')
    parser.add_argument('-t', '--postfix', metavar='',
                        type=str, help='filename postfix')

    args = parser.parse_args()

    try:
        globals()[args.subcommand](args)
    except KeyError:
        print('Unrecognized command. Use -h flag to see usage tips.')
        return


def list_files(path, recursion=False):  
    filelist = []
    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filelist.append(os.path.join(dirpath, filename))
        if not recursion:
            break
    
    return filelist


def clean(args):
    if not os.path.exists(args.path):
        print('Path does not exist.')
        return
    
    if not os.path.isdir(args.path):
        print('Path does not point to a directory.')
        return

    filelist = list_files(args.path, args.recursively)
    successfully_cleaned = len(filelist)
    special_files = 0
    could_not_delete = 0

    for filepath in filelist:
        if os.path.basename(filepath)[0] == '.' and args.no_special_files:
            # Stumbled onto special file starting with a dot and --no-special-files flag
            # was set.
            successfully_cleaned -= 1
            special_files += 1
        else:
            try:
                with open(filepath, 'w') as f:
                    f.write('')
            except PermissionError:
                successfully_cleaned -= 1
                could_not_delete += 1
                if args.verbosity:
                    print('Could not clean out {}. Permission denied.'.format(filepath))

    if args.verbosity:
        print(f'Successfully cleaned out {successfully_cleaned}/{len(filelist)} files.')
        if args.no_special_files:
            print(f'{special_files} special files were ignored.')
        if could_not_delete > 0:
            print(f'Failed to delete {could_not_delete} files.')

    if args.prefix is not None or args.postfix is not None:
        # User needs to rename files too.
        rename(args)


def rename(args):
    if not os.path.exists(args.path):
        print('Path does not exist.')
        return
    
    if not os.path.isdir(args.path):
        print('Path does not point to a directory.')
        return

    filelist = list_files(args.path, args.recursively)
    successfully_renamed = len(filelist)
    special_files = 0
    could_not_delete = 0

    for filepath in filelist:
        if os.path.basename(filepath)[0] == '.' and args.no_special_files:
            # Stumbled onto special file starting with a dot and --no-special-files flag
            # was set.
            successfully_renamed -= 1
            special_files += 1
        else:
            try:
                new_name = os.path.join(
                    os.path.split(filepath)[0],
                    args.prefix or '' + os.path.split(filepath)[1] + args.postfix or ''
                )
                os.rename(filepath, new_name)
            except PermissionError:
                successfully_renamed -= 1
                could_not_delete += 1
                if args.verbosity:
                    print('Could not rename {}. Permission denied.'.format(filepath))
    
    if args.verbosity:
        print(f'Successfully renamed {successfully_renamed}/{len(filelist)} files.')
        if args.no_special_files:
            print(f'{special_files} special files were ignored.')
        if could_not_delete > 0:
            print(f'Failed to rename {could_not_delete} files.')


if __name__ == '__main__':
    main()
