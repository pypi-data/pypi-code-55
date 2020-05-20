import os
import time
import traceback
from datetime import datetime, timedelta

import boto3

from starling.config import CONFIG
from starling.exception import RetryTaskExitError, RetryTaskError, RetryTaskSkipAuthError
from starling.helper import retry_task, retry_run
from starling.types import ScrapperData, TaskData
from .blueprint_scrapper import BlueprintScrapper


class Scrapper:
    @staticmethod
    @retry_task()
    def _run_task(task: TaskData, scrapper_data: ScrapperData):
        package_name, classname = task.action.rsplit('.', 1)
        blueprint = getattr(__import__(package_name, fromlist=[package_name]), classname)(scrapper_data, task)
        fetched_data = blueprint.fetch()
        time.sleep(os.getenv('INTERVAL', blueprint.interval()))
        scrapper_data.message.scrap_finished_at = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        visibility_timeout_at = datetime.strptime(scrapper_data.message.visibility_timeout_at, '%Y%m%d%H%M%S')
        if visibility_timeout_at - datetime.now() < timedelta(seconds=8 * 60):
            message = scrapper_data.message
            consumed_at = datetime.strptime(message.consumed_at, '%Y%m%d%H%M%S')

            next_visibility_timeout_at = visibility_timeout_at + timedelta(seconds=10 * 60)
            message.visibility_timeout_at = next_visibility_timeout_at.strftime('%Y%m%d%H%M%S')
            visibility_timeout = (next_visibility_timeout_at - consumed_at).seconds

            boto3.client('sqs').change_message_visibility(
                QueueUrl=message.message['QueueUrl'],
                ReceiptHandle=message.message['ReceiptHandle'],
                VisibilityTimeout=visibility_timeout,
            )

        return fetched_data, True, {}

    @staticmethod
    @retry_run()
    def _run(scrapper: BlueprintScrapper, is_auth=True):
        if is_auth:
            scrapper.authenticate()

        for action in scrapper.valid_actions:
            for task in [task for task in [tasks for tasks in scrapper.data.actions[action]]
                         if task.is_done is False]:
                task.fetched_data, task.is_done, task.error = Scrapper._run_task(task, scrapper.data)

    @staticmethod
    def run(scrapper: BlueprintScrapper, **kwargs):
        CONFIG.update(kwargs)
        scrapper.data.message.scrap_started_at = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        try:
            Scrapper._run(scrapper)
        except (RetryTaskExitError, RetryTaskError, RetryTaskSkipAuthError) as e:
            scrapper.data.is_valid = e.extra.get('is_valid', False)
            scrapper.data.error_message = e.message
            scrapper.data.error_extra = e.extra
        except Exception as e:
            scrapper.data.is_valid = False
            scrapper.data.error_message = '__UNEXPECTED_SCRAPPER_ERROR__'
            scrapper.data.error_extra = dict(tb=traceback.format_exc(), err=str(e))
        return scrapper.data
