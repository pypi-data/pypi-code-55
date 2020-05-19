# textparsingtools
# Author: Reid Prichard
# Date: 19 May 2020
# Description: This file reads and delimits an ANSYS Fluent transcript file to create a CSV file containing
#              a summary of DPM statistics.
# Instructions to install the xlsxwriter library (Windows):
# - Be sure you have Python added to PATH
# - Open a command line and enter the command 'python -m pip install xlsxwriter'
# - If prompted, you may first want to update pip via 'python pip install --upgrade pip'
# - You may need to point your compiler to pip's path. In Visual Studio code, this is done by adding the following
#   line to settings.json: "python.autoComplete.extraPaths": ["[Python directory]\\Lib\\site-packages"]
#  
# Changelog:
# v10
# - Incorporated transcript_reader_functions
# - Revised analyzed_transcript to read a single file at a time.
# - Removed some control over zone names - if a list is not input, they will be sorted alphabetically
# - recursively_replace now accepts a list of replacement strings
# V9.2
# - Modularized print function
# - Removed CSV option
# V9.1b
# - Added injection monitoring.
# V9.1
# - Added functionality to write to Excel file.
# - Moved timestep data recording to its own function.
# - Removed some unused code. 
# V9.0
# - Decomposed main code into functions. This should allow the script to be generalized to other applications more easily.
# - Moved existing and new functions to transcript_reader_functions.py
# V8.1
# - Added some comments.
# - Fixed some bugs.
# - Cleaned up some unused snippets and variables.
# - Added line_delimiters, replacement_strings, and associated functionality.
# - Decomposed parsing into finding particle fates and mass flows separately.
# - Simplified file name specification.
# - Cleaned up output file
# - Added timestep recording
# - Added 'net' and 'mass flow difference' recording
# - Added ability to study multiple files
# - Added ability to change directory.
# 
# Todo:
# - Finish moving functionality into functions
# - Account for beginning/end strings occurring at a specific location or any
# - Get rid of 'trimming' functionality, except for debugging
# - Move file specifications to a function input
# - Search through all input files for consistent zone names
# - Change replacement string format to a list of lists
# - Implement regex
# - Remove old_chars and new_chars from recursively_replace

# ************************************* Script begin *************************************
import os
import re
import xlsxwriter

def build_header(names, variables):
    """Builds a header for a dataset where columns consist of repeating 
    variables for a list of names/categories

    ### Parameters
    1. names : list
        - a list containing names of data categories
    2. variables : list
        - a list of repeating variables

    ### Returns
    - list
        - a nested list containing two header rows, where the first
          consists of <names> listed sequentially every n elements, and
          the second consists of cyclic repetition of n <variables>
    """
    header = [[],[]]
    for i in range(len(names)*len(variables)):
        if i % len(variables) == 0:
            # print(int(i/vars_per_name), len(names))
            header[0].append(names[int(i/len(variables))])
        else:
            header[0].append('')
        header[1].append(variables[i % len(variables)])
    return header

def trim_lines(lines, data_begin_string, data_end_string):
    """Trims a list of lines of text based on strings bounding desired content

    ### Parameters
    1. lines : list
        - a list containing each line of text
    2. data_begin_string : str
        - a string found in a line at the beginning of the desired data
    3. data_end_string: str
        - a string found in a line at the end of the desired data

    ### Returns
    - list
        - a list of lines of text, trimmed according to the specified
          bounds
    """

    # TODO: Rewrite this more efficiently, possibly copying from get_text_data.

    trimmed_lines = []
    reading_data = False
    line_number = 0
    previous_timestep_data = [0,0]
    while line_number < len(lines):
        # if debug and line_number % 1000 == 0:
            # print('Reading line:', file_lines[line_number])
        line = lines[line_number]

        if line.find(data_begin_string) != -1:
            reading_data = True
        elif line.find(data_end_string) != -1:
            reading_data = False

        if reading_data:
            trimmed_lines.append(line)

        line_number += 1
    return trimmed_lines

