import time
import os
import logging
import threading
from typing import Callable, Union, List
import re
from ika.c_mag_hs_7 import CMAGHS7Interface, CMAGHS7InterfaceVisual
from pathlib import Path
from hein_utilities.slack_integration.parsing import ignore_bot_users
from hein_utilities.slack_integration.bots import WebClientOverride
from hein_utilities.slack_integration.slack_managers import RTMControlManager, do_nothing, return_empty


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

"""
    for slack integration, this requires a python file called slack_manager_info.py to be in the same directory as this 
    file. this file should be not shared online, so you will have to create one in order to use slack integration
    there should be three lines in the file:
    bot_token = 'BOT_TOKEN_HERE'  
    bot_name = 'BOT_NAME_HERE'
    channel_name = '#CHANNEL_NAME_HERE'

    Create this mock rtm control manager class so that if no slack details are provided, then calls to post something 
    to 
    slack don't crash the script
    """


class MockRTMControlManager(RTMControlManager):
    def __init__(self,
                 user_member_ids: Union[str, List[str]] = None,
                 token: str = None,
                 channel_name: str = None,
                 auto_reconnect: bool = True,
                 ping_interval: int = 10,
                 start_action: Callable = do_nothing,
                 stop_action: Callable = do_nothing,
                 resume_action: Callable = do_nothing,
                 pause_action: Callable = do_nothing,
                 status_query: Callable = return_empty,
                 help_query: Callable = return_empty,
                 pre_parsing_methods: List[Callable] = None,
                 ):
        pass

    def post_slack_message(self,
                           msg: str,
                           tag_admin: bool = False,
                           tagadmin: bool = None,
                           snippet: str = None,
                           ):
        pass

    def post_slack_file(self,
                        filepath: str,
                        title: str,
                        comment: str,
                        ):
        pass


def main():
    test_save_path = Path.cwd().joinpath('ika_test')
    Path.mkdir(test_save_path, exist_ok=True)
    ika_magnetic_stirrer_port = 'COM7'  # todo
    # ika_magnetic_stirrer = CMAGHS7Interface(device_port=ika_magnetic_stirrer_port)
    ika_magnetic_stirrer = CMAGHS7InterfaceVisual(device_port=ika_magnetic_stirrer_port,
                                                  save_folder=test_save_path)
    ika_magnetic_stirrer.save_temperature_data_interval = 30  # seconds
    ika_magnetic_stirrer.n = 180
    ika_magnetic_stirrer.std_max = 0.05
    ika_magnetic_stirrer.sem_max = 0.05
    ika_magnetic_stirrer.upper_limit = 0.5
    ika_magnetic_stirrer.lower_limit = 0.5
    ika_magnetic_stirrer.r_min = None
    ika_magnetic_stirrer.slope_upper_limit = None
    ika_magnetic_stirrer.slope_lower_limit = None

    try:
        import slack_manager_info
        bot_token, bot_name, channel_name = slack_manager_info.bot_token, slack_manager_info.bot_name, \
                                            slack_manager_info.channel_name

        slack_manager = RTMControlManager(
            token=bot_token,
            channel_name=channel_name,
        )
        logger.addHandler(slack_manager)

        # # add the event handler function
        # @slack_manager.run_on(event='message')
        # @ignore_bot_users
        # def catch_message(**payload):
        #     """catches and interprets a message"""
        #     message = payload['data']
        #     text = message.get('text')
        #     web_client = payload['web_client']
        #
        #     # current image catch
        #     if re.search('graph', text, re.IGNORECASE) is not None:
        #         with WebClientOverride(slack_manager, web_client):
        #             image_save_path: Path = ika_magnetic_stirrer.save_graph()
        #             slack_manager.post_slack_file(filepath=str(image_save_path),
        #                                           title='Temperature vs. time',
        #                                           comment='Temperature vs. time graph, the green regions are stable '
        #                                                   'regions'
        #                                           )
        #             os.remove(str(image_save_path))
        #
        # slack_manager_thread = threading.Thread(target=slack_manager.start_rtm_client).start()
    except Exception as e:
        slack_manager = MockRTMControlManager()

    stir_rate = 250
    increment = 10
    initial_temp = 35
    current_temp = initial_temp - increment
    final_temp = 60
    time_out = 45 * 60  # seconds

    ika_magnetic_stirrer.target_stir_rate = stir_rate
    ika_magnetic_stirrer.start_stirring()

    # logger.info('before start')
    # ika_magnetic_stirrer.start_monitoring_temperature()
    # logger.info('after start')
    # time.sleep(10)
    # logger.info('before stop')
    # ika_magnetic_stirrer.stop_monitoring_temperature()
    # logger.info('after stop')
    # logger.info('before start')
    # ika_magnetic_stirrer.start_monitoring_temperature()
    # logger.info('after start')
    # time.sleep(10)
    # logger.info('before stop')
    # ika_magnetic_stirrer.stop_monitoring_temperature()
    # logger.info('after stop')
    # logger.info('before start')
    # ika_magnetic_stirrer.start_monitoring_temperature()
    # logger.info('after start')
    # time.sleep(10)
    # logger.info('before stop')
    # ika_magnetic_stirrer.stop_monitoring_temperature()
    # logger.info('after stop')
    # logger.info('done with testing monitoring')

    ika_magnetic_stirrer.target_temperature = initial_temp
    ika_magnetic_stirrer.start_heating()

    while current_temp < final_temp:
        current_temp += increment
        ika_magnetic_stirrer.target_temperature = current_temp
        temp_stabilized: bool = ika_magnetic_stirrer.wait_until_temperature_stable(time_out=time_out)
        ika_magnetic_stirrer.save_graph_stable_visualized(file_name=f'ika_test_target_{current_temp}')
        logger.info(f'reached stabilized at temperature {current_temp}: {temp_stabilized}')

    ika_magnetic_stirrer.stop_heating()


if __name__ == '__main__':
    main()
