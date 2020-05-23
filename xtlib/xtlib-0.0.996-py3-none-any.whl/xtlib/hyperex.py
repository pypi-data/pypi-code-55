import os
import json
import numpy as np
import arrow
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons

import xtlib.helpers
from xtlib import utils
from xtlib.helpers.xt_config import XTConfig
from xtlib.store import Store

# for now, these parameters to HyperparameterExplorer() are implemented as globals
XTLIB_WORKSPACE = None  
XTLIB_DEST_NAME = None 
SCORE_NAME = None
SCORE_ROLLUP = None

DOWNLOAD_RUNS_AND_CONFIG = True
STD_ERR = 0
STD_DEV = 1
SEPARATE = 2
PLOT_STYLE_LABELS = ['Standard error', 'Standard deviation', 'Separate runs']

MAX_NUM_RUNS = 0  # For throttling.
fig = None   # global

class PerformanceChart(object):
    def __init__(self, explorer, num_reports_per_run):
        self.explorer = explorer
        self.num_reports_per_run = num_reports_per_run
        self.perf_axes = fig.add_axes([0.54, 0.05, 0.44, 0.92])
        self.prev_curve = None
        self.plot_from_runs()

    def plot_from_runs(self):
        self.perf_axes.clear()

        if XTLIB_DEST_NAME.startswith("job"):
            self.perf_axes.set_title("Workspace={}  Job={}".format(XTLIB_WORKSPACE, XTLIB_DEST_NAME), fontsize=16)
        else:
            self.perf_axes.set_title("Workspace={}  Experiment={}".format(XTLIB_WORKSPACE, XTLIB_DEST_NAME), fontsize=16)

        self.perf_axes.set_xlabel("Time steps", fontsize=16)
        self.perf_axes.set_ylabel("Mean {} over recent steps".format(SCORE_NAME), fontsize=16)
        self.perf_axes.set_xlim(self.explorer.plot_min_x, self.explorer.plot_max_x)
        self.perf_axes.set_ylim(self.explorer.plot_min_score, self.explorer.plot_max_score)
        # Count how many runs to include after filtering.
        runs = self.explorer.runs
        num_runs = 0
        for run in runs:
            if run.include:
                num_runs += 1
        # Gather the data into a numpy array.
        d = np.zeros((self.num_reports_per_run, num_runs))
        run_i = 0
        for run in runs:
            if run.include:
                #for i in range(self.num_reports_per_run):
                for i in range(len(run.metric_reports)):  
                    d[i, run_i] = run.metric_reports[i].score
                run_i += 1

        # Gather the steps for the x axis.
        steps = np.zeros((self.num_reports_per_run))
        #for i in range(self.num_reports_per_run):
        run0 = runs[0]
        for i in range(len(run0.metric_reports)):   
            steps[i] = run0.metric_reports[i].steps

        if (self.explorer.plot_style == STD_DEV) or (self.explorer.plot_style == STD_ERR):
            # Display means with error bars.
            means = np.zeros((self.num_reports_per_run))
            std_errs = np.zeros((self.num_reports_per_run))
            #for i in range(self.num_reports_per_run):
            for i in range(len(run.metric_reports)):   
                scores = d[i,:]
                means[i] = np.mean(scores)
                if self.explorer.plot_style == STD_DEV:
                    std_errs[i] = np.sqrt(np.var(scores, ddof=1))
                elif self.explorer.plot_style == STD_ERR:
                    std_errs[i] = np.sqrt(np.var(scores, ddof=1) / num_runs)
            ymin = means - std_errs
            ymax = means + std_errs
            curve = PerfCurve(steps, means, ymin, ymax, num_runs)
            # Plot the curves.
            self.plot_error(curve, 'blue')
            self.plot_curve(curve, 'blue', 'Current set')
            if self.prev_curve:
                self.plot_error(self.prev_curve, 'red')
                self.plot_curve(self.prev_curve, 'red', 'Previous set')
            self.perf_axes.legend(loc='lower left', prop={'size': 16})
            self.prev_curve = curve
            # Dump.
            # for i in range(self.num_reports_per_run):
            #     print(means[i])
        else:
            # Display the runs separately.
            run_i = 0
            for run in runs:
                if run.include:
                    scores = d[:,run_i]
                    curve = PerfCurve(steps, scores, 0, 0, 1)
                    self.plot_curve(curve, 'blue', '')
                    run_i += 1

    def plot_error(self, curve, color):
        self.perf_axes.fill_between(curve.steps, curve.ymax, curve.ymin, color=color, alpha=0.2)

    def plot_curve(self, curve, color, label):
        self.perf_axes.plot(curve.steps, curve.means, label=(label + "  ({} runs)".format(curve.num_runs)), color=color)