def get_dpm_flow_time(lines):
    """Creates a list of flow time for each dpm report in text from a Fluent transcript file

    ### Parameters
    1. lines : list
        - a list of lines of a Fluent transcript file
    
    ### Returns
    - list
        - a list of flow times corresponding with each dpm report
    """

    last_match = []
    flow_time_list = []
    
    time_regex = re.compile(r"Flow time = ((\d|\.)+)")
    report_regex = re.compile(r"-\n")

    for line in lines:
        match_flow_time = time_regex.search(line)
        match_report = report_regex.search(line)
        if match_flow_time:
            flow_time = match_flow_time.group(1)
            last_match = 'flow_time'
        if match_report and last_match == 'flow_time':
            flow_time_list.append(flow_time)
            last_match = 'report'
    
    return flow_time_list

def get_injection_groups(lines):
    """Creates a list of injection group numbers in dpm reports within text from a Fluent transcript file

    ### Parameters
    1. lines : list
        - a list of lines of a Fluent transcript file
    
    ### Returns
    - list
        - a list of injection group numbers in string format
    """

    injection_group_list = []

    regex = re.compile(r"injection-(\d+)")

    for line in lines:
        match = regex.search(line)
        if match and (len(injection_group_list) == 0 or not match.group(1) == injection_group_list[-1]):
            injection_group_list.append(match.group(1))
    
    return injection_group_list

def get_text_data(lines, data_begin_string, data_end_string, *column_numbers, data_begin_offset = 1):
    """Extracts whitespace-separated strings from lines of text

    ### Parameters 
    1. lines : list
        - a list containing each line of the text
    2. data_begin_string : str
        - a regex raw string found at the beginning of the line before
          data begins (unless otherwise specified). Be sure to properly
          escape special characters.
    3. data_end_string : str
        - a regex raw string found at the beginning of the line
          immediately after data ends. Be sure to properly escape
          special characters.
    4. column_numbers : int
        - a variable-length list of column numbers (beginning with 0)
          pointing to desired data
    5. data_begin_offset : int, (default 1)
        - the number of lines to skip after data_begin_string before beginning
          reading data

    ### Returns
    - list
        - a list of lists of the data, where each inner list represents
          a single row. Blocks of data are separated by blank rows.
    """

    data = []
    reading_data = False

    lines_iter = iter(lines)
    for line in lines_iter:
        if re.search(data_begin_string, line):
            reading_data = True
            for i in range(data_begin_offset-1):
                next(lines_iter)
            continue
        elif reading_data == True and re.match(data_end_string, line):
            reading_data = False
            # Appends a blank row to divide data
            data.append([[]]*len(column_numbers))
            continue

        if reading_data:
            # Uses regex to decompose line into whitespace-separated
            # values, then takes the columns corresponding to
            # column_numbers
            data.append([re.findall(r"(\S+)", line)[i] for i in range(len(column_numbers))])
    
    # Returns the transpose of data
    # NOTE: Possible inconsistent results with only 1 column
    return data#[list(i) for i in zip(*data)]

def get_user_input(prompt, acceptable_answers):
    answer = input(prompt)
    while answer not in acceptable_answers:
        print('Please enter a response from the following list:', acceptable_answers)
        answer = input()
    return answer

def interleave_datasets(names, *data):
    out_data = []
    for index in range(len(names)):
        for dataset in data:
            var_count = int(len(dataset)/len(names))
            [out_data.append(cell) for cell in dataset[index*var_count:(index+1)*var_count]]
    return out_data

def get_transcript_zone_names(lines):
    unique_names = []
    [unique_names.append(name) for name in get_text_data(lines, r"> report dpm-summary", r"\n", 0, 4) if name not in unique_names]
    return unique_names

