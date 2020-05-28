import copy
import datetime
import jinja2
import json
import logging
import os
import pytz

import quicklogging

from . import APP_NAME
from . import datastore
from . import utils

DATE_FORMAT = "%H:%M:%S %d/%m/%Y %Z%z"


class Report:
    def __init__(
            self,
            outputdir,
            name,
            template_loader,
            accepted_checklevels=None,
            ignored_keyvalues=None,
    ):
        """
        :param sequence accepted_checklevels: if None, all levels are accepted
            list containing "warning", "critical", "unknown", "ok"
        :param sequence ignored_keyvalues: if None, all checks are accepted
        """
        self.name = name
        self.accepted_checklevels = accepted_checklevels
        self.ignored_keyvalues = ignored_keyvalues
        outputfile = os.path.join(outputdir, name)
        self.filename = f"{outputfile}.html"
        self.filename_swp = f"{self.filename}.swp"

        # set in config
        templateEnv = jinja2.Environment(loader=template_loader)
        TEMPLATE_FILE = "report.html.jinja2"
        self.template = templateEnv.get_template(TEMPLATE_FILE)

    def _filter_checklevels(self, all_checks):
        for check in all_checks:
            if self.accepted_checklevels is None:
                yield check
            elif check.level in self.accepted_checklevels:
                yield check

    def _filter_ignored(self, all_checks):
        if self.ignored_keyvalues is None:
            for check in all_checks:
                yield check
            return
        for attr, value in self.ignored_keyvalues.items():
            for check in all_checks:
                if getattr(check, attr) == value:
                    continue
                yield check

    def _all_filters(self, all_checks):
        residual = copy.copy(all_checks)
        for filterfunc in (
                self._filter_checklevels,
                self._filter_ignored,
        ):
            residual = list(filterfunc(residual))

        return residual

    def generate(self, all_checks, printable_date):
        displayed = list(self._all_filters(all_checks))

        with open(self.filename_swp, "w") as reportfd:
            reportfd.write(
                self.template.render(
                    supervision_data=displayed,
                    date=printable_date,
                )
            )
        os.rename(self.filename_swp, self.filename)

        quicklogging.debug(
            "Updated: %s: %s with %d records",
            printable_date,
            self.filename,
            len(displayed)
        )


class Munin2Widget:
    def __init__(self, config, restore=False):
        self.cache_file = os.path.join(config.cache_directory, "cache.yaml")
        self._reports = list(
            self._gen_reports(config.outputdir, config.reports)
        )
        checkstore = self._get_store(restore)
        assert isinstance(checkstore, datastore.CheckStore)
        self.store = checkstore
        self._tz_utc = pytz.timezone("UTC")
        self._tz_user = config.timezone

    def consume(self, text):
        """Handles request content

        :param str text:
        """
        self.store.consume(text)
        self.gen_html()
        self._update_cache()

    def _gen_reports(self, outputdir, reportcfg_dict):
        template_loader = jinja2.PackageLoader(APP_NAME, "templates")
        for name, reportcfg in reportcfg_dict.items():
            yield Report(
                outputdir,
                name,
                template_loader,
                **reportcfg
            )

    def _get_store(self, restore):
        if restore:
            try:
                return datastore.CheckStore.restore(self.cache_file)
            except OSError:
                logging.exception(
                    "Error opening cache file %s - this is not fatal, "
                    "starting with no cache",
                    self.cache_file
                )
        return datastore.CheckStore()

    def _update_cache(self):
        self.store.save(self.cache_file)

    def gen_html(self):
        now_utc = datetime.datetime.now(self._tz_utc)
        now_local = now_utc.astimezone(self._tz_user)
        printable_date = now_local.strftime(DATE_FORMAT)
        data = list(self.store.getchecks())
        for report in self._reports:
            report.generate(data, printable_date)

    def filter_essential(self, obj):
        if obj.level not in self.checklevels:
            return False
        for attr, value in self.ignored.items():
            if getattr(obj, attr) == value:
                return False
        return True

    def json_load_concatenated(self, text):
        text = text.lstrip()
        decoder = json.JSONDecoder()
        while text:
            obj, index = decoder.raw_decode(text)
            utils.purge_none(obj)

            if self.should_display(obj):
                yield obj

            text = text[index:].lstrip()
