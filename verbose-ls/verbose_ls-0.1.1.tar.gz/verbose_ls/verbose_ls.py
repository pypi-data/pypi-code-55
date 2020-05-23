#!/usr/bin/env python

import argparse
from subprocess import check_output


class LSFormatter:
    """Formats ls command into verbose, human readable output."""

    code_to_file_permission = {
        'r': 'Read',
        'w': 'Write',
        'x': 'Execute'
    }
    code_to_file_type = {
        '-': 'Regular file',
        'b': 'Block special file',
        'c': 'Character special file',
        'd': 'Directory',
        'l': 'Symlink',
        'p': 'Pipe (FIFO)',
        's': 'Socket link'
    }

    def __init__(self, files):
        self.verbose_ls_output = []
        self._get_ls_output(files)
        self.current_line = None

    def _get_ls_output(self, files):
        if not files:
            files = ['.']

        ls_output = []
        for file in files:
            ls_output += check_output(['ls', '-lh', file]).decode().split("\n")
        self.all_lines = [x.split() for x in ls_output]
        # get rid of empty space or mac adding 'total' at top
        self.all_lines = [y for y in self.all_lines if len(y) == 9]

    def format_and_print(self):
        for line in self.all_lines:
            self.verbose_ls_output = []
            self.current_line = line

            self._add_readable_file_name()
            self._add_readable_file_type()
            self._add_all_readable_perms()
            self._add_readable_meta_data()

            print(" \n ".join(self.verbose_ls_output) + "\n")

    def _add_readable_file_name(self):
        filename = self.current_line[-1]
        self._update_verbose_ls_output("Filename", filename)

    def _add_readable_file_type(self):
        file_type_code = self.current_line[0][0]
        file_type = self.code_to_file_type[file_type_code]
        self._update_verbose_ls_output("File Type", file_type)

    def _add_all_readable_perms(self):
        perm_info = self.current_line[0]

        perm_codes_and_types = [
            [perm_info[1:4], 'Owner'],
            [perm_info[4:7], 'Group'],
            [perm_info[7:10], 'Other Users']
        ]
        for perm_code_and_type in perm_codes_and_types:
            self._add_readable_perms(perm_code_and_type[0], perm_code_and_type[1])

    def _add_readable_perms(self, perm_codes, owner_type):
        readable_perms = []
        for perm_code in perm_codes:
            permission = self.code_to_file_permission.get(perm_code)
            if permission:
                readable_perms.append(permission)

        readable_perms = ', '.join(readable_perms)
        self._update_verbose_ls_output('{} Permissions'.format(owner_type), readable_perms)

    def _add_readable_meta_data(self):
        self._update_verbose_ls_output('Hard Links', self.current_line[1])
        self._update_verbose_ls_output('Owner', self.current_line[2])
        self._update_verbose_ls_output('Owner Group', self.current_line[3])
        self._update_verbose_ls_output('Size', self.current_line[4])
        last_modified = " ".join(self.current_line[5:8])
        self._update_verbose_ls_output('Last Modified', last_modified)

    def _update_verbose_ls_output(self, title, desc):
        self.verbose_ls_output.append("{}: {}".format(title, desc))


def main():
    parser = argparse.ArgumentParser(description='Verbosely Describe files.')
    parser.add_argument('files', nargs='*')

    args = parser.parse_args()
    LSFormatter(args.files).format_and_print()


if __name__ == '__main__':
    main()