# Recursively replaces one string with another. Useful for collapsing a repeated string or character.
def recursively_replace(string, replacement_strings, max_iterations=100):
        #print("Replacing '" + old_chars + "' with '" + new_chars + "' in string: '" + string + "'")
    for replacement_set in replacement_strings:
        # print(replacement_set)
        counter = 0
        old_chars = replacement_set[0]
        new_chars = replacement_set[1]
        
        if new_chars.find(old_chars) != -1:
            print('Error in recursively_replace: new_chars contains old_chars. Infinite loop will occur.')
        
        while string.find(old_chars) != -1:
            string = string.replace(old_chars, new_chars)
            counter += 1
            if counter > max_iterations:
                print('Error in recursively_replace: too many iterations. Input a larger value of max_iterations if you want to keep going.')
                break
    return string

def transpose_transcript_data(data, names, empty_value = ''):
    block = []
    transposed_data = []
    row_num = 0
    # Determines number of variables. Assumes one column represents name.
    var_count = len(data[0])-1
    # Create a column for number of names times number of variables per
    # name. Name is subtracted from the length of the row.
    [transposed_data.append([]) for i in range(var_count*len(names))]
    for row in data:
        print(row)
        if row[0]:
            block.append(row)
        if not row[0] or data.index(row) == len(data)-1:
            row_num += 1
            for row in block:
                col_index = names.index(row[0])
                [transposed_data[col_index*var_count + i - 1].append(row[i]) for i in range(1,len(row))]
            [col.append(empty_value) for col in transposed_data if len(col) < row_num]
            block = []
    
    return transposed_data

# Writes data to one or more sheets in a new or existing Excel file
# data: list of lists of lists, where the hierarchy is such: data[sheet][column][row]
# header: list of lists, where hierarchy is such: header[row][column]. This will be written to the top of each sheet.
# book_name: name of workbook to be created
# sheet_names: list of sheet names; dimensionality must agree with the top-level dimension of data
# overwrite: boolean to indicate whether an existing file with name book_name should be overwritten or appended to

def write_excel_file(book_name, data, header = [], sheet_names = [], overwrite = False, text_to_num = True):
    if not overwrite and os.path.isfile(book_name + '.xlsx'):
        print()
        if str.upper(get_user_input('Warning: output file already exists. Do you want to overwrite? (Y/N)\n',['Y','N','y','n'])) == 'N':
            book_name = book_name + '_2'
            print('Output saved to ' + book_name + '.xlsx')


    workbook = xlsxwriter.Workbook(book_name + '.xlsx')

    # timestep_index_format = workbook.add_format({'num_format': '0'})
    # timestep_value_format = workbook.add_format({'num_format': '0.000'})
    # particle_fate_format = workbook.add_format({'num_format': '0'})
    # mass_flow_format = workbook.add_format({'num_format': '0.00E+00'})

    for sheet_num in range(len(data)):
        if sheet_names:
            sheet = workbook.add_worksheet(sheet_names[sheet_num])
        else:
            sheet = workbook.add_worksheet()

        if header:
            header_rows = len(header)
        else:
            header_rows = 0

        for row_num in range(len(header)):
            row = header[row_num]
            for col_num in range(len(row)):
                sheet.write(row_num, col_num, header[row_num][col_num])

        for col_num in range(len(data[sheet_num])):
            col = data[sheet_num][col_num]
            for row_num in range(len(col)):
                # print(data[sheet_num][col_num][row_num+header_rows])
                cell_data = data[sheet_num][col_num][row_num]
                if text_to_num:
                    try:
                        cell_data = float(cell_data)
                    except: 
                        pass
                sheet.write(row_num + header_rows, col_num, cell_data)
                # print('Writing', data[sheet_num][col_num][row_num],'to cell',col_num,',',row_num)

    try:
        workbook.close()
        print('Workbook successfully closed')
    except:
            print('Error: could not write to ', book_name + '.xlsx.', 'Make sure the file is not open.')