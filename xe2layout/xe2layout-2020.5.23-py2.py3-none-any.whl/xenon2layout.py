#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# @package xenon2
###############################################################################

import logging
import sys
import os
import traceback
import argparse
import tempfile
import ctypes  # An included library with Python install.

import xe2layout
import xe2layout.inoutstream

__actions_list__ = {}
__actions_list__['generate_template'] = xe2layout.generate_template
__actions_list__['get_release'] = xe2layout.get_release


###############################################################################
# test the dir name
#
# @param prospective_dir The dirname
# @return prospective_dir.
###############################################################################
def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise Exception(
            "readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise Exception(
            "readable_dir:{0} is not a readable dir".format(prospective_dir))


###############################################################################
# test the filename for argparsing
#
# @param filename The filename
# @return filename.
###############################################################################
def is_real_file(filename):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.isfile(filename):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(filename))
    return filename


###############################################################################
# Create a windows message box
#
# @param text The message
# @param title The title of the windows
# @return nothing.
###############################################################################
def message_box(text, title):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


###############################################################################
# Define the parsing of arguments of the command line
###############################################################################
def get_parser_for_command_line():
    docstring = ""
    for action in __actions_list__:
        docstring = docstring + action + ":\n" + \
            __actions_list__[action].__doc__.split("@")[0][0:-3] + "\n\n"

    description = docstring

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--conf', dest="conf_filename", required=False,
                        type=is_real_file,
                        help="the configuration file in yaml", metavar="FILE")
    parser.add_argument('--dir', dest="directory", required=False,
                        type=readable_dir,
                        help="Target folder for the template")
    parser.add_argument('--get-template', dest="get_template",
                        choices=['yes', 'no'], default='no',
                        help="Target folder for the template")
    parser.add_argument('--version', dest="version", default=None,
                        help="Version for the template")
    parser.add_argument('--template-name', dest="template_name", default=None,
                        help="Name of the template to upload")
    parser.add_argument('--gen-template', action='store', dest='gen_template',
                        choices=['yes', 'no'], default='no',
                        help='generate the template')
    parser.add_argument('--windows', action='store_true', dest='windows',
                        help='Define if we need all popups windows.')
    parser.add_argument('--verbose', action='store_true', dest='verbose',
                        help='Put the logging system on the console for info.')

    return parser

###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the filename of THIS script.
###############################################################################
def __get_this_filename():
    result = ""
    if getattr(sys, 'frozen', False):
        # frozen
        result = sys.executable
    else:
        # unfrozen
        result = __file__
    return result


###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the folder of THIS script.
###############################################################################
def __get_this_folder():
    return os.path.split(os.path.abspath(os.path.realpath(
        __get_this_filename())))[0]


###############################################################################
# Logging system
###############################################################################
def __set_logging_system():
    log_filename = os.path.splitext(os.path.abspath(
        os.path.realpath(__get_this_filename())))[0] + '.log'

    if xe2layout.inoutstream.is_frozen():
        log_filename = os.path.abspath(os.path.join(
            tempfile.gettempdir(),
            os.path.basename(__get_this_filename()) + '.log'))

    logging.basicConfig(filename=log_filename, level=logging.INFO,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler(
        xe2layout.inoutstream.initial_stream().stdout)
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger

    if not xe2layout.inoutstream.is_frozen():
        logging.getLogger('').addHandler(console)

    return console

###############################################################################
# Main script
###############################################################################
def __main():
    console = __set_logging_system()
    # ------------------------------------
    logging.info('+')
    logging.info('-------------------------------------------------------->>')
    logging.info('Started %s', __get_this_filename())
    logging.info('The Python version is %s.%s.%s',
                 sys.version_info[0], sys.version_info[1], sys.version_info[2])

    try:
        parser = get_parser_for_command_line()
        logging.info("parsing args")
        args = parser.parse_args()
        logging.info("parsing done")

        if args.verbose:
            console.setLevel(logging.INFO)

        logging.info("conf_filename=%s", args.conf_filename)
        logging.info("gen_template=%s", args.gen_template)
        logging.info("directory=%s", args.directory)
        logging.info("get_template=%s", args.get_template)
        logging.info("template_name=%s", args.template_name)
        logging.info("version=%s", args.version)
        logging.info("verbose=%s", args.verbose)

        args.gen_template_bool = (args.gen_template == "yes")
        args.get_template_bool = (args.get_template == "yes")

        if args.gen_template_bool:
            xe2layout.generate_template(args.conf_filename)

        if args.get_template_bool:
            if args.directory is None or len(args.directory) == 0:
                raise Exception('You need to define the destination directory')
            if args.template_name is None or len(args.template_name) == 0:
                raise Exception('You need to define the template name')
            logging.info("Get the template version %s", args.version)
            logging.info("    the template name %s", args.template_name)
            xe2layout.get_release(
                args.directory, args.template_name, args.version)

    except argparse.ArgumentError as errmsg:
        logging.error(str(errmsg))
        if ('args' in locals()) and (args.windows):
            message_box(text=parser.format_usage(), title='Usage')

    except SystemExit:
        if ('args' in locals()) and (args.windows):
            message_box(text=parser.format_help(), title='Help')

    except Exception as ex:
        logging.error(str(ex))
        if ('args' in locals()) and (args.windows):
            message_box(text=str(ex), title='Usage')

    except:
        var = traceback.format_exc()
        logging.error('Unknown error : \n %s', var)
        if ('args' in locals()) and (args.windows):
            message_box(text='Unknown error : \n' + var,
                        title='Error in this program')
        # raise

    logging.info('Finished')
    logging.info('<<--------------------------------------------------------')
    logging.info('+')
    # ------------------------------------


# -----------------------------------------------------------------------------
# Call main if the script is main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    __main()
