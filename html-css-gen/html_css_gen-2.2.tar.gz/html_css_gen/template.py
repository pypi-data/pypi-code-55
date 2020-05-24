#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 03:23:44 2020

@author: guangyong
"""
import os


class init_template:

    def __init__(self, **payload):
        for x in payload:
            self.__dict__['{}_html'.format(payload[x])], self.__dict__[
                '{}_css'.format(payload[x])] = self.read_component(payload[x])

    def add_tags(self):
        instructions = [{'output_css': ['<style> \n', '\n </style>']},
                        {'output_html': ['<html> \n', '\n </html>']}]

        for x in range(0, len(instructions)):
            key = list(instructions[x].keys())[0]
            steps = instructions[x][key]
            self.__dict__[key] = steps[0] + self.__dict__[key]
            self.__dict__[key] += steps[1]

    def read_component(self, name):
        with open('{}.html'.format(name)) as f:
            data = f.read().strip().split('</html>')
            if len(data) != 2:
                raise Exception('HTML not found')
            html = data[0].replace('<html>', '').strip()
            css_data = data[1].split('</style>')
            css = None
            if len(css_data) == 2:
                css = css_data[0].replace('<style>', '').strip()
            return html, css

    def loop_check(self, checkOjb, checklist):
        check = [True if z in checkOjb else False for z in checklist]
        return True if any(check) else False

    def consolidate_css(self, css):
        data = [x.strip() for x in css.splitlines()]
        subHeaderIndicator = ['{']
        css_data = {}
        temp_key = None
        for y in data:
            current_entries = css_data.keys()
            if y:
                # create a new entry
                if self.loop_check(y, subHeaderIndicator) and y not in current_entries:
                    css_data[y] = []
                    continue
                # assign temp key and do nth if a new row is discovered but already created
                elif y in current_entries:
                    temp_key = y
                    continue
                # last row detected
                elif '}' in y:
                    temp_key = None
                    continue
                # no new row created and no temp key assigned, just append to last entry in the dict
                if temp_key == None:
                    css_data[list(css_data.keys())[-1]].append(y)
                # no new row created but temp key assigned, find the temp key and append there
                else:
                    css_data[temp_key].append(y)
        css_data = {key: set(value) for key, value in css_data.items()}
        consolidated_css = ''
        for entry in css_data:
            consolidated_css += entry + '\n'
            for value in css_data[entry]:
                consolidated_css += value + '\n'
            consolidated_css += '}\n'
        return consolidated_css

    def clean_css(self, css):
        data = [x.strip() for x in css.splitlines()]
        subHeaderIndicator = ['{', '}']
        output = ''
        for y in data:
            if y:
                check = [True if z in y else False for z in subHeaderIndicator]
                temp_entry = y + '\n' if any(check) else '    ' + y + '\n'
                output += temp_entry
        return output[:-1]
        #self.output_css = output[:-1]

    def combine_element(self):
        # combine html
        output_html = ''
        output_css = ''
        for k in self.__dict__:
            if 'html' in k:
                output_html += self.__dict__[k] + '\n'
            if 'css' in k and self.__dict__[k] != None:
                output_css += self.__dict__[k] + '\n'
        self.output_html = output_html
        consolidated_css = self.consolidate_css(output_css)
        cleaned_css = self.clean_css(consolidated_css)
        self.output_css = cleaned_css
        self.add_tags()
        self.final_output = self.output_html + '\n\n' + self.output_css
        return self.final_output

    def add_parent_html(self, change_data, html_tags):
        for entry in html_tags:
            pos = change_data.find('<html>') + 6
            change_data = change_data[:pos] + \
                '\n{}'.format(entry[0]) + change_data[pos:]
            pos = change_data.find('</html>')
            change_data = change_data[:pos] + \
                '{}\n'.format(entry[1]) + change_data[pos:]
        return change_data

    def add_customised_css(self, change_data, css_input):
        cleaned_css = self.clean_css(css_input)
        output = change_data.replace(
            '</style>', '') + '\n{}\n</style>'.format(str(cleaned_css))
        return output

    def check_if_file_exists(self, path):
        if os.path.exists(path):
            os.remove(path)

    def export(self, export_data, filename):
        path = '{}.html'.format(filename)
        self.check_if_file_exists(path)
        with open(path, 'w') as f:
            f.write(export_data)

    def populate(self, change_data, **data):
        change_data_list = change_data.split('</html>')
        try:
            output = change_data_list[0].format(
                **data) + '</html>\n' + change_data_list[1]
        except KeyError as error:
            print(
                '{%s} indicated in html but now subitute value provided' % error)
            raise
        return output

    def __str__(self):
        return self.change_data


if __name__ == '__main__':
    pass
