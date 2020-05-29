import time
import logging
import threading
import yaml
from xlsxhelper import get_worksheet, get_cells
from .browser import Browser

CMD_STARTING_ROW = 5

logger = logging.getLogger(__name__)


def run_xlsx_config(config_xlsx_path, sheet=None, variables_yml_path=None, instance_start_delay=5):
    worksheet = get_worksheet(config_xlsx_path, sheet)
    xlsxdata = get_cells(worksheet, only_data=True)
    config = {}
    config["webdriver"] = xlsxdata[1][1]
    config["width"] = xlsxdata[2][1]
    config["height"] = xlsxdata[3][1]
    config["commands"] = xlsxdata[CMD_STARTING_ROW:]
    if variables_yml_path:
        with open(variables_yml_path, "r", encoding="utf-8") as fobj:
            context = yaml.safe_load(fobj)
    else:
        context = {}
    if isinstance(context, (tuple, set, list)):
        contexts = context
        browsers = []
        threads = []
        for context in contexts:
            browser = Browser(config)
            thread = threading.Thread(target=browser.run, args=[context])
            thread.setDaemon(True)
            thread.start()
            browsers.append(browser)
            threads.append(thread)
            time.sleep(instance_start_delay)
        for thread in threads:
            thread.join()
    else:
        browser = Browser(config)
        browser.run(context)
