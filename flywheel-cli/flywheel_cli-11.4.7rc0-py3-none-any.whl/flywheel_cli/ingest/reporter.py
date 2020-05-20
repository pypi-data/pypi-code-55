"""Ingest progress reporter"""
import datetime
import logging
import os
import stat
import sys
import threading
import time

import crayons
import fs
import tzlocal

from .. import config as root_config
from .. import util
from .client.abstract import Client
from .container_tree import ContainerTree
from .config import ReporterConfig
from . import schemas as T

log = logging.getLogger(__name__)


class TerminalSpinnerThread:
    """Thread for terminal spinner"""

    def __init__(self, message, fh=sys.stdout):
        self._thread = None
        self._shutdown_event = threading.Event()
        self._fh = fh
        self.mode = os.fstat(sys.stdout.fileno()).st_mode
        self.message = message

    def start(self):
        """Start terminal spinner"""
        if not stat.S_ISREG(self.mode) and not self.is_running:
            log.debug("Starting terminal spinner reporter...")
            self._thread = threading.Thread(target=self.run, name="terminal-spinner-thread")
            self._thread.daemon = True
            self._thread.start()

    def run(self):
        """Run terminal spinner"""
        spinner = ["[   ]", "[=  ]", "[== ]", "[===]", "[ ==]", "[  =]", "[   ]"]
        counter = 0
        while self.is_running:
            current_spin = str(crayons.magenta(spinner[counter]))
            message = str(crayons.blue(self.message, bold=True))
            self.print(current_spin + " " + message + "\r")
            counter = (counter + 1) % len(spinner)
            if counter == 0:
                spinner.reverse()

            time.sleep(0.2)

    def stop(self, message):
        """Stop terminal spinner"""
        if self.is_running:
            self._shutdown_event.set()
            self._thread.join()
            self.print("")
            formatted_msg = str(crayons.blue(message, bold=True))
            self.print(f"\033[K{formatted_msg}\n")

    @property
    def is_running(self):
        """Spinner running status"""
        if self._thread is None or self._shutdown_event.is_set():
            return False
        return True

    def print(self, msg):
        """Print"""
        self._fh.write(msg)
        self._fh.flush()


