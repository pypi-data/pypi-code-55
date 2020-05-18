"""General scikick.yml functions"""
import os
import re
from ruamel.yaml.compat import ordereddict
from scikick.utils import reterr
from scikick.yaml import yml_in


class ScikickConfig:
    """
    A class for reading and manipulating all configuration
    settings.
    """

    def read(self):
        self.config = yml_in()

    def __init__(self, filename=None):
        if filename is None:
            self.filename = "scikick.yml"
        else:
            self.filename = filename
        self.read()

    @property
    def analysis(self):
        if self.config['analysis'] is not None:
            return self.config['analysis']
        else:
            reterr("No analysis field found in scikick config")

    @property
    def report_dir(self):
        return self.config['reportdir']

    @property
    # Duplicate of global function read_deps()
    def inferred_deps(self):
        """Return dictionary of {Rmd -> [dependencies], ...}"""
        deps = {}
        for rmd in self.analysis.keys():
            rmd_name = os.path.splitext(rmd)[0]
            deps[rmd_name] = []
            deps[rmd_name].append(rmd)
            if isinstance(self.analysis[rmd], list):
                for dep in self.analysis[rmd]:
                    if os.path.splitext(dep)[-1].lower() == ".rmd":
                        out_md_file = os.path.join(self.report_dir, "out_md", \
                                                   re.sub('.rmd$', ".md", dep, \
                                                          flags=re.IGNORECASE))
                        deps[rmd_name].append(out_md_file)
                    else:
                        deps[rmd_name].append(dep)
        return deps


def read_deps(analysis, report_dir):
    """Return dictionary of {Rmd -> [dependencies], ...}
    analysis -- 'analysis' dictionary from scikick.yml
    report_dir -- 'reportdir' field in scikick.yml
    """
    deps = {}
    for rmd in analysis.keys():
        rmd_name = os.path.splitext(rmd)[0]
        deps[rmd_name] = []
        deps[rmd_name].append(rmd)
        if isinstance(analysis[rmd], list):
            for dep in analysis[rmd]:
                if os.path.splitext(dep)[-1].lower() == ".rmd":
                    out_md_file = os.path.join(report_dir, "out_md", \
                                               re.sub('.rmd$', ".md", dep, \
                                                      flags=re.IGNORECASE))
                    deps[rmd_name].append(out_md_file)
                else:
                    deps[rmd_name].append(dep)
    return deps


def get_tabs(config):
    """Return a list of tab names determined from scikick.yml
    'analysis:' dict
    config -- scikick.yml as an ordereddict
    """
    # get tab strucutre
    tabs = {}
    for i in config['analysis'].keys():
        tabname = os.path.dirname(i)
        if tabname == "":
            tabname = "./"
        if tabname not in tabs.keys():
            tabs[tabname] = []
        if tabname == "./":
            tabs[tabname].append("./%s" % \
                                 re.sub('.rmd$', "", i, flags=re.IGNORECASE))
        else:
            tabs[tabname].append(re.sub('.rmd$', "", i, flags=re.IGNORECASE))
    # get the common dir suffix for all files
    dnames = tabs.keys()
    dlists = list(map(lambda d: d.split(os.path.sep), dnames))
    maxdir = list(filter(lambda x: len(x) == max(map(len, dlists)), dlists))[0]
    igfirst = 0
    # ignore first 'igfirst' common directories for all tab names
    for md_filename in maxdir:
        if all(map(lambda cl: cl[igfirst] == md_filename if len(cl) > igfirst \
                else False, dlists)):
            igfirst += 1
        else:
            break

    def rm_commdir(text, igfirst):
        ntxt = os.path.sep.join(text.split(os.path.sep)[igfirst:])
        return ntxt if ntxt != "" else "./"

    tabs = ordereddict(map(lambda k: (rm_commdir(k, igfirst), tabs[k]), \
                           tabs.keys()))
    # all files in './' have their own tab
    if "./" in tabs.keys():
        wd_idx = list(tabs.keys()).index("./")
        tabs["./"].reverse()
        for root_file in tabs["./"]:
            fname = os.path.basename(root_file)
            if fname in tabs.keys():
                fname = f"{fname}.Rmd"
            tabs.insert(wd_idx, fname, [root_file])
        del tabs["./"]
    return tabs


def new_tab_order(args_order, tabs):
    """Get the new order of tabs based on the user input.
    Returns a list of indices, which would be used to reorder the
    'analysis' keys in scikick.yml
    args_order -- order provided by the user (list of indices as strings)
    tabs -- list of tab names
    """
    joined_args = "".join(args_order)
    if re.match(".*sw.*", joined_args) is not None:
        order = list(range(len(tabs.keys())))
        swap_idxs = list(map(int, joined_args.split("sw")))
        order[swap_idxs[0]] = swap_idxs[1]
        order[swap_idxs[1]] = swap_idxs[0]
    elif re.match(".*to.*", joined_args) is not None:
        order = list(range(len(tabs.keys())))
        insert_idxs = list(map(int, joined_args.split("to")))
        order.remove(insert_idxs[0])
        order.insert(insert_idxs[1], insert_idxs[0])
    else:
        order = list(map(int, args_order))
        if len(set(order)) == len(order) and \
                len(order) <= len(tabs.keys()) and \
                min(order) >= 0 and max(order) < len(tabs):
            # fill the rest of idxs if not all provided
            for i in range(len(tabs.keys())):
                if i not in order:
                    order.append(i)
        else:
            return None
    return order


def reordered_analysis(tabs, old_analysis, order):
    """Reorder the 'analysis' dict in scikick.yml.
    Returns the reordered 'analysis' dict which produces
    the differently ordered tab list in all pages
    tabs -- list of tab names
    old_analysis -- 'analysis' dict from scikick.yml
    order -- list of indices
    """
    new_analysis = ordereddict()
    for ord_no in order:
        for rmd in tabs[list(tabs.keys())[ord_no]]:
            norm_rmd = os.path.normpath(rmd)
            curr_key = list(filter(lambda x: \
                                       os.path.splitext(x)[0] == norm_rmd, \
                                   old_analysis.keys()))[0]
            new_analysis[curr_key] = old_analysis[curr_key]
    return new_analysis
