import time
import os
from itertools import chain, combinations

import pytest
import os

from octorest import OctoRest

from betamax import Betamax
from betamax_serializers import pretty_json

from _common import URL, APIKEY

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'
    record_mode = os.environ.get('RECORD', 'none')
    config.default_cassette_options['record_mode'] = record_mode
    config.default_cassette_options['match_requests_on'] = {
        'uri',
        'method',
    }
    Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    config.default_cassette_options['serialize_with'] = 'prettyjson'


def sleep(seconds):
    '''
    If recording, sleep for a given amount of seconds
    '''
    # if 'RECORD' in os.environ:
    time.sleep(seconds)


def cmd_wait(client, state):
    while client.state() == state:
        sleep(0.1)


def cmd_wait_until(client, state):
    while client.state() != state:
        sleep(0.1)


def subsets(*items):
    '''
    Get all possible subsets of something
    '''
    N = len(items)+1
    return chain(*map(lambda x: combinations(items, x), range(0, N)))


def zero(component):
    '''
    Add a 0 at the end of the component, if it is tool
    '''
    return 'tool0' if component == 'tool' else component


# @pytest.mark.usefixtures('betamax_session')
@pytest.fixture
def client():
    return OctoRest(url=URL, apikey=APIKEY, session=None)


@pytest.fixture
def gcode():
    class GCode:
        def __init__(self, filename):
            self.filename = filename
            self.path = 'tests/fixtures/gcodes/{}'.format(filename)

    return GCode('telephonebox.gcode')


