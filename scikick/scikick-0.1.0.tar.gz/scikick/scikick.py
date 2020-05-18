#!/usr/bin/env python3
"""CLI tool script"""
import os
import sys
import argparse
from re import sub, match, IGNORECASE
from ruamel.yaml import YAML
import scikick
import scikick.yaml
from scikick.utils import reterr, warn, get_sk_snakefile, get_sk_exe_dir
from scikick.snakemake import run_snakemake, snake_status
from scikick.config import get_tabs
from scikick.config import new_tab_order
from scikick.config import reordered_analysis
from scikick.init import init
from scikick.yaml import yml_in

def run(args):
    """Run the workflow"""
    # check for empty analysis:
    analysis = yml_in()['analysis']
    if analysis is None or len(analysis) == 0:
        reterr("sk: Error: no pages have been added to scikick.yml, " + \
               "this can be done with\nsk: sk add my.rmd")

    if args.snakeargs is not None:
        run_snakeargs = " ".join(args.snakeargs)
        warn(f"sk: Snakemake arguments received: {run_snakeargs}")
    else:
        run_snakeargs = None
    run_snakemake(snakefile=get_sk_snakefile(), \
                  workdir=os.getcwd(), \
                  dryrun=args.dryrun, \
                  run_snakeargs=run_snakeargs, \
                  verbose=args.verbose)


def init_loc(args):
    """Initialize scikick project"""
    if not (args.git or args.dirs or args.yaml or args.readme):
        args.yaml = True
        warn("sk: No arguments supplied, defaulting to sk init -y")
        init(get_sk_exe_dir(), args)
        warn("sk: See the below arguments for other " + \
             "possible sk init components")
        parser_init.print_help()
        warn("sk: To add an R/Rmd script to the analysis use")
        warn("sk: sk add my.rmd")
        warn("sk: Then, to execute the workflow")
        warn("sk: sk run")
    else:
        init(get_sk_exe_dir(), args)


def add(args):
    """Add Rmds to scikick.yml"""
    for curr_rmd in args.rmd:
        scikick.yaml.add_file(os.path.normpath(curr_rmd))


def delete(args):
    """Remove Rmds from scikick.yml"""
    for curr_rmd in args.rmd:
        scikick.yaml.rm_file(os.path.normpath(curr_rmd))


def depadd(args):
    """Add dependencies to Rmds in scikick.yml"""
    rmd = args.rmd[0]
    for curr_dep in args.dep:
        scikick.yaml.add_dep(os.path.normpath(rmd), os.path.normpath(curr_dep))


def depdel(args):
    """Remove dependencies from Rmds in scikick.yml"""
    rmd = args.rmd[0]
    for curr_dep in args.dep:
        scikick.yaml.rm_dep(os.path.normpath(rmd), os.path.normpath(curr_dep))