class Reporter:
    """Ingest progress reporter"""

    def __init__(self, client: Client, config: ReporterConfig):
        self._fh = sys.stdout
        self.client = client
        self.config = config
        self.mode = os.fstat(sys.stdout.fileno()).st_mode
        self.last_reported_status_idx = -1

    def run(self):
        """Report progress"""
        ingest = self.client.ingest
        while not T.IngestStatus.is_terminal(ingest.status):
            prev_status_idx = self.last_reported_status_idx
            self.print_status_history(ingest.history)
            if self.last_reported_status_idx == prev_status_idx:
                # take a nap if status did not change (reduce db overhead)
                time.sleep(self.config.refresh_interval)
            ingest = self.client.ingest

        self.final_report()

    def final_report(self):
        """Print final report"""
        ingest = self.client.ingest
        self.print_status_history(ingest.history, final=True)
        self.print_final_report()
        log.debug("Ingest done, collecting logs...")
        self.save_reports()
        if ingest.status == T.IngestStatus.finished and not self.client.report.errors:
            sys.exit(0)
        else:
            sys.exit(1)

    def print_status_history(self, history, final=False):
        """Print report of every status since previous status"""
        for idx, status in enumerate(history):
            if self.last_reported_status_idx >= idx:
                continue
            st_name, timestamp = status
            timestamp = datetime.datetime.fromtimestamp(timestamp, tz=tzlocal.get_localzone())
            self.print_status_header(st_name, timestamp)
            follow_method = getattr(self, f"follow_{st_name}_status", None)
            # do not follow if its a final report to avoid stuck in a reporting cycle
            if follow_method:
                follow_method(final)
            self.print("")  # start new line
            self.last_reported_status_idx = idx

    def follow_scanning_status(self, final=False):
        """Follow scanning status"""
        while not final and self.client.ingest.status == T.IngestStatus.scanning:
            self.print_scan_progress()
            time.sleep(self.config.refresh_interval)
        self.print_scan_progress()
        self.print("")  # start new line

    def print_scan_progress(self):
        """Print scan progress"""
        progress = self.client.progress
        size = fs.filesize.traditional(progress.bytes.total)
        file_str = "files" if progress.files.total > 1 else "file"
        finished_scan = progress.scans.finished
        total_scan = progress.scans.total
        msg = f"{finished_scan} / {total_scan}, {progress.files.total} {file_str}, {size}"
        self.print(msg, replace=True)

    def follow_resolving_status(self, final=False):
        """Show resolve progress"""
        spinner = TerminalSpinnerThread("Resolving containers", fh=self._fh)
        spinner.start()
        while not final and self.client.ingest.status == T.IngestStatus.resolving:
            time.sleep(self.config.refresh_interval)
        spinner.stop("Resolved containers")

    def follow_detecting_duplicates_status(self, final=False):
        """Show detecting duplicates progress"""
        while not final and self.client.ingest.status == T.IngestStatus.detecting_duplicates:
            progress = self.client.progress.stages.detecting_duplicates
            if progress.total:
                self.print(f"{round(progress.completed/progress.total*100, 2)}%", replace=True)
            time.sleep(self.config.refresh_interval)
        progress = self.client.progress.stages.detecting_duplicates
        if progress.total:
            self.print(f"{round(progress.completed/progress.total*100, 2)}%", replace=True)
        self.print("")

    def follow_in_review_status(self, final=False):
        """Print summary report of review stage"""
        if self.config.verbose:
            self.print("Hierarchy sample:\n")
            container_factory = ContainerTree()
            for container in self.client.tree:
                container_factory.add_node(
                    container.id,
                    container.parent_id,
                    container.level,
                    src_context=container.src_context,
                    dst_context=container.dst_context,
                    bytes_sum=container.bytes_sum,
                    files_cnt=container.files_cnt,
                )
            container_factory.print_tree(fh=self._fh)

        self.print("Summary:")
        summary = self.client.summary
        for k, v in summary.dict().items():
            if k == "errors":
                continue
            self.print(f"  {k.capitalize()}: {v}")

        if summary.errors:
            self.print(f"\nErrors summary:")
            for error in summary.errors:
                self.print(f"  {error.message} ({error.code}): {error.count}")
        if final or self.client.ingest.status != T.IngestStatus.in_review:
            # do not prompt if status is not in_review
            return
        if self.config.assume_yes or util.confirmation_prompt("Confirm upload?"):
            self.client.review()
        else:
            self.client.abort()

    def follow_preparing_status(self, final=False):
        """Show preparing progress"""
        spinner = TerminalSpinnerThread("Preparing for ingest", fh=self._fh)
        spinner.start()
        while not final and self.client.ingest.status == T.IngestStatus.preparing:
            time.sleep(self.config.refresh_interval)
        spinner.stop("Preparing complete")

    def follow_uploading_status(self, final=False):
        """Print report of uploading stage"""
        prev_eta = {}
        ingest = self.client.ingest
        while not final and ingest.status == T.IngestStatus.uploading:
            progress = self.client.progress
            self.print_upload_progress(progress, ingest, prev_eta)
            time.sleep(self.config.refresh_interval)
            ingest = self.client.ingest

        progress = self.client.progress
        ingest = self.client.ingest
        self.print_upload_progress(progress, ingest, prev_eta)
        self.print("")  # start a new line
        self.print_upload_summary(progress)

    def print_upload_progress(self, progress, ingest, prev_eta):
        """Print upload progress"""
        finished = progress.items.finished + progress.items.skipped
        failed = progress.items.failed
        total = progress.items.total
        eta = self.compute_eta(ingest, progress.items, prev_eta)
        if eta:
            eta = str(eta["eta"]).split(".")[0]
        else:
            eta = "~"
        msg = f"{finished} / {total} ({failed} failed), ETA: {eta}"
        self.print(msg, replace=True)

    def print_upload_summary(self, progress):
        """Print upload summary"""
        exclude = ["finished"]
        for status, count in progress.items.dict().items():
            if count > 0 and status not in exclude:
                self.print(f"{status.capitalize()}: {count}")

    def print_final_report(self):
        """Print final report of the ingest"""
        self.print(str(crayons.magenta("Final report", bold=True)))
        report = self.client.report
        if report.errors:
            self.print("The following errors happend:")
            for error in report.errors:
                self.print(f"{error.type}: {error.message}")

        for status, elapsed in report.elapsed.items():
            elapsed = str(datetime.timedelta(seconds=elapsed))
            cap_status = status.replace('_', ' ').capitalize()
            self.print(f"{cap_status} took: {elapsed}")

        total_elapsed = 0
        for st_elapsed in report.elapsed.values():
            total_elapsed += st_elapsed

        elapsed = str(datetime.timedelta(seconds=total_elapsed))
        self.print(f"Total elapsed time: {elapsed}")

    def print(self, msg, replace=False):
        """Print"""
        if replace:
            msg = f"\r{msg}\033[K"
        else:
            msg = f"{msg}\n"
        self._fh.write(msg)
        self._fh.flush()

    def print_status_header(self, status, timestamp):
        """Print status header"""
        status_name = status.replace("_", " ").capitalize().ljust(15)
        status_name = str(crayons.magenta(status_name, bold=True))
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.print(f"{status_name}[{timestamp}]")

    def save_reports(self):
        """Save audit/deid logs and subjects csv if it was requested"""
        for type_ in ("save_audit_log", "save_deid_log", "save_subjects"):
            path = getattr(self.config, type_)
            if not path:
                continue
            stream = getattr(self.client, type_)
            final_path = self.save_stream_to_file(stream, path, type_)
            self.print(f"Saved {type_.replace('_', ' ')} to {final_path}")

    @staticmethod
    def save_stream_to_file(stream, path, prefix, extension="csv"):
        """Save stream to file"""
        error = None
        try:
            path = util.get_filepath(path, prefix=prefix, extension=extension)
        except FileNotFoundError as exc:
            error = str(exc)
            path = util.get_filepath(root_config.LOG_FILE_DIRPATH, prefix=prefix)
        except FileExistsError as exc:
            error = f"File already exists: {path}"
            path = util.get_incremental_filename(path)

        with open(path, "w") as fp:
            for line in stream:
                fp.write(line)

        if error:
            msg = f"{error}. Fallback to: {path}"
            log.error(msg)

        return path

    @staticmethod
    def compute_eta(ingest, item_stats, prev_eta):
        """Compute ETA"""
        if item_stats.finished == 0:
            return None
        if prev_eta and item_stats.finished == prev_eta["finished"]:
            report_time = datetime.datetime.utcnow()
            new_eta = prev_eta["eta"] - (report_time - prev_eta["report_time"])
            prev_eta["eta"] = max(new_eta, datetime.timedelta(0))
            prev_eta["report_time"] = report_time
        else:
            upload_started = Reporter.get_upload_start_time(ingest.history)
            report_time = datetime.datetime.utcnow()
            elapsed_time = report_time - upload_started
            remaining_time = (elapsed_time / item_stats.finished) * (item_stats.pending + item_stats.running)
            prev_eta.update({
                "eta": remaining_time,
                "report_time": report_time,
                "pending": item_stats.pending,
                "finished": item_stats.finished,
            })
        return prev_eta

    @staticmethod
    def get_upload_start_time(status_history):
        """Return when upload started"""
        for st_name, timestamp in status_history:
            if st_name == T.IngestStatus.uploading:
                return datetime.datetime.utcfromtimestamp(timestamp)
        return None