class TestClient:
    @pytest.mark.usefixtures('betamax_session')
    def test_init_works_with_good_auth(self):
        # Should not raise anything
        OctoRest(url=URL, apikey=APIKEY)

    @pytest.mark.usefixtures('betamax_session')
    def test_init_raises_with_bad_auth(self):
        with pytest.raises(RuntimeError):
            OctoRest(url=URL, apikey='nope')

    ### VERSION INFORMATION TESTS ###

    def test_version(self, client):
        version = client.get_version()
        assert 'api' in version
        assert 'server' in version
        assert 'text' in version

    ### FILE OPERATION TESTS ###

    def test_files_contains_files_and_free_space_info(self, client):
        files = client.files()
        assert 'bigben.gcode' in [f['name'] for f in files['files']]
        assert isinstance(files['free'], int)

    def test_files_local_works(self, client):
        files = client.files('local')
        assert 'bigben.gcode' in [f['name'] for f in files['files']]
        assert isinstance(files['free'], int)

    def test_files_sdcard_works(self, client):
        files = client.files('sdcard')
        assert files['files'] == []  # no files on sdcard
        assert 'free' not in files  # API doesn't report that back

    @pytest.mark.parametrize('filename', ('bigben.gcode', 'stpauls.gcode'))
    def test_info_for_specific_file(self, client, filename):
        f = client.files(filename)
        assert f['name'] == filename

    @pytest.mark.parametrize('filename', ('unicorn.gcode', 'yeti.gcode', 'noexist.gcode'))
    def test_nonexisting_file_raises(self, client, filename):
        with pytest.raises(RuntimeError):
            client.files(filename)

    def test_upload_by_path(self, client, gcode):
        f = client.upload(gcode.path)
        assert f['done']
        assert f['files']['local']['name'] == gcode.filename
        client.delete(gcode.filename)

    def test_upload_file_object(self, client, gcode):
        with open(gcode.path) as fo:
            f = client.upload(('fake.gcode', fo))
        assert f['done']
        assert f['files']['local']['name'] == 'fake.gcode'
        client.delete('fake.gcode')

    def test_upload_and_select(self, client, gcode):
        f = client.upload(gcode.path, select=True)
        assert f['done']
        assert f['files']['local']['name'] == gcode.filename
        selected = client.job_info()['job']['file']['name']
        assert selected == gcode.filename
        client.delete(gcode.filename)

    def test_upload_and_print(self, client, gcode):
        f = client.upload(gcode.path, print=True)
        sleep(1)
        assert f['done']
        assert f['files']['local']['name'] == gcode.filename
        selected = client.job_info()['job']['file']['name']
        assert selected == gcode.filename
        assert client.state() == 'Printing'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_upload_and_select_one_by_one(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename)
        selected = client.job_info()['job']['file']['name']
        assert selected == gcode.filename
        client.delete(gcode.filename)

    def test_upload_and_select_with_print_one_by_one(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename, print=True)
        sleep(1)
        selected = client.job_info()['job']['file']['name']
        assert selected == gcode.filename
        assert client.state() == 'Printing'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_upload_and_select_and_print_one_by_one(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename)
        selected = client.job_info()['job']['file']['name']
        assert selected == gcode.filename
        client.start()
        sleep(1)
        assert client.state() == 'Printing'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_file_copy(self, client, gcode):
        client.upload(gcode.path)
        client.copy(gcode.filename, 'copied.gcode')
        files = client.files()
        assert gcode.filename in [f['name'] for f in files['files']]
        assert 'copied.gcode' in [f['name'] for f in files['files']]
        client.delete(gcode.filename)
        client.delete('copied.gcode')

    def test_file_copy_exists(self, client, gcode):
        client.upload(gcode.path)
        client.copy(gcode.filename, 'copied.gcode')
        files = client.files()
        assert gcode.filename in [f['name'] for f in files['files']]
        assert 'copied.gcode' in [f['name'] for f in files['files']]
        with pytest.raises(RuntimeError):
            client.copy(gcode.filename, 'copied.gcode')
        client.delete(gcode.filename)

    def test_file_copy_folder_not_exist(self, client, gcode):
        files = client.files()
        if 'copied.gcode' in [f['name'] for f in files['files']]:
            client.delete('copied.gcode')
        client.upload(gcode.path)
        with pytest.raises(RuntimeError):
            client.copy(gcode.filename, '/random/path/copied.gcode')
        client.delete(gcode.filename)

    def test_file_move(self, client, gcode):
        client.upload(gcode.path)
        client.move(gcode.filename, 'moved.gcode')
        files = client.files()
        assert 'moved.gcode' in [f['name'] for f in files['files']]
        client.delete('moved.gcode')

    def test_file_move_exists(self, client, gcode):
        client.upload(gcode.path)
        client.move(gcode.filename, 'moved.gcode')
        files = client.files()
        assert 'moved.gcode' in [f['name'] for f in files['files']]
        client.upload(gcode.path)
        with pytest.raises(RuntimeError):
            client.move(gcode.filename, 'moved.gcode')
        client.delete(gcode.filename)
        client.delete('moved.gcode')

    def test_file_move_folder_not_exist(self, client, gcode):
        client.upload(gcode.path)
        with pytest.raises(RuntimeError):
            client.copy(gcode.filename, '/random/path/moved.gcode')
        client.delete(gcode.filename)

    def test_slice_curalegacy(self, client):
        client.slice('biscuithelper.STL', slicer='curalegacy')
        sleep(2)
        files = client.files()
        assert 'biscuithelper.gco' in [f['name'] for f in files['files']]
        client.delete('biscuithelper.gco')

    @pytest.mark.parametrize('name', ('biscuits.gco', 'richtea.gcode'))
    def test_slice_curalegacy_gcode(self, client, name):
        client.slice('biscuithelper.STL', slicer='curalegacy', gcode=name)
        sleep(2)
        files = client.files()
        assert name in [f['name'] for f in files['files']]
        client.delete(name)

    def test_slice_curalegacy_select(self, client):
        client.slice('biscuithelper.STL', slicer='curalegacy', select=True)
        sleep(2)
        files = client.files()
        assert 'biscuithelper.gco' in [f['name'] for f in files['files']]
        selected = client.job_info()['job']['file']['name']
        assert selected == 'biscuithelper.gco'
        client.delete('biscuithelper.gco')

    def test_upload_print_pause_cancel(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename, print=True)
        cmd_wait_until(client, 'Printing')
        client.pause()
        cmd_wait(client, 'Pausing')
        assert client.state() == 'Paused'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_upload_print_pause_restart(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename, print=True)
        cmd_wait_until(client, 'Printing')
        client.pause()
        cmd_wait_until(client, 'Paused')
        assert client.state() == 'Paused'
        client.restart()
        cmd_wait_until(client, 'Printing')
        assert client.state() == 'Printing'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_upload_print_pause_resume(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename, print=True)
        cmd_wait_until(client, 'Printing')
        client.pause()
        cmd_wait_until(client, 'Paused')
        assert client.state() == 'Paused'
        client.resume()
        cmd_wait_until(client, 'Printing')
        assert client.state() == 'Printing'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_upload_print_toggle(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename, print=True)
        cmd_wait_until(client, 'Printing')
        client.toggle()
        cmd_wait_until(client, 'Paused')
        assert client.state() == 'Paused'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_upload_print_toggle_toggle(self, client, gcode):
        client.upload(gcode.path)
        client.select(gcode.filename, print=True)
        cmd_wait_until(client, 'Printing')
        client.toggle()
        cmd_wait_until(client, 'Paused')
        assert client.state() == 'Paused'
        client.toggle()
        cmd_wait_until(client, 'Printing')
        assert client.state() == 'Printing'
        client.cancel()
        cmd_wait(client, 'Cancelling')
        client.delete(gcode.filename)

    def test_logs(self, client):
        logs = client.logs()
        assert 'files' in logs
        assert 'free' in logs
        assert isinstance(logs['free'], int)

    def test_delete_log(self, client):
        logs = client.logs()
        log_lst = [log['name'] for log in logs['files']]
        assert log_lst[0] in log_lst
        client.delete_log(log_lst[0])
        logs = client.logs()
        for log in logs['files']:
            assert log['name'] != log_lst[0]

    def test_printer(self, client):
        printer = client.printer()
        assert 'ready' in printer['sd']
        assert printer['state']['flags']['operational']
        assert printer['state']['flags']['ready']
        assert not printer['state']['flags']['error']
        assert not printer['state']['flags']['printing']

    def test_printer_temps(self, client):
        printer = client.printer()
        cmd_wait_until(client, 'Operational')
        assert 'bed' in printer['temperature']
        assert 'tool0' in printer['temperature']
        assert 'history' not in printer['temperature']

    @pytest.mark.parametrize('exclude', subsets('sd', 'temperature', 'state'))
    def test_printer_with_excluded_stuff(self, client, exclude):
        printer = client.printer(exclude=exclude)
        for key in exclude:
            assert key not in printer
        assert len(printer) == 3 - len(exclude)

    def test_printer_with_history(self, client):
        printer = client.printer(history=True)
        assert isinstance(printer['temperature']['history'], list)

    @pytest.mark.parametrize('limit', range(1, 4))
    def test_printer_with_history_and_limit(self, client, limit):
        printer = client.printer(history=True, limit=limit)
        assert len(printer['temperature']['history']) == limit

    @pytest.mark.parametrize('key', ('actual', 'target', 'offset'))
    @pytest.mark.parametrize('component', ('tool', 'bed'))
    def test_tool_and_bed(self, client, key, component):
        info = getattr(client, component)()  # client.tool() or bed()
        assert 'history' not in info
        assert isinstance(info[zero(component)][key], (float, int))

    # @pytest.mark.parametrize('key', ('actual', 'target'))
    # @pytest.mark.parametrize('component', ('tool', 'bed'))
    # def test_tool_and_bed_with_history(self, client, key, component):
    #     # TODO: history is not working with bed or tool, only printer
    #     info = getattr(client, component)(history=True)
    #     assert 'history' in info
    #     for h in info['history']:
    #         assert isinstance(h[zero(component)][key], (float, int))

    # @pytest.mark.parametrize('limit', range(1, 4))
    # @pytest.mark.parametrize('component', ('tool', 'bed'))
    # def test_tool_and_bed_with_history_limit(self, client, limit, component):
    #     # TODO: history is not working with bed or tool, only printer
    #     info = getattr(client, component)(history=True, limit=limit)
    #     assert len(info['history']) == limit

    def test_home_all(self, client):
        # we are only testing if no exception occurred, there's no return
        client.home()

    @pytest.mark.parametrize('axes', (('x',), ('y',), ('z',), ('x', 'y',)))
    def test_home_some(self, client, axes):
        # we are only testing if no exception occurred, there's no return
        client.home(axes)

    @pytest.mark.parametrize('coordinates', ((20, 0, 0), (0, 20, 0)))
    def test_jog(self, client, coordinates):
        # we are only testing if no exception occurred, there's no return
        client.jog(*coordinates)

    @pytest.mark.parametrize('factor', (100, 50, 150, 0.5, 1.0))
    def test_feedrate(self, client, factor):
        # we are only testing if no exception occurred, there's no return
        client.feedrate(factor)

    @pytest.mark.parametrize('how', (200, [200], {'tool0': 200}))
    def test_set_tool_temperature_to_200(self, client, how):
        client.tool_target(how)
        tool = client.tool()
        assert tool['tool0']['target'] == 200.0
        if 'RECORD' in os.environ:
            # Betamax had some problems here
            # And we don't do this for testing, but only with actual printer
            client.tool_target(0)

    # @pytest.mark.parametrize('how', (20, [20], {'tool0': 20}))
    # def test_set_tool_offset_to_20(self, client, how):
    #     client.tool_offset(how)
    #     tool = client.tool()
    #     print(tool)
    #     assert tool['tool0']['offset'] == 20.0
    #     # TODO: make the above assert work?
    #     if 'RECORD' in os.environ:
    #         client.tool_offset(0)

    def test_selecting_tool(self, client):
        # we are only testing if no exception occurred, there's no return
        client.tool_select(0)

    def test_extruding(self, client):
        # we are only testing if no exception occurred, there's no return
        client.extrude(1)

    def test_retracting(self, client):
        # we are only testing if no exception occurred, there's no return
        client.retract(1)

    @pytest.mark.parametrize('factor', (100, 75, 125, 0.75, 1.0))
    def test_flowrate(self, client, factor):
        # we are only testing if no exception occurred, there's no return
        client.flowrate(factor)

    def test_set_bed_temperature_to_100(self, client):
        client.bed_target(100)
        bed = client.bed()
        assert bed['bed']['target'] == 100.0
        if 'RECORD' in os.environ:
            client.bed_target(0)

    def test_set_bed_offset_to_10(self, client):
        client.bed_offset(10)
        bed = client.bed()
        assert bed['bed']['offset'] == 10.0
        if 'RECORD' in os.environ:
            client.bed_offset(0)

    def test_sd_card_init(self, client):
        client.sd_init()

    def test_sd_card_refresh(self, client):
        client.sd_refresh()

    def test_sd_card_release(self, client):
        client.sd_release()

    def test_sd_card_status(self, client):
        sd = client.sd()
        # no SD card here, so always not ready
        assert sd['ready'] is False

    def test_single_gcode_command(self, client):
        client.gcode('G28 X')

    def test_multiple_gcode_commands_nl(self, client):
        client.gcode('G28 X\nG28 Y')

    def test_multiple_gcode_commands_list(self, client):
        client.gcode(['G28 X', 'G28 Y'])

    def test_get_settings(self, client):
        settings = client.settings()
        assert 'api' in settings
        assert 'appearance' in settings

    def test_unchanged_settings(self, client):
        settings = client.settings()
        new_settings = client.settings({})
        assert settings['api'] == new_settings['api']
        assert settings['appearance'] == new_settings['appearance']

    def test_change_settings(self, client):
        settings = client.settings()
        printer_name = settings['appearance']['name']
        test_name = {'appearance': {'name': 'Gandalf'}}
        new_settings = client.settings(test_name)
        assert new_settings['appearance']['name'] == 'Gandalf'
        client.settings({'appearance': {'name': printer_name}})

    # def test_tmp_session_key(self, client):
    #     key = client.tmp_session_key()
    #     print(key)

    def test_users(self, client):
        users = client.users()
        assert 'users' in users

    ### CONNECTION HANDLING TESTS ###

    def test_connection_info(self, client):
        info = client.connection_info()

        assert 'current' in info
        assert 'baudrate' in info['current']
        assert 'port' in info['current']
        assert 'state' in info['current']

        assert 'options' in info
        assert 'baudrates' in info['options']
        assert 'ports' in info['options']

    def test_fake_ack(self, client):
        # we are only testing if no exception occurred, there's no return
        client.fake_ack()

    def test_disconnect(self, client):
        client.disconnect()
        assert client.state() in ['Offline', 'Closed']

    def test_connect(self, client):
        '''
        Since it's hard with betamax fixture to check state() multiple times
        in one test, this test hopes test_disconnect() was called before it.
        It is not possible to run it without it in record mode.
        TODO: Fix this
        '''
        client.connect()
        cmd_wait(client, 'Detecting baudrate')
        assert client.state() in ['Connecting',
                                  'Operational',
                                  'Opening serial port']
        client.disconnect()
        assert client.state() in ['Offline', 'Closed']


# import json
# client = OctoRest(url=URL, apikey=APIKEY)
# client.new_folder('hello')
# f = client.files(recursive=False)
# print(json.dumps(f, indent=4))
# g = client.files(recursive=True)
# print(json.dumps(f, indent=4))
# print(f == g)
# print(client.version)
# client.gcode("M106")
# client.gcode("M106 \n G28 X Y Z \n M107")