def mv(args):
    """Rename an Rmd in scikick.yml and associated files"""

    # helpers for moving files
    def sk_move_file(src, dest):
        # this if statement could be handled directly by 'mv'
        if os.path.isfile(src):
            warn("sk: mv %s %s" % (src, dest))
            if not os.system("mv %s %s" % (src, dest)) == 0:
                sys.exit(1)
        else:
            reterr('sk: %s file not found' % (src))

    def sk_move_dir(src, dest):
        destdir = os.path.dirname(dest)
        # make parent dir if it doesn't exist
        if not os.path.isdir(destdir):
            os.makedirs(destdir)
        # only move if dest doesn't exist already
        if not os.path.isdir(dest):
            cmd = "mv %s %s" % (src, dest)
            warn("sk: " + cmd)
            if not os.system(cmd) == 0:
                sys.exit(1)
        else:
            reterr("%s exists, %s was not moved" % (dest, src))

    src = [os.path.normpath(p) for p in args.src]
    dest = [os.path.normpath(p) for p in args.dest]
    # for mvs inside reportdir
    reportdir = yml_in()["reportdir"]
    if not os.path.isdir(dest[0]) and len(src) > 1:
        reterr("sk: Error: moving multiple files to a single one")
    # format the input
    # ensure that src and dest are of the same length
    if os.path.isdir(dest[0]):
        dest = [os.path.normpath(os.path.join(dest[0], \
                                              os.path.basename(i))) for i in src]
    else:
        if dest[-1] == os.sep:
            reterr("sk: Error: directory %s does not exist" % dest)
    ## Error if .Rmd ext is removed
    if len(src) == 1:
        src_is_rmd = match(string=os.path.splitext(src[0])[-1], \
                           pattern=".Rmd$", flags=IGNORECASE) is not None
        dest_isnot_rmd = match(string=os.path.splitext(dest[0])[-1], \
                               pattern=".Rmd$", flags=IGNORECASE) is None
        if src_is_rmd and dest_isnot_rmd:
            warn("sk: Warning: changing file extension")
    for i, _ in enumerate(src):
        if args.git:
            warn("sk: git mv %s %s" % (src[i], dest[i]))
            if not os.system("git mv %s %s" % (src[i], dest[i])) == 0:
                sys.exit(1)
        else:
            sk_move_file(src[i], dest[i])

    # Moving mds, knitmetas and output figures in out_md/; 
    ## No need to change _site.ymls, since
    ## they are recreated after each change in scikick.yml
    for i, _ in enumerate(src):
        md_rootdir = os.path.join(reportdir, "out_md")
        md_destdir = os.path.join(md_rootdir, os.path.dirname(dest[i]))
        md_srcdir = os.path.join(md_rootdir, os.path.dirname(src[i]))
        if not os.path.isdir(md_destdir):
            os.makedirs(md_destdir)

        # Move .md
        md_src = os.path.join(md_rootdir, sub(pattern="\.Rmd$",
                                              repl=".md", string=src[i],
                                              flags=IGNORECASE))
        md_dest = os.path.join(md_destdir, sub(pattern="\.Rmd$",
                                               repl=".md", string=os.path.basename(dest[i]),
                                               flags=IGNORECASE))
        sk_move_file(md_src, md_dest)

        # Move knitmeta
        k_src = sub(pattern="\.md$", repl=".knitmeta.RDS",
                    string=md_src)
        k_dest = sub(pattern="\.md$", repl=".knitmeta.RDS",
                     string=md_dest)
        sk_move_file(k_src, k_dest)

        # Move markdown outputs (figures)
        tabname = sub(string=os.path.basename(md_src),
                      pattern="\.md$", repl="")
        md_srcfigdir = os.path.join(md_srcdir, "output", tabname)
        md_destfigdir = os.path.join(md_destdir, "output", tabname)
        if os.path.isdir(md_srcfigdir):
            sk_move_dir(md_srcfigdir, md_destfigdir)

        # rename all entries in scikick.yml from from to f_dest
        if 1 == scikick.yaml.rename(src[i], dest[i]):
            warn("sk: %s renamed to %s in ./scikick.yml" % (src[i], dest[i]))
        else:
            warn("sk: Warning: %s not found in ./scikick.yml" % src[i])


def snake(args):
    """Change snakemake-related arguments in scikick.yml"""
    # no help message by defaul (for now)
    if not args.get:
        if args.args_set is not None:
            scikick.yaml.set_snakeargs(args.args_set)
            warn("sk: Snakemake arguments updated")
        if args.conda is not None:
            scikick.yaml.set_arg('conda', args.conda)
        if args.singularity is not None:
            scikick.yaml.set_arg('singularity', args.singularity)
    else:
        if args.args_set is not None:
            warn("sk: Snakemake arguments are set to:\n%s" % \
                 scikick.yaml.get_snakeargs())
        if args.conda is not None:
            warn("sk: Conda environment file is \'%s\'" % \
                 scikick.yaml.get_arg('conda'))
        if args.singularity is not None:
            warn("sk: Singularity image is \'%s\'" % \
                 scikick.yaml.get_arg('singularity'))


def status(args):
    """Get status of the current workflow"""
    snake_status(snakefile=get_sk_snakefile(), \
                 workdir=os.getcwd(), \
                 exe_dir=get_sk_exe_dir(), \
                 verbose=args.verbose)


def layout(args):
    """Manipulate the tab order in resulting htmls by changing
    the order of keys of 'analysis' dict in scikick.yml.
    """
    config = yml_in()
    if config["analysis"] is None:
        reterr("sk: Error: no pages have been added to scikick.yml")
    tabs = get_tabs(config)

    if len(args.order) == 0:
        for i in range(len(tabs.keys())):
            print(f"{i}:  {list(tabs.keys())[i]}")
        return

    # detect submenu argument
    submenu = None
    if not args.order[0].isdigit():
        submenu = args.order.pop(0)
        warn('sk: layout for submenus is not yet available')
        return

    # get the new ordering based on the argument list
    order = new_tab_order(args.order, tabs)
    if order is None:
        reterr("sk: Wrong index list provided, " + \
               "must be a unique list of tab indices")
    # do the reordering of config['analysis']
    new_analysis = reordered_analysis(tabs, config['analysis'], order)
    # copy each item one by one from the new dict to the old one
    config['analysis'].clear()
    for k in new_analysis.keys():
        config['analysis'][k] = new_analysis[k]
    YAML().dump(config, open("scikick.yml", "w"))
    # print layout again
    tabs = get_tabs(config)
    for i in range(len(tabs.keys())):
        print(f"{i}:  {list(tabs.keys())[i]}")