class PerfCurve(object):
    def __init__(self, steps, means, ymin, ymax, num_runs):
        self.steps = steps
        self.means = means
        self.ymin = ymin
        self.ymax = ymax
        self.num_runs = num_runs


class Histogram(object):
    def __init__(self, explorer, id, num_ids):
        self.explorer = explorer
        self.id = id
        self.num_ids = num_ids
        self.axes = None
        self.values = []
        self.y_button_height = 0.018
        self.setting = None  # Always None for global hist. Changes for setting hists.

    def add_axes(self, axes_to_share):
        bottom_client_margin = 0.02  # So there's room at the bottom for a histogram title.
        top_hist_margin = 0.04  # To separate the histograms a bit.
        self.width = 0.25
        self.height = 1. / self.num_ids
        self.left_bound = 0.25
        self.bottom = bottom_client_margin + (self.num_ids - self.id - 1) * self.height
        self.height -= top_hist_margin

        if axes_to_share:
            self.axes = fig.add_axes([self.left_bound, self.bottom, self.width, self.height], sharex=axes_to_share)
        else:
            self.axes = fig.add_axes([self.left_bound, self.bottom, self.width, self.height])
        if self.id > 0:
            self.axes.get_xaxis().set_visible(False)
            self.axes.spines["right"].set_visible(False)
            self.axes.spines["top"].set_visible(False)
            self.init_button()
            self.set_visible(False)
        return self.axes

    def init_button(self):
        x_left_bound = self.left_bound
        x_width = self.width
        y_top = self.bottom
        self.button_axes = plt.axes([x_left_bound, y_top - self.y_button_height, x_width, self.y_button_height])
        self.button = Button(self.button_axes, "some text")
        self.button.label.set_fontsize(12)
        self.button.on_clicked(self.on_click)

    def set_visible(self, visible):
        #self.axes.get_xaxis().set_visible(visible)
        self.axes.get_yaxis().set_visible(visible)
        self.axes.spines["left"].set_visible(visible)
        self.axes.spines["bottom"].set_visible(visible)
        self.button_axes.set_visible(visible)

    def update(self):
        self.axes.clear()
        self.values = []
        if self.id == 0:
            # The global histogram.
            for run in self.explorer.runs:
                if run.include:
                    overall_score = run.overall_score
                    self.values.append(overall_score)
        else:
            # A per-setting histogram.
            hparam = self.explorer.current_hparam
            if hparam != None:
                num_settings = len(hparam.settings)
                if self.id <= num_settings:
                    self.setting = hparam.settings[self.id - 1]
                    self.set_visible(True)
                    if self.setting.include:
                        for run in self.explorer.runs:
                            if run.include and self.setting.hparam.name in run.hparams:
                                if run.hparams[self.setting.hparam.name] == self.setting.value:
                                    overall_score = run.overall_score
                                    self.values.append(overall_score)
                        self.button.label.set_text("{}  ({} runs)".format(self.setting.value, len(self.values)))
                        self.axes.set_facecolor('1.0')
                        self.axes.get_yaxis().set_visible(True)
                    else:
                        # This setting is excluded. Show any runs that would be included if this setting were toggled.
                        for run in self.explorer.runs:
                            if run.num_settings_that_exclude_this == 1:
                                if run.hparams[self.setting.hparam.name] == self.setting.value:
                                    overall_score = run.overall_score
                                    self.values.append(overall_score)
                        self.button.label.set_text("{}  ({} runs, excluded)".format(self.setting.value, len(self.values)))
                        self.axes.set_facecolor('0.9')
                        self.axes.get_yaxis().set_visible(False)
                else:
                    # This histogram is not currently mapped to a setting.
                    self.axes.set_facecolor('1.0')
                    self.set_visible(False)
        if self.id == 0:
            color = 'b'
            rollup = SCORE_ROLLUP["roll-up"]

            if rollup == "mean":
                self.axes.set_xlabel("Mean {} over all steps".format(SCORE_NAME), fontsize=14)
            elif rollup == "min":
                self.axes.set_xlabel("Min {}".format(SCORE_NAME), fontsize=14)
            elif rollup == "max":
                self.axes.set_xlabel("Max {}".format(SCORE_NAME), fontsize=14)
            else:    # if  rollup == "last":
                self.axes.set_xlabel("Last {}".format(SCORE_NAME), fontsize=14)

            self.axes.set_ylabel("Runs in set", fontsize=14)
        else:
            color = 'g'

        # set HIST properties    
        #self.axes.hist(self.values, bins=20, facecolor=color, alpha=1.0, edgecolor='black')

        global_range = (self.explorer.plot_min_score, self.explorer.plot_max_score)

        edgecolor = 'black' if self.values else None
        self.axes.hist(self.values, bins=50, range=global_range, facecolor=color, edgecolor=edgecolor)
        #self.axes.set_xlim(0, 1)


    def on_click(self, event):
        self.setting.include = not self.setting.include
        self.explorer.update_runs()


