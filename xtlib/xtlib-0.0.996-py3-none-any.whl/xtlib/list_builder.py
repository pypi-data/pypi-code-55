# list_builder.py: builds the list shown in "list exper" cmd
import os
import json
import time
import arrow
import datetime
from fnmatch import fnmatch

from . import utils
from .azure_batch import AzureBatch

class ListBuilder():
    def __init__(self, config, store, client):
        self.config = config
        self.store = store
        self.client = client

        self.ws = self.config.get("general", "workspace")

        # all possible status values should be listed here
        
        # pre-run
        self.allocating = config.get("general", "allocating")
        self.queued = config.get("general", "queued")

        # running
        self.spawning = config.get("general", "spawning")
        self.running = config.get("general", "running")

        # ended
        self.completed = config.get("general", "completed")
        self.killed = config.get("general", "killed")
        self.aborted = config.get("general", "aborted")
        self.error = config.get("general", "error")
        self.unknown = config.get("general", "error")

        if config.get("general", "active"):
            self.queued = True
            self.spawning = True
            self.running = True
            self.allocating = True

        if config.get("general", "finished"):
            self.completed = True
            self.killed = True
            self.error = True
            self.aborted = True

        # if none of the status options were specified, set them all to True
        if not self.queued and not self.spawning and not self.running and not self.completed and not self.killed and not self.error \
                and not self.aborted:
            self.allocating = True
            self.queued = True
            self.spawning = True
            self.running = True
            self.completed = True
            self.killed = True
            self.error = True
            self.aborted = True
            self.unknown = True

    def filtering_active_only(self):
        return not(self.completed or self.killed or self.error or self.aborted)

    def get_requested_cols(self, request_list, avail_list):
        #print("request_list=", request_list)
        #print("avail_list=", avail_list)
        actual_cols = []
        
        for key in request_list:
            if key in avail_list:
                actual_cols.append(key)
        
        #print("actual_cols=", actual_cols)
        return actual_cols

    def sort_records(self, stat_records):
        sort_col = self.config.get("reports", "sort")
        #print("sort_name=", sort_name, ", sort_col=", sort_col)

        reverse = self.config.get("reports", "reverse")
        if sort_col == "name":
            # only want to sort "exper_name/run341" by the number at the end
            def get_name_key(r):
                name = r["name"]
                index = name.rfind("/run")
                if index == -1:
                    key = name[3:]
                else:
                    key = name[index+4:]

                # key is either an int (for parent records) or a int.int (for child)
                if "." in key:
                    parts = key.split(".")
                    key = 10000*int(parts[0]) + int(parts[1])
                else:   
                    key = 10000*int(key)
                return key

            stat_records.sort(key=get_name_key, reverse=reverse)
        else:
            # normal sort
            #print("sort_col=", sort_col)
            #print("stat_records=", stat_records)
            stat_records.sort(key=lambda r: r[sort_col], reverse=reverse)

    def get_exper_status_and_duration(self, log_records):
        duration = 0
        started = ""
        status = ""
        exit_code = None
        start_time = 0
        last_time = 0
        box_name = ""
        exper_name = ""

        if len(log_records) > 0:
            start_time = arrow.get(log_records[0]["time"])
            last_time = arrow.get(log_records[-1]["time"])

            start_dd = log_records[0]["data"]
            if "box_name" in start_dd:
                box_name = start_dd["box_name"]

            if "exper_name" in start_dd:
                exper_name = start_dd["exper_name"]

            end_records = [record for record in log_records if record["event"] == "ended"]
            if len(end_records) == 0:
                # was experiment terminated without an "ended" log record being written?
                since_start = utils.time_diff(arrow.now(), start_time)
                if duration >= 24*3600:   # no update for 24 hours
                    status = "timed-out"
                else:
                    start_records = [record for record in log_records if record["event"] in ["start", "started"]]
                    if len(start_records):
                        status = "running"
                    else:
                        status = "queued"
                        create_records = [record for record in log_records if record["event"] == "created"]
                        if len(create_records):
                            data = create_records[0]["data"]
                            if "repeat" in data and data["repeat"]:
                                status = "spawning"

                    last_time = arrow.now() 
            else:
                # we have the ENDED record - use it for status, elapsed
                end_record = end_records[-1]
                last_time = arrow.get(end_record["time"])
                status = self.safe_record_get("status", end_record, "")
                exit_code = self.safe_record_get("exit_code", end_record, "")

            duration = utils.time_diff(last_time, start_time)

        return exper_name, status, exit_code, duration, start_time, last_time, box_name

    def safe_record_get(self, name, record, default_value):
        value = default_value

        if "data" in record:
            data = record["data"]
            if name in data:
                value = data[name]

        return value

    def filtered_out(self, status):
        #print("status=", status)
        fo = not getattr(self, status)
        # if fo:
        #     print("filtered out status=", status)

        return fo

    def get_run_hyperparams_from_summary_records(self, run_records, run_name):
        hparams = {}

        if len(run_records) > 1:
            last_record = run_records[-1]
            if "hparams" in last_record:
                hparams = last_record["hparams"]

        return hparams

    def get_run_stats(self, ws, run_records, status_dict, log_records, run_name, merge_exper_name=True):
        metrics = {}
        first_record = run_records[0]
        last_record = None

        #print("run_name=", run_name, ", run_records=", run_records)

        if len(run_records) > 1:
            last_record = run_records[-1]
            if "metrics" in last_record:
                metrics = last_record["metrics"]

        if not metrics and log_records:
            rollup_specs = self.config.get("metrics", None)
            metrics = self.store.rollup_metrics_from_records(log_records, rollup_specs)

        restarts = None
        if last_record and "restarts" in last_record:
            restarts = last_record["restarts"]
            if restarts == 0:
                # hide the zeros
                restarts = None

        #exper_name, status, exit_code, duration, start_time, last_time, box_name = self.get_exper_status_and_duration(log_records)
        exper_name = first_record["exper_name"]
        app_name = first_record["app_name"]
        start_time = arrow.get(first_record["time"])
        box_name = first_record["box_name"]
        job = first_record["job_id"] if "job_id" in first_record else None
        #print("job=", job)
        pool = first_record["pool"] if "pool" in first_record else None
        description = first_record["description"] if "description" in first_record else None
        repeat = first_record["repeat"] if "repeat" in first_record else None
        workspace = ws
        from_host = first_record["from_computer_name"] if "from_computer_name" in first_record else None
        username = first_record["username"] if "username" in first_record else None
        path = first_record["path"] if "path" in first_record else None
        target = os.path.basename(path) if path else None
        
        status = last_record["status"] if last_record else status_dict[run_name]["status"]
        exit_code = last_record["exit_code"] if last_record else None
        last_time = arrow.get(last_record["time"]) if last_record else arrow.now()
        duration = utils.time_diff(last_time, start_time) 
        #print("status=", status, ", last_record=", last_record)

        if status and self.filtered_out(status):
            return None

        run_path = exper_name + "/" + run_name if exper_name and merge_exper_name else run_name
        #print("run_path=", run_path)

        sr = {}
        sr["name"] = run_path
        sr["app"] = app_name
        sr["status"] = status
        sr["exit-code"] = exit_code
        sr["started"] = start_time
        sr["ended"] = last_time
        sr["duration"] = duration
        sr["box"] = box_name
        sr["experiment"] = exper_name
        sr["path"] = path
        sr["target"] = target

        sr["job"] = job
        sr["pool"] = pool
        sr["description"] = description
        sr["repeat"] = repeat
        sr["workspace"] = workspace
        sr["from-host"] = from_host
        sr["username"] = username
        sr["restarts"] = restarts

        # sr["metric"] = metric_name
        # sr["score"] = value

        for name, value in metrics.items():
            #print("sr: name=", name, ", value=", value, ", type(value)=", type(value))
            sr[name] = value

        return sr

    def match_exper_wildcard(self, exper_dict, exper_wildcard):
        if not exper_wildcard:
            exper_wildcard = "*"
        exper_wildcard = exper_wildcard.lower()

        # match wildcard exper_name to all exper_names
        exper_names = []

        for en in exper_dict:
            enlow = en.lower()
            #print("comparing '" + enlow + "' to '" + exper_wildcard + "'")
            if fnmatch(enlow, exper_wildcard):
                exper_names.append(en)

        #print("exper_names=", exper_names)
        return exper_names

    def build_filtered_summary_records_by_run(self, ws_name, run_names, boxes_filter):
        started = time.time()
        records_by_run = {}
        status_dict = {}
        count = 0

        app_filter = self.config.get("general", "app")
        exper_filter = self.config.get("general", "experiment")
        job_filter = self.config.get("general", "job")
        utils.validate_job_name(job_filter)

        # read everything from the single summary file
        # if self.store.does_workspace_file_exist(ws_name, utils.WORKSPACE_SUMMARY):
        #     text = self.store.read_workspace_file(ws_name, utils.WORKSPACE_SUMMARY)
        #     utils.timing("build_filtered_summary_records_by_run: after read of WORKSPACE_SUMMARY")
        #     summary_records = utils.load_json_records(text)
        summary_records = self.store.get_run_summaries(ws_name)
        if summary_records:
            utils.timing("list_builder: summary record count=" + str(len(summary_records)))

            # gather run names to keep
            all_run_names = [sr["run_name"] for sr in summary_records]
            if run_names:
                # build keepers from run_names (some of which could be wildcards)
                keepers = set()
                for wild_name in run_names:
                    if "*" in wild_name:
                        names = [name for name in all_run_names if fnmatch(name, wild_name)]
                        keepers.update(names)
                    else:
                        keepers.add(wild_name)
            else:
                # use all run names
                keepers = set(all_run_names)
            
            #print("keepers #1=", keepers)
            #print("boxes_filter=", boxes_filter, ", ws_name=", ws_name)

            # apply filters: box names
            if boxes_filter:
                boxes_dict = {name:1 for name in boxes_filter}
                box_keeps = set([sr["run_name"] for sr in summary_records if "box_name" in sr and sr["box_name"] in boxes_dict])
                keepers = keepers.intersection(box_keeps)

            # apply filters: experiments
            if exper_filter:
                exper_filter = exper_filter.lower()
                exper_keeps = set([sr["run_name"] for sr in summary_records if "exper_name" in sr and sr["exper_name"].lower() == exper_filter])
                keepers = keepers.intersection(exper_keeps)

            # apply filters: app
            if app_filter:
                app_filter = app_filter.lower()
                app_keeps = set([sr["run_name"] for sr in summary_records if "app_name" in sr and sr["app_name"].lower() == app_filter])
                keepers = keepers.intersection(app_keeps)

            # apply filters: job_id
            if job_filter:
                job_filter = job_filter.lower()
                app_keeps = set([sr["run_name"] for sr in summary_records if "job_id" in sr and sr["job_id"].lower() == job_filter])
                keepers = keepers.intersection(app_keeps)

            # apply keeps to all records
            summary_records = [sr for sr in summary_records if sr["run_name"] in keepers]

            # organize runs records to be accessible by run_name
            run_names = set([sr["run_name"] for sr in summary_records])
            records_by_run = {name: [] for name in run_names}

            for sr in summary_records:
                run_name = sr["run_name"]
                records_by_run[run_name].append(sr)
        
            detect_and_repair = self.config.get("general", "repair")

            # find and repair phantom records
            status_dict = self.validate_unfinished_records(ws_name, records_by_run)

            if detect_and_repair:
                # repair phantom runs
                count = self.repair_phantom_runs(ws_name, status_dict)

        elapsed2 = time.time() - started
        #print("building of FILTERED summary records took: {:.1f} secs".format(elapsed2))

        #print("count=", count)
        return records_by_run, status_dict, count

    def repair_phantom_runs(self, ws_name, status_dict):
        #print("status_dict=", status_dict)

        metric_rollup_dict = self.config.get("metrics", None)
        count = 0
        dry_run = self.config.get("general", "dry-run")

        for run_name, dd in status_dict.items():
            status = dd["status"]
            aggregate_dest = self.config.get("hp-search", "aggregate-dest")

            if aggregate_dest == "experiment" and "exper_name" in dd:
                dest_name = dd["exper_name"]
            elif aggregate_dest == "job" and "job" in dd:
                dest_name = dd["job"]
            else:
                dest_name = None

            if status is None:
                if dry_run:
                    print("  (dry-run) repairing phantom run: {}".format(run_name))
                else:
                    print("  repairing phantom run: {}".format(run_name))
                    self.store.rollup_and_end_run(ws_name, run_name, aggregate_dest, dest_name, "aborted", None, \
                        metric_rollup_dict, use_last_end_time=True)
                    count += 1
        return count
                    
    def validate_unfinished_records(self, ws, records_by_run, ask_boxes_status=True):
        status_dict = {}
        unfinished_by_box = {}
        count = 0
        init_status = None   # if detect_and_repair else "running"  

        for key, records in records_by_run.items():
            #print("run=", key)

            if len(records) == 1:
                first_record = records[0]
                box_name = first_record["box_name"]
                run_name = first_record["run_name"]
                exper_name = first_record["exper_name"]
                #print("unfinished run=", run_name)

                if not box_name in unfinished_by_box:
                    unfinished_by_box[box_name] = []

                unfinished_by_box[box_name].append(run_name)
                status_dict[run_name] = {"status": init_status, "exper_name": exper_name}     # default
                count += 1

        if count and ask_boxes_status:
            # workaround for not being able to "import client" in this file (cyclic import)
            xt_client = self.client.create_new_client(self.config)

            #print("validating {} unfinished runs in workspace '{}'".format(count, ws))

            for box_name, run_names in unfinished_by_box.items():
                box_status_dict = self.get_run_status_from_box(xt_client, ws, box_name, run_names)

                if box_status_dict:
                    # add box_status_dict to status_dict
                    for key, value in box_status_dict.items():
                        status_dict[key]["status"] = value

        #print("status_dict=", status_dict)
        return status_dict

    def get_run_status_from_azure_box(self, box_name, run_names):
        box_status_dict = {}
        job_id = box_name.split("-")[0]

        job = AzureBatch(self.config)
        status = job.get_job_status(job_id)
        #print("job_id=", job_id, ", status=", status)

        for run_name in run_names:
            box_status_dict[run_name] = status

        return box_status_dict

    def get_run_status_from_box(self, xt_client, ws, box_name, run_names):
        box_status_dict = None
        try:
            if utils.is_azure_batch_box(box_name):
                box_status_dict = self.get_run_status_from_azure_box(box_name, run_names)
            else:
                if not utils.is_localhost(box_name) and not \
                    self.config.get("boxes", box_name, default_value=None, suppress_warning=True):
                        print("  skipping unknown box=", box_name)
                elif not xt_client.init_controller(box_name, launch_if_needed=False):
                    print("  skipping unreachable box=", box_name)
                else:
                    box_status_dict = xt_client.get_status_of_runs(ws, run_names)
        except Exception as ex:
            print("exception raised by box={}: {}".format(box_name, ex))
            if self.config.get("general", "raise"):
                raise ex   
        
        return box_status_dict

    def build_flat(self, ws, ws_runs=[], boxes_filter=None):
        
        utils.timing("build_flat: started")

        started = time.time()

        records_by_run, status_dict, count = self.build_filtered_summary_records_by_run(ws, ws_runs, boxes_filter)
        if count:
            # refresh info after repairing records
            records_by_run, status_dict, count = self.build_filtered_summary_records_by_run(ws, ws_runs, boxes_filter)

        utils.timing("build_flat: after build_filtered_summary_records_by_run")

        #print("ws_runs=", ws_runs)
        boxout = self.config.get("general", "boxout")
        lines = self.build_for_runs(records_by_run, status_dict, ws, "", False, boxout=boxout)

        elapsed = time.time() - started
        #print("building of list took: {:.1f} secs".format(elapsed))

        return lines
        
    def build_exper_summary(self, exper_wildcard=None, show_counts=False):
        exper_dict = self.store.get_all_runs_grouped_by_experiment(self.ws)
        lines = []
        #print("exper_wildcard=", exper_wildcard, ", exper_dict=", exper_dict)

        # print HEADERS
        if show_counts:
            lines.append(f'  {"EXPERIMENT":20.20s} {"RUNS":>8s}\n')

            # print VALUES for each record
            for name, run_list in exper_dict.items():
                exper_count = len(run_list) if run_list else 0
                if len(name) > 20:
                    name = name[0:18] + "..."
                lines.append(f'  {name:20.20s} {exper_count:>8d}')
        else:
            for name in exper_dict.keys():
                if (not exper_wildcard) or fnmatch(name, exper_wildcard):
                    lines.append(f'  {name:20.20s}')

        return lines

    def build_grouped(self, exper_wildcard=None, detail="cols"):
        # TODO ASAP - rewrite this code to use summary.log for all but status=running runs
        # and it will be SO MUCH FASTER

        # experimental - TEMP TEMP TEMP
        start = time.time()
        # if self.store.does_workspace_file_exist(self.ws, utils.WORKSPACE_SUMMARY):
        #     text = self.store.read_workspace_file(self.ws, utils.WORKSPACE_SUMMARY)
        #     records = utils.load_json_records(text)
        # else:
        #     records = []
        records = self.store.get_run_summaries(ws_name)

        #utils.print_elapsed(start, "load summary records: count=" + str(len(records)))

        start = time.time()
        exper_dict = self.store.get_all_runs_grouped_by_experiment(self.ws)
        #print("exper_dict=", exper_dict.keys())
        #utils.print_elapsed(start, "get all runs grouped")

        start = time.time()
        exper_names = self.match_exper_wildcard(exper_dict, exper_wildcard)
        #print("exper_names=", exper_names)
        #utils.print_elapsed(start, "match_exper_wildcard")

        start = time.time()
        exper_names.sort()
        #utils.print_elapsed(start, "sort")
        #print("exper_names=", exper_names)

        start = time.time()
        lines = []
        for exper_name in exper_names:
            lines.append(exper_name + ":")
            
            # underline exper_name
            lines.append("-"*(1+len(exper_name)))

            #print("self.ws=", self.ws)
            #run_names = self.store.get_true_run_names(self.ws, exper_name)
            runs = exper_dict[exper_name]
            run_names = map(lambda r: r["run_name"], runs)

            records_by_run, status_dict, count = self.build_filtered_summary_records_by_run(self.ws, ws_runs, boxes_filter)
            if count:
                # refresh info after repairing records
                records_by_run, status_dict, count = self.build_filtered_summary_records_by_run(self.ws, ws_runs, boxes_filter)

            lines += self.build_for_runs(records_by_run, status_dict, self.ws, "  ", False)
            lines.append("")

        return lines

    def get_run_num(self, sr):
        name = sr["name"][3:]    # skip over "run" prefix
        if "." in name:
            p, c = name.split(".")
            return int(p)*100000 + int(c)
        return int(name)*100000
            
    def build_for_runs(self, records_by_run, status_dict, ws, indent="", merge_exper_name=True, boxout=False):
        stat_records = []
        std_set = set()
        hp_set = set()
        #print("records_by_run=", records_by_run)

        start = time.time()
        run_names = records_by_run.keys()

        for run_name in run_names:
            try:
                run_records = records_by_run[run_name]
                log_records = None

                if len(run_records) == 1:
                    # active run, or unrepaired phantom run
                    # need to gather hparams and metrics from full set of run's log records
                    #print("getting run log for run_name=", run_name)
                    log_records = self.store.get_run_log(ws, run_name)
                
                start2 = time.time()
                stat_record = self.get_run_stats(ws, run_records, status_dict, log_records, run_name, merge_exper_name)

                # if filtered out by options, skip further processing
                if not stat_record:
                    continue

                start2 = time.time()

                if log_records:
                    hp_dict = self.store.gather_run_hyperparams(log_records)
                else:
                    hp_dict = self.get_run_hyperparams_from_summary_records(run_records, run_name)
                #utils.print_elapsed(start2, "get_run_hyperparams")

                # keep track of all avail STD and HP keys
                std_set = std_set.union(stat_record.keys())
                hp_set = hp_set.union(hp_dict.keys())

                stat_record =  {**hp_dict, **stat_record} 
                #print("MERGED sr=", stat_record)
                stat_records.append(stat_record)
            except BaseException as ex:
                print("while processing run={}, received exception={}".format(run_name, ex))
                if self.config.get("general", "raise"):
                    raise ex  
                
        if boxout:
            # allow only latest stat_record for each box
            box_dict = {}
            for sr in stat_records:
                box = sr["box"]
                if not box in box_dict:
                    # first entry always goes in
                    box_dict[box] = sr
                else:
                    # which is the most recent?
                    if self.get_run_num(sr) > self.get_run_num(box_dict[box]):
                        box_dict[box] = sr

            stat_records = list(box_dict.values())

        # early return if no runs found
        if not stat_records:
            return []

        self.sort_records(stat_records)

        #print("len(stat_records)=", len(stat_records))

        std_list = list(std_set)
        hp_list = list(hp_set)

        # combine available col lists
        avail_list = std_list + hp_list

        requested_list = self.config.get("reports", "report-cols")

        actual_cols = self.get_requested_cols(requested_list, avail_list)
        #print("actual_cols=", actual_cols)

        #self.old_generate_report(stat_records, avail_list, actual_cols)
        text = self.build_formatted_table(stat_records, avail_list, actual_cols)
        lines = text.split("\n")
        return lines

    def build_formatted_table(self, records, avail_cols, col_list=None):
        '''
        builds a nicely formatted text table from a set of records.

        'records' - a list of dict entries containing data to format
        'avail_cols' - list of columns (unique dict keys found in records)
        'actual_cols' - list of columns to be used for report (strict subset of 'avail_cols')
        '''

        max_col_width = int(self.config.get("reports", "max-width"))    
        float_precision = self.config.get("reports", "precision")
        uppercase_hdr_cols = self.config.get("reports", "uppercase-hdr")
        right_align_num_cols = self.config.get("reports", "right-align-numeric")
        truncate_with_ellipses = self.config.get("reports", "truncate-with-ellipses")

        if not col_list:
            col_list = avail_cols
        #print("col_list=", col_list)

        col_space = 2               # spacing between columns
        col_infos = []              # {width: xxx, value_type: int/float/str, is_numeric: true/false}

        # formatting strings with unspecified width and alignment
        float_fmt = "{:." + str(float_precision) + "f}"
        int_fmt = "{:d}"
        str_fmt = "{:s}"
        #print("float_fmt=", float_fmt)

        # build a col_info for each col 
        for i, col in enumerate(col_list):

            # examine all records for determining max col_widths
            col_width = len(col)
            #print("col=", col, ", col_width=", col_width)
            value_type = str
            is_numeric = False
            first_value = True

            for record in records:

                if not col in record:
                    # not all columns are defined in all records
                    continue

                value = record[col]

                # special formatting for time values
                if col == "duration":
                    value = str(datetime.timedelta(seconds=value))
                    index = value.find(".")
                    if index > -1:
                        value = value[:index]
                elif col in ["started", "ended"]:
                    value = value.format('YYYY-MM-DD @HH:mm:ss')

                if isinstance(value, float):
                    value_str = float_fmt.format(value)
                    if value_type == str:
                        value_type = float
                        is_numeric = True
                elif isinstance(value, int):
                    value_str = int_fmt.format(value)
                    if value_type == str:
                        value_type = int
                        is_numeric = True
                elif value is not None:
                    # don't let None values influence the type of field
                    # assume value found is string-like
                    value_str = str_fmt.format(value) if value else ""
                    if first_value:
                        is_numeric = utils.str_is_float(value)
                else:
                    value_str = ""

                col_width = max(col_width, len(value_str))
                #print("name=", record["name"], ", col=", col, ", value_str=", value_str, ", col_width=", col_width)

            # finish this col
            col_width = min(max_col_width, col_width)
            col_info = {"name": col, "col_width": col_width, "value_type": value_type, "is_numeric": is_numeric}
            col_infos.append(col_info)
            #print(col_info)

        # process headers
        text = ""
        first_col = True

        for col_info in col_infos:
            if first_col:
                first_col = False
            else:
                text += " " * col_space

            right_align = right_align_num_cols and col_info["is_numeric"]
            col_width = col_info["col_width"]
            col_name = col_info["name"].upper() if uppercase_hdr_cols else col_info["name"]

            if truncate_with_ellipses and len(col_name) > col_width:
                col_text = col_name[0:col_width-3] + "..."
            elif right_align:
                fmt = ":>{}.{}s".format(col_width, col_width)
                fmt = "{" + fmt + "}"
                col_text = fmt.format(col_name)
            else:
                fmt = ":<{}.{}s".format(col_width, col_width)
                fmt = "{" + fmt + "}"
                col_text = fmt.format(col_name)

            text += col_text

        text += "\n\n"

        # process value rows
        for record in records:
            first_col = True

            for col_info in col_infos:
                if first_col:
                    first_col = False
                else:
                    text += " " * col_space

                right_align = right_align_num_cols and col_info["is_numeric"]
                col_width = col_info["col_width"]
                col = col_info["name"]
                align = ">" if right_align else "<"

                if not col in record:
                    # not all records define all columns
                    str_fmt = "{:" + align + str(col_width)  + "." + str(col_width) + "s}"
                    text += str_fmt.format("")
                else:
                    value = record[col]

                    #print("col=", col, ", value=", value, ", type(value)=", type(value))

                    # special formatting for time values
                    if col == "duration":
                        value = str(datetime.timedelta(seconds=value))
                        index = value.find(".")
                        if index > -1:
                            value = value[:index]
                    elif col in ["started", "ended"]:
                        value = value.format('YYYY-MM-DD @HH:mm:ss')

                    if isinstance(value, float):
                        float_fmt = "{:" + align + str(col_width) + "." + str(float_precision) +"f}"
                        text += float_fmt.format(value)
                    elif isinstance(value, int):
                        int_fmt = "{:" + align + str(col_width) + "d}"
                        text += int_fmt.format(value)
                    else:
                        str_fmt = "{:" + align + str(col_width)  + "." + str(col_width) + "s}"
                        value = value if value else ""
                        text += str_fmt.format(value)
            text += "\n"

        # all records processed
        return text

