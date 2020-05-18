"""Functions that run snakemake with various arguments"""
import os
import re
import subprocess
import sys
from scikick.utils import warn, reterr, get_sk_snakefile, get_sk_exe_dir
from scikick.yaml import yml_in

def run_snakemake(snakefile=get_sk_snakefile(), workdir=os.getcwd(), \
    verbose=False, dryrun=False, run_snakeargs=None):
    """Run snakemake with specified arguments
    snakefile -- string (path to the main snakefile)
    workdir -- string
    verbose -- bool
    dryrun -- bool
    run_snakeargs -- list (list of additional arguments to snakemake)
    """

    exe_dir = get_sk_exe_dir()
    yml = yml_in()
    snakemake_args = ""
    snakemake_args += f" --singularity-args=\"--bind {exe_dir}\" "
    snakemake_args += f" --snakefile {snakefile}"
    snakemake_args += f" --directory {workdir}"
    # config
    if dryrun:
        snakemake_args += f" --dry-run"
    # overwrite scikick.yml snakemake_args if run_snakeargs given
    if run_snakeargs is not None:
        snakemake_args += f" {run_snakeargs}"
    elif 'snakemake_args' in yml.keys() and yml['snakemake_args'] is not None:
        snakemake_args += f" {' '.join(yml['snakemake_args'])}"

    # Adding additional config variables not present in the users scikick.yml
    # --config has to be the last
    #config = {}
    #config['exe_dir'] = exe_dir
    #snakemake_args += " --config"
    #for i in config.keys():
    #    snakemake_args += f" {i}=\"{config[i]}\" "
    if verbose:
        sys.exit(subprocess.call(f"snakemake {snakemake_args}", shell=True))
    else:
        snake_p = subprocess.Popen(f"snakemake {snakemake_args}", \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        warn("sk: Starting snakemake")
        lines = list()
        while True:
            line = snake_p.stderr.readline().decode('utf-8')
            if not line:
                break
            lines.append(line)
            ntbd_match = re.match(".*Nothing to be done..*", \
                line)
            done_match = re.match(".*All rules from .* are complete.*", \
                line)
            rmd2md_match = re.match(".*Executing R chunks in (.*)," + \
                " outputting to (.*)", line)
            layout_match = re.match(".*Creating site layout from scikick.*", \
                line)
            html_match = re.match(".*Generating (.*) html page.*", \
                line)
            skwarn_match = re.match("sk: .*", line)
            quit_fromlines_match = re.match("Quitting from lines.*", line)
            if done_match is not None:
                warn("sk: Done, homepage is report/out_html/index.html")
            elif rmd2md_match is not None:
                warn("sk: Compiling %s to %s" % \
                    (rmd2md_match.groups()[0], rmd2md_match.groups()[1]))
            elif layout_match is not None:
                warn("sk: Creating site layouts from scikick.yml,"+ \
                    " outputting to _site.yml files")
            elif html_match is not None:
                warn("sk: Generating %s.html" % html_match.groups()[0])
            elif ntbd_match is not None:
                warn("sk: Nothing to be done")
            elif skwarn_match is not None:
                warn(re.sub("\n$", "", line))
            elif quit_fromlines_match is not None:
                warn(f"sk: %s" % re.sub('\n$', '', line))
        snake_p.wait()
        if snake_p.returncode != 0:
            warn("sk: Errors encountered, displaying last 30 lines " + \
                "from verbose output:")
            # Display captured snakemake output
            for line in lines[max(-len(lines), -30):]:
                sys.stderr.write(line)
        sys.exit(snake_p.returncode)

def snake_status(snakefile, workdir, exe_dir, verbose):
    """Print workflow status
    snakefile -- string (path to the main snakefile)
    workdir -- string
    exe_dir -- string (path to the system 'scikick.py' script)
    verbose -- bool
    """
    yml = yml_in()
    if yml['analysis'] is None or len(yml['analysis']) == 0:
        reterr("sk: Error: no pages have been added to scikick.yml, " + \
            "this can be done with\nsk: sk add my.rmd")
    # colors
    reportdir = yml['reportdir']
    md_prefdir = os.path.join(reportdir, "out_md")
    html_prefdir = os.path.join(reportdir, "out_html")
    status = subprocess.run(
        ['snakemake', '--snakefile', snakefile, \
            '--directory', workdir, \
            '--summary'], \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    status = list(map(lambda x: x.split("\t"), \
        status.stdout.decode("utf-8").split("\n")[0:-1]))
    # get all md files
    builds = {'from_Rmd' : [], 'from_md': []}
    for curr_md in map(lambda x: x[0], filter(lambda x: \
        re.match(".*.md$", x[0]) is not None, status[1:])):
        md_status = list(filter(lambda x: curr_md == x[0], status[1:]))[0]
        html_status = list(filter(lambda x: re.sub(f"{md_prefdir}(.*).md$", \
            f"{html_prefdir}\\1.html", curr_md) == x[0], status[1:]))[0]
        curr_rmd = re.sub(f"{md_prefdir}{os.sep}(.*).md$", \
            "\\1.Rmd", curr_md)
        if md_status[6] == "update pending":
            builds['from_Rmd'].append(curr_rmd)
        elif html_status[6] == "update pending":
            builds['from_md'].append(curr_rmd)
    # remove index.Rmd from 'builds'
    if 'index' not in list(map(lambda x: os.path.splitext(x)[0], \
        list(yml['analysis'].keys()))):
        # from Rmd => html
        builds['from_Rmd'] = \
            list(filter(lambda x: os.path.splitext(x)[0] != 'index', \
                builds['from_Rmd']))
        # from md => html
        builds['from_md'] = \
            list(filter(lambda x: os.path.splitext(x)[0] != 'index', \
                builds['from_md']))
    # print status
    if verbose:
        if len(builds['from_Rmd']) > 0:
            print("Number of Rmd => md => html tasks (+): " + \
                f"{len(builds['from_Rmd'])}")
        if len(builds['from_md']) > 0:
            print(f"Number of md => html tasks (*): " + \
                f"{len(builds['from_md'])}")
        analysis = yml["analysis"]
        for curr_page in analysis.keys():
            # status of analysis keys
            if curr_page.lower() in (x.lower() for x in builds["from_Rmd"]):
                status = "+"
            elif curr_page in builds["from_md"]:
                status = "*"
            elif not os.path.exists(curr_page):
                status = "X"
            else:
                status = " "
            print(f"{status} {curr_page}")
            # status of analysis values (dependencies)
            if analysis[curr_page] is not None:
                for curr_dep in analysis[curr_page]:
                    if curr_dep.lower() in \
                        (x.lower() for x in builds["from_Rmd"]):
                        status = "+"
                    elif curr_dep in builds["from_md"]:
                        status = "*"
                    elif not os.path.exists(curr_dep):
                        status = "X"
                    else:
                        status = " "
                    print(f"{status} \t{curr_dep}")
    else:
        if len(builds['from_Rmd']) == 0 and len(builds['from_md']) == 0:
            warn("sk: Nothing to be done")
        if len(builds['from_Rmd']) > 0:
            print("Number of Rmd => md => html tasks: " + \
                f"{len(builds['from_Rmd'])}")
            for rmdf in builds['from_Rmd']:
                print(f"\t{rmdf}")
        if len(builds['from_md']) > 0:
            print(f"Number of md => html tasks: {len(builds['from_md'])}")
            for rmdf in builds['from_md']:
                print(f"\t{rmdf}")