class MetricReport(object):
    def __init__(self, json_line, index, start_time):
        metric_dict = json_line["data"]

        if "sec" in metric_dict:
            self.time = float(metric_dict["sec"])
        else:
            self.time = arrow.get(json_line["time"]).utcnow().timestamp - start_time

        if "steps" in metric_dict:
            self.steps = int(metric_dict["steps"])
        else:
            self.steps = index

        self.score = float(metric_dict[SCORE_NAME])

class Run(object):
    def __init__(self, nested_record):
        self.hparams = {}
        self.settings = []
        self.include = True
        self.num_settings_that_exclude_this = 0
        self.reset_metrics()
        # line = file_path  # Fix the name.
        # json_line = json.loads(line)
        event_dict_list = nested_record['log']
        self.name = nested_record["run_name"]

        start_time = 0

        for event_dict in event_dict_list:
            event = event_dict["event"]
            if event == "started":
                start_time = arrow.get(event_dict["time"]).utcnow().timestamp
            elif event == "hparams":
                hparam_dict = event_dict["data"]
                for key in hparam_dict:
                    self.hparams[key] = hparam_dict[key]
            elif event == "metrics":
                self.add_metric_report(event_dict, start_time)
        self.rollup_score()

    def reset_metrics(self):
        self.metric_reports = []
        self.overall_score = 0.

    def add_metric_report(self, json_line, start_time):
        metric_report = MetricReport(json_line, len(self.metric_reports), start_time)
        self.metric_reports.append(metric_report)
        self.overall_score += metric_report.score

    def rollup_score(self):
        num_reports = len(self.metric_reports)
        if num_reports > 0:
            if SCORE_ROLLUP == "mean":
                self.overall_score /= num_reports
            elif SCORE_ROLLUP == "min":
                scores = [mr.score for mr in self.metric_reports]
                self.overall_score = min(scores)
            elif SCORE_ROLLUP == "max":
                scores = [mr.score for mr in self.metric_reports]
                self.overall_score = max(scores)
            else:       # last
                self.overall_score = self.metric_reports[-1].score
            
    def update_inclusion(self):
        self.include = True
        self.num_settings_that_exclude_this = 0
        for setting in self.settings:
            if not setting.include:
                self.include = False
                self.num_settings_that_exclude_this += 1
        return


class HyperparameterSetting(object):
    def __init__(self, explorer, hparam, id, value, include):
        self.explorer = explorer
        self.hparam = hparam
        self.id = id
        self.value = value
        self.include = include


class Hyperparameter(object):
    def __init__(self, explorer, group, name):
        self.explorer = explorer
        self.group = group
        self.name = name
        self.id = -1
        self.value_setting_dict = {}
        self.settings = []
        self.display = False

    def add_setting(self, setting_value, include):
        if setting_value not in self.value_setting_dict.keys():
            setting = HyperparameterSetting(self.explorer, self, 0, setting_value, include)
            self.value_setting_dict[setting_value] = setting
        setting = self.value_setting_dict[setting_value]
        return setting

    def init_button(self):
        x_left_bound = 0.015
        x_width = 0.2
        y_top_bound = 0.08
        y_spacing = 0.06
        y_button_height = 0.04
        self.button_axes = plt.axes([x_left_bound, 1.0 - y_top_bound - self.id * y_spacing, x_width, y_button_height])
        self.button = Button(self.button_axes, self.name)
        self.button.label.set_fontsize(18)
        self.button.on_clicked(self.on_click)

    def on_click(self, event):
        if self.explorer.current_hparam != self:
            self.explorer.set_current_hparam(self)
            self.explorer.update_histograms()
            fig.canvas.draw()


