import os
import copy
import time
import datetime
import logging
import selenium
from selenium import webdriver

logger = logging.getLogger(__name__)

CMD_COLUMN = 2
CMD_INDEX_COLUMN = 0
PARAM1_COLUMN = 3
PARAM2_COLUMN = 4
PARAM3_COLUMN = 5
PARAM4_COLUMN = 6
PARAM5_COLUMN = 7
PARAM6_COLUMN = 8
PARAM7_COLUMN = 9
PARAM8_COLUMN = 10
PARAM9_COLUMN = 11
PARAM10_COLUMN = 12
STATUS_TIP_COLUMN = 13


def default_status_report_callback(status, command_line=None):
    command_line = command_line or ["XXX"]
    logger.info("Browser status change to {0} at step {1}".format(status, command_line[0]))
    print("INFO: Browser status change to {0} at step {1}".format(status, command_line[0]))

class Browser(object):

    def __init__(self, config, status_report_callback=None, browser=None):
        self.config = config
        self.browser = browser
        self.status_report_callback = status_report_callback or default_status_report_callback

    def run(self, context=None):
        logger.info("Browser.run start...")
        context = context or {}
        logger.info("Browser setup start...")
        self.setup()
        logger.info("Browser setup done.")
        for command_line in self.config.get("commands", []):
            logger.info("Run a command: {0}".format(command_line))
            status = command_line[STATUS_TIP_COLUMN]
            if status:
                self.status_report_callback(status, command_line)
            self.run_cmd(command_line, context)
        logger.info("Browser.run done.")

    def setup(self):
        self.setup_browser()
        self.setup_browser_size()
        self.init_screenshot_counter()

    def init_screenshot_counter(self):
        self._screenshot_counter = 0

    def setup_browser(self):
        if self.browser:
            return self.browser
        browser_engine = self.config.get("webdriver", "phantomjs").strip().lower()
        if browser_engine == "phantomjs":
            self.browser = webdriver.PhantomJS()
        elif browser_engine == "chrome":
            self.browser = webdriver.Chrome()
        elif browser_engine == "firefox":
            self.browser = webdriver.Firefox()
        elif browser_engine == "ie":
            self.browser = webdriver.Ie()
        else:
            raise RuntimeError("Bad browser engine: {}, avaiable options are phantomjs, chrome, firefox and ie.".format(config[1][1]))

    def setup_browser_size(self):
        width = int(self.config.get("width", 1366))
        height = int(self.config.get("height", 768))
        self.browser.set_window_size(width, height)

    def run_cmd(self, command_line, context):
        cmd = command_line[CMD_COLUMN].strip().lower()
        cmd_attr = cmd.replace("-", "_")
        cmd_func = getattr(self, cmd_attr, None)
        if not cmd_func:
            raise RuntimeError("Command {} not implemented...".format(cmd))
        cmd_func(command_line, context)

    def get_default_variables(self, context):
        variables = {
            "screenshot_counter": self._screenshot_counter,
        }
        variables.update(self.get_now_time_variables())
        variables.update(copy.deepcopy(context))
        return variables

    def get_now_time_variables(self):
        now_time = datetime.datetime.now()
        return {
            "now_time": now_time,
            "year": now_time.year,
            "month": now_time.month,
            "day": now_time.day,
            "hour": now_time.hour,
            "minitue": now_time.minute,
            "second": now_time.second,
            "timestamp": now_time.timestamp(),
        }

    def screenshot(self, command_line, context):
        self._screenshot_counter += 1
        variables = self.get_default_variables(context)
        filename = command_line[PARAM1_COLUMN].format(**variables)
        folder = os.path.dirname(filename)
        os.makedirs(folder, exist_ok=True)
        self.browser.save_screenshot(filename)

    def get(self, command_line, context):
        variables = self.get_default_variables(context)
        url = command_line[PARAM1_COLUMN].format(**variables)
        self.browser.get(url)

    def sleep(self, command_line, context):
        time.sleep(int(command_line[PARAM1_COLUMN]))

    def wait_for_url(self, command_line, context):
        variables = self.get_default_variables(context)
        cmd_index = command_line[CMD_INDEX_COLUMN]
        url = command_line[PARAM1_COLUMN].format(**variables)
        timeout = int(command_line[PARAM2_COLUMN])
        stime = time.time()
        while True:
            if time.time() - stime > timeout:
                raise RuntimeError("wait-for-url timeout at row: {}.".format(cmd_index))
            if url in self.browser.current_url:
                break
            time.sleep(1)

    def send_keys(self, command_line, context):
        variables = self.get_default_variables(context)
        targets = self.get_targets(command_line[PARAM1_COLUMN:], variables)
        text = command_line[PARAM3_COLUMN].format(**variables)
        for target in targets:
            target.send_keys(text)

    def click(self, command_line, context):
        variables = self.get_default_variables(context)
        targets = self.get_targets(command_line[PARAM1_COLUMN:], variables)
        for target in targets:
            try:
                target.click()
            except selenium.common.exceptions.ElementNotVisibleException:
                pass
            except selenium.common.exceptions.ElementNotInteractableException:
                pass

    def wait_and_monitoring(self, command_line, context):
        variables = self.get_default_variables(context)
        interval = command_line[PARAM1_COLUMN]
        filename = command_line[PARAM2_COLUMN].format(**variables)
        total = command_line[PARAM3_COLUMN]
        tip = command_line[PARAM4_COLUMN].format(**variables)
        stime = time.time()
        while True:
            if time.time() - stime >= total:
                break
            folder = os.path.dirname(filename)
            os.makedirs(folder, exist_ok=True)
            self.browser.save_screenshot(filename)
            logger.info("wait-and-monitoring start sleeping...")
            time.sleep(interval)
            self.status_report_callback(tip, command_line)

    def get_targets(self, params, variables):
        value = params[1].format(**variables)
        method = params[0]
        method_attr = "select_{0}".format(method).replace("-", "_")
        method_func = getattr(self, method_attr, None)
        if not method_func:
            raise RuntimeError("Element selector method not implemented: {}.".format(method))
        targets = method_func(value)
        if not isinstance(targets, (set, tuple, list)):
            return [targets]
        else:
            return targets

    def select_by_id(self, selector):
        return self.browser.find_element_by_id(selector)

    def select_by_class_name(self, selector):
        return self.browser.find_elements_by_class_name(selector)
    
    def select_by_tag_name(self, selector):
        return self.browser.find_elements_by_tag_name(selector)

    def select_by_xpath(self, selector):
        return self.browser.find_elements_by_xpath(selector)

    def select_by_css_selector(self, selector):
        return self.browser.find_elements_by_css_selector(selector)

    def select_by_link_text(self, selector):
        return self.browser.find_elements_by_link_text(selector)

    def select_by_partial_link_text(self, selector):
        return self.browser.find_elements_by_partial_link_text(selector)