parser = argparse.ArgumentParser(
    description="Scikick core functions")
parser.add_argument("-v", "--version", action="version", \
                    version="%(prog)s {version}".format(version=scikick.__version__))

subparsers = parser.add_subparsers(help="different scikick functions")

parser_run = subparsers.add_parser("run", help="run scikick workflow")
parser_run.add_argument("-v", "--verbose", action="store_true")
parser_run.add_argument("-d", "--dryrun", action="store_true", \
                        help="show the snakemake wokflow plan")
parser_run.add_argument("-s", "--snakeargs", nargs=argparse.REMAINDER, \
                        help="specify snakemake arguments to be used")
parser_run.set_defaults(func=run)

parser_init = subparsers.add_parser("init", \
                                    help="initializes the project to be used with scikick")
parser_init.add_argument("--yaml", "-y", action="store_true", \
                         help="create the template scikick.yml configuration file")
parser_init.add_argument("--dirs", "-d", action="store_true", \
                         help="create directories")
parser_init.add_argument("--git", "-g", action="store_true", \
                         help="append relevant directories to .gitignore")
parser_init.add_argument("--readme", "-r", action="store_true", \
                         help="prints a message that scikick is used in this project")
parser_init.set_defaults(func=init_loc)

parser_add = subparsers.add_parser("add", \
                                   help="add Rmd file(s) to the workflow")
parser_add.add_argument("rmd", nargs="+")
parser_add.set_defaults(func=add)

parser_del = subparsers.add_parser("del", \
                                   help="remove Rmd file(s) from the workflow")
parser_del.add_argument("rmd", nargs="+", \
                        help="Rmd(s) to be removed)")
parser_del.set_defaults(func=delete)

parser_depadd = subparsers.add_parser("depadd", \
                                      help="modify scikick configurartion by adding Rmds")
parser_depadd.add_argument("rmd", nargs=1, \
                           help="Rmd to which add the dependencies")
parser_depadd.add_argument("dep", nargs="+", \
                           help="dependencies to be added to the Rmd")
parser_depadd.set_defaults(func=depadd)

parser_depdel = subparsers.add_parser("depdel", \
                                      help="remove dependencies from the workflow")
parser_depdel.add_argument("rmd", nargs=1, \
                           help="Rmd from which to remove the dependencies")
parser_depdel.add_argument("dep", nargs="+", \
                           help="dependencies to be removed from the Rmd")
parser_depdel.set_defaults(func=depdel)

parser_mv = subparsers.add_parser("mv", \
                                  help="modify scikick configuration by moving Rmds")
parser_mv.add_argument("src", nargs="+", \
                       help="move from")
parser_mv.add_argument("dest", nargs=1, \
                       help="move to")
parser_mv.add_argument("-g", "--git", action="store_true", \
                       help="perform git mv instead")
parser_mv.add_argument("-v", "--verbose", action="store_true", \
                       help="show moves taking place, for debugging")
parser_mv.set_defaults(func=mv)

parser_snake = subparsers.add_parser("snake", \
                                     help="set/get snakemake arguments")
parser_snake.add_argument("--args-set", \
                          nargs=argparse.REMAINDER, \
                          help="specify snakemake arguments to be used")
parser_snake.add_argument("-g", "--get", action="store_true", \
                          help="conbine with others to get the value instead of setting it")
parser_snake.add_argument("--singularity", \
                          nargs="?", const="", \
                          help="set singularity image")
parser_snake.add_argument("--conda", \
                          nargs="?", const="", \
                          help="set conda env file")
parser_snake.set_defaults(func=snake)

parser_status = subparsers.add_parser("status", \
                                      help="get status of pages")
parser_status.add_argument("-v", "--verbose", action="store_true",
                           help="show full config with: (+) indicates Rmd=>md=html task,"
                                " (*) indicates md=>html task, (X) indicates file is not found.")
parser_status.set_defaults(func=status)

parser_layout = subparsers.add_parser("layout", \
                                      help="get tab layout/order")
parser_layout.add_argument("order", nargs="*", \
                           help="specify a new order")
parser_layout.set_defaults(func=layout)


def main():
    """Parse the arguments and run the according function"""
    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
        return
    func(args)