class HyperparameterGroup(object):
    def __init__(self, explorer, title):
        self.explorer = explorer
        self.title = title
        self.hparams = []
        self.display = False

    def add_hparam(self, hparam):
        self.hparams.append(hparam)


class HyperparameterExplorer(object):
    def __init__(self, ws, hx_metric, score_rollup, cache_dir, aggregate_dest, dest_name, fn_hp_config):

        # TODO: remove these globals
        global XTLIB_WORKSPACE, XTLIB_DEST_NAME, SCORE_NAME, SCORE_ROLLUP, fig

        XTLIB_WORKSPACE = ws
        XTLIB_DEST_NAME = dest_name
        SCORE_NAME = hx_metric
        SCORE_ROLLUP = score_rollup

        fig = plt.figure(figsize=(20,12))
        fig.canvas.set_window_title('Hyperparameter Explorer')

        #print("ws=", ws, ", dest_name=", dest_name, ", hx_metric=", hx_metric)
        
        self.left_pane_axes = fig.add_axes([0.0, 0.0, 1.0, 1.0])
        self.left_pane_axes.get_xaxis().set_visible(False)
        self.left_pane_axes.get_yaxis().set_visible(False)
        self.left_pane_axes.spines["left"].set_visible(False)
        self.left_pane_axes.spines["right"].set_visible(False)
        self.left_pane_axes.spines["top"].set_visible(False)
        self.left_pane_axes.spines["bottom"].set_visible(False)

        self.plot_style = STD_ERR
        self.radio_buttons_axes = fig.add_axes([0.86, 0.07, 0.11, 0.1])
        self.radio_buttons = RadioButtons(self.radio_buttons_axes, (PLOT_STYLE_LABELS[0], PLOT_STYLE_LABELS[1], PLOT_STYLE_LABELS[2]))
        self.radio_buttons_axes.set_zorder(20)
        self.radio_buttons.on_clicked(self.radio_buttons_on_clicked)

        self.set_current_hparam(None)
        self.fn_hp_config = fn_hp_config

        # Connect to XT.
        self.xtstore = Store(config=XTConfig())
        self.ws_name = XTLIB_WORKSPACE

        #config_file_text = self.xtstore.read_experiment_file(self.ws_name, self.exper_name, "config.txt")

        # Download the all_runs file
        local_cache_path = "{}/{}/{}/".format(cache_dir, self.ws_name, dest_name)
        config_file_path = "{}{}".format(local_cache_path, "config.txt")
        all_runs_file_path = "{}{}".format(local_cache_path, "all_runs.txt")
        if DOWNLOAD_RUNS_AND_CONFIG:

            if aggregate_dest == "experiment":
                print("downloading runs for EXPERIMENT={}...".format(dest_name))
                # files are at EXPERIMENT LEVEL
                # read SWEEPS file
                if not self.xtstore.does_experiment_file_exist(self.ws_name, dest_name, self.fn_hp_config):
                    utils.user_error("missing experiment hp_config file (ws={}, exper={}, fn={})".format(self.ws_name, 
                        dest_name, self.fn_hp_config))
                self.xtstore.download_file_from_experiment(self.ws_name, dest_name, self.fn_hp_config, config_file_path)

                # read ALLRUNS info aggregated in EXPERIMENT
                # if not self.xtstore.does_experiment_file_exist(self.ws_name, dest_name, utils.ALL_RUNS_FN):
                #     utils.user_error("missing experiment SUMMARY file (ws={}, exper={}, fn={})".format(
                #         self.ws_name, dest_name, utils.ALL_RUNS_FN))
                # self.xtstore.download_file_from_experiment(self.ws_name, dest_name, utils.ALL_RUNS_FN, all_runs_file_path)
                allrun_records = self.xtstore.get_all_runs(aggregate_dest, self.ws_name, dest_name)
            else:  
                print("downloading runs for JOB={}...".format(dest_name))
                # files are at JOB LEVEL
                # read SWEEPS file
                if not self.xtstore.does_job_file_exist(dest_name, self.fn_hp_config):
                    utils.user_error("missing job hp_config file (job={}, fn={})".format(dest_name, self.fn_hp_config))
                self.xtstore.download_file_from_job(dest_name, self.fn_hp_config, config_file_path)

                # read ALLRUNS info aggregated in JOB
                # if not self.xtstore.does_job_file_exist(dest_name, utils.ALL_RUNS_FN):
                #     utils.user_error("missing job SUMMARY file (job={}, fn={})".format(dest_name, utils.ALL_RUNS_FN))
                # self.xtstore.download_file_from_job(dest_name, utils.ALL_RUNS_FN, all_runs_file_path)
                allrun_records = self.xtstore.get_all_runs(aggregate_dest, self.ws_name, dest_name)

            utils.timing("after downloading all runs")

        print("analyzing data...")
        # Read and process the data.
        self.read_config_file(config_file_path)  # Get the superset of hparam definitions.
        num_reports_per_run = self.load_runs_from_records(allrun_records)  # Populate the run objects with some data.
        #print("num_reports_per_run=", num_reports_per_run)
        
        self.get_plot_bounds_from_runs()
        self.populate_hparams()
        for run in self.runs:
            run.update_inclusion()  # This takes into consideration any non-included settings.
        self.assemble_left_pane()
        self.create_hparam_border()

        # Create a fixed set of histogram objects to be reused for all settings.
        # The first (top) histogram is the aggregate for all settings (in the focus).
        self.hists = []
        for i in range(self.max_settings_per_hparam + 1):
            self.hists.append(Histogram(self, i, self.max_settings_per_hparam + 1))

        # Add the histogram axes in reverse order, to get the right z-order.
        axes_to_share = self.hists[self.max_settings_per_hparam].add_axes(None)
        for i in range(self.max_settings_per_hparam):
            self.hists[self.max_settings_per_hparam - i - 1].add_axes(axes_to_share)

        if len(self.runs):
            # Populate histograms.
            self.update_histograms()

            # Create the perf chart.
            self.perf = PerformanceChart(self, num_reports_per_run)

        utils.timing("after load runs into memory")

    def radio_buttons_on_clicked(self, label):
        if label == PLOT_STYLE_LABELS[self.plot_style]:
            return
        if label == PLOT_STYLE_LABELS[0]:
            self.plot_style = 0
        elif label == PLOT_STYLE_LABELS[1]:
            self.plot_style = 1
        elif label == PLOT_STYLE_LABELS[2]:
            self.plot_style = 2
        self.perf.prev_curve = None
        self.perf.plot_from_runs()
        fig.canvas.draw()

    def draw(self):
        self.hist.draw()

    def create_hparam_border(self):
        if len(self.hparams) > 0:
            if len(self.displayed_hparams) > 0:
                rect = self.displayed_hparams[0].button_axes.get_position()
                xm = 0.004
                ym = 0.006
                x = rect.x0 - xm
                y = 2.0
                w = (rect.x1 - rect.x0) + 2*xm
                h = (rect.y1 - rect.y0) + 2*ym
                rect = patches.Rectangle((x, y), w, h, linewidth=4, edgecolor='g', facecolor='none')
                self.hparam_border = self.left_pane_axes.add_patch(rect)

    def set_current_hparam(self, hparam):
        self.current_hparam = hparam
        if hparam != None:
            rect = hparam.button_axes.get_position()
            xm = 0.004
            ym = 0.006
            x = rect.x0 - xm
            y = rect.y0 - ym
            self.hparam_border.set_xy([x, y])

    def run(self):
        if len(self.runs) == 0:
            print("error - no valid runs found")
        else:
            plt.show()

    def read_config_file(self, config_file_path):
        self.hparams = {}
        self.hparam_groups = []
        # config_file_text = self.xtstore.read_experiment_file(self.ws_name, self.exper_name, "config.txt")
        with open(config_file_path, 'r') as file:
            config_file_text = file.read()
        line_num = 0
        group = None
        lines = config_file_text.split('\n')
        for line in lines:
            line_num += 1
            if (len(line) == 0) or (line[0] == '#'):
                if (len(line) > 0):
                    group = HyperparameterGroup(self, line[2:])
                    self.hparam_groups.append(group)
                continue
            halves = line.split('=')
            name_string, value_string = halves[0].strip(), halves[1].strip()
            if value_string == 'randint':
                continue  # Ignore the seed parameters.
            hparam = Hyperparameter(self, group, name_string)
            if '#' in value_string:
                value_string = value_string[:value_string.index('#')].strip()
            values = value_string.split(',')
            for value in values:
                hparam.add_setting(self.cast_value(value.strip()), True)
            self.hparams[name_string] = hparam
            group.add_hparam(hparam)

    def cast_value(self, value_str):
        if value_str == 'True':
            new_value = True
        elif value_str == 'False':
            new_value = False
        else:
            try:
                new_value = int(value_str)
            except ValueError:
                try:
                    new_value = float(value_str)
                except ValueError:
                    new_value = value_str
        return new_value

    def load_runs_from_records(self, allrun_records):
        self.runs = []
        num_reports_per_run = None
        #for line in open(all_runs_path, 'r'):
        for record in allrun_records:
            # Process one run.log
            run = Run(record)

            if len(run.hparams) == 0:
                # skip over parent runs
                #print("skipping run with no hparams: ", run.name)
                continue

            if len(run.metric_reports) == 0:
                # skip over runs that generated no metrics (something is wrong, so warn user)
                print("WARNING - skipping run with no metrics: ", run.name)
                continue

            #print("run.hparams=", run.hparams)

            if num_reports_per_run is None:
                num_reports_per_run = len(run.metric_reports)  
            else:
                num_reports_per_run = max(num_reports_per_run, len(run.metric_reports))
            # else:
            #     if (num_reports_per_run != len(run.metric_reports)):
            #         continue  # Discard this incomplete run.
            self.runs.append(run)
            if MAX_NUM_RUNS > 0:
                if len(self.runs) == MAX_NUM_RUNS:
                    break
        # print("num runs processed = {}".format(len(self.runs)))
        return num_reports_per_run

    def get_plot_bounds_from_runs(self):
        self.plot_min_x = 1000000000
        self.plot_max_x = -1000000000

        if SCORE_ROLLUP and "bounds" in SCORE_ROLLUP:
            bounds = SCORE_ROLLUP["bounds"]
            self.plot_min_score = bounds[0]
            self.plot_max_score = bounds[1]
        else:
            self.plot_min_score = 1000000000
            self.plot_max_score = -1000000000

        for run in self.runs:
            for report in run.metric_reports:
                x = report.steps
                if x > self.plot_max_x:
                    self.plot_max_x = x
                if x < self.plot_min_x:
                    self.plot_min_x = x
                y = report.score
                if y > self.plot_max_score:
                    self.plot_max_score = y
                if y < self.plot_min_score:
                    self.plot_min_score = y

    def populate_hparams(self):
        # Connect up the runs and hparams.
        for run in self.runs:
            for hparam_name in run.hparams.keys():  # Only hparams that were read by the code,
                if hparam_name in self.hparams.keys():  # and were listed in config.txt.
                    hparam = self.hparams[hparam_name]
                    setting_value = run.hparams[hparam_name]
                    setting = hparam.add_setting(setting_value, False)
                    run.settings.append(setting)
        # Decide which hparams to display in the left pane.
        for hparam_name, hparam in self.hparams.items():
            if len(hparam.value_setting_dict) > 1:
                hparam.display = True
                hparam.group.display = True
                setting_values = []
                for setting in hparam.value_setting_dict.values():
                    setting_values.append(setting.value)
                    #print("setting.value=", setting.value, ", type(setting.value)=", type(setting.value))

                # Sort the settings, to determine their display order in the middle pane.
                setting_values.sort()
                for val in setting_values:
                    hparam.settings.append(hparam.value_setting_dict[val])

    def assemble_left_pane(self):
        self.max_settings_per_hparam = 0
        id = 0
        self.displayed_hparams = []
        for group in self.hparam_groups:
            if group.display:
                # print("\n# {}".format(group.title))
                for hparam in group.hparams:
                    if hparam.display:
                        self.displayed_hparams.append(hparam)
                        num_settings = len(hparam.settings)
                        if num_settings > self.max_settings_per_hparam:
                            self.max_settings_per_hparam = num_settings
                        hparam.id = id
                        id += 1
                        hparam.init_button()
                        # print("  {}".format(hparam.name))
                        # for setting in hparam.settings:
                        #     print("    {}".format(setting.value))
        self.num_settings_to_display = self.max_settings_per_hparam

    def update_histograms(self):
        for hist in self.hists:
            hist.update()
        self.hists[0].axes.set_xlim(self.plot_min_score, self.plot_max_score)

    def update_runs(self):
        for run in self.runs:
            run.update_inclusion()
        self.update_histograms()
        self.perf.plot_from_runs()
        fig.canvas.draw()

#hx = HyperparameterExplorer()
#hx.run()



