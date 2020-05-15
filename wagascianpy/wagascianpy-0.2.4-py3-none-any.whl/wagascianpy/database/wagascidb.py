#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

"""WAGASCI simple run database"""

import ctypes as ct
import os

import wagascianpy.database.db_record
import wagascianpy.database.my_tiny_db
import wagascianpy.utils.utils

###############################################################################
#                                  Constants                                  #
###############################################################################

# Public
WAGASCI_TOPOLOGY = {"0": 32, "1": 32, "2": 32, "3": 32, "4": 32, "5": 32, "6": 32, "7": 32,
                    "8": 32, "9": 32, "10": 32, "11": 32, "12": 32, "13": 32, "14": 32,
                    "15": 32, "16": 32, "17": 32, "18": 32, "19": 32}
WALLMRD_TOPOLOGY = {"0": 32, "1": 32, "2": 32}
DETECTORS = {'WallMRD north (DIF 0-1)': {"0": WALLMRD_TOPOLOGY, "1": WALLMRD_TOPOLOGY},
             'WallMRD south (DIF 2-3)': {"2": WALLMRD_TOPOLOGY, "3": WALLMRD_TOPOLOGY},
             'WAGASCI upstream (DIF 4-5)': {"4": WAGASCI_TOPOLOGY, "5": WAGASCI_TOPOLOGY},
             'WAGASCI downstream (DIF 6-7)': {"6": WAGASCI_TOPOLOGY, "7": WAGASCI_TOPOLOGY}}


###############################################################################
#                               Helper functions                              #
###############################################################################

# DIF ID ################################################

def _dif_id(file_name):
    file_name_split = os.path.splitext(os.path.basename(file_name))[0].split('ecal_dif_')
    if len(file_name_split) != 2:
        raise ValueError("raw data file name is not valid : %s" % str(file_name))
    else:
        return file_name_split[1]


# Get DIF topology ################################################

def _wrap_function(lib, funcname, restype, argtypes):
    """Simplify wrapping ctypes functions"""
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


def _get_dif_topology(lib_path, acq_config_xml):
    """Get detector topology (map_dif) from the acquisition configuration xml
    file"""
    if not os.path.exists(lib_path):
        return "undef"
    lib_wagasci = ct.CDLL(lib_path)
    wg_get_dif_topology = _wrap_function(lib_wagasci, 'GetDifTopologyCtypes',
                                         ct.c_char_p, [ct.c_char_p])
    return wg_get_dif_topology(bytes(acq_config_xml, encoding='utf-8')).decode()


def _free_topology(lib_path, topology_string):
    """Release memory for the topology string"""
    if os.path.exists(lib_path):
        lib_wagasci = ct.CDLL(lib_path)
        wg_free_topology = _wrap_function(lib_wagasci, 'FreeTopologyCtypes', None,
                                          [ct.c_char_p])
        wg_free_topology(bytes(topology_string, encoding='utf-8'))


# Check records ################################################

def _check_records(records):
    """check that all records are sane"""
    for record in records:
        if not isinstance(record, WagasciRunRecord):
            raise ValueError("record is not of type WagasciRunRecord")
        if not record.is_ready():
            raise ValueError("record is not ready to be inserted")


###########################################################################
#                                RunRecord                                #
###########################################################################

class WagasciRunRecord(wagascianpy.database.db_record.DBRecord):
    """Run record"""

    def __init__(self, record=None):

        self.name = None
        self.run_type = None
        self.run_number = None
        self.is_bad = None
        self.start_time = None
        self.stop_time = None
        self.duration_h = None
        self.topology = None
        self.run_folder = None
        self.xml_config = None
        self.raw_files = None
        super(WagasciRunRecord, self).__init__(record)

    def set_bad_run(self):
        """Set all fields other than name, run_number, run_type to default values for
        bad run. The name, run_number, run_type fields must be manually set.
        """
        self.is_bad = True
        self.start_time = 0
        self.stop_time = 0
        self.duration_h = 0.
        self.topology = "undef"
        self.raw_files = {}
        self.run_folder = "undef"
        self.xml_config = "undef"

    def set_start_time(self, datetime_str):
        """Set the run start time converting datetime string to epoch timestamp
        """
        self.start_time = self.datetime2timestamp(datetime_str)

    def set_stop_time(self, datetime_str):
        """Set the run stop time converting datetime string to epoch timestamp
        """
        self.stop_time = self.datetime2timestamp(datetime_str)

    def set_duration_h(self):
        """Set the run duration in hours
        """
        if self.stop_time is None or self.start_time is None:
            raise ValueError("Set start time and stop time before duration")
        self.duration_h = float((self.stop_time - self.start_time) / 3600.0)

    def get_start_datetime(self):
        """Get start datetime
        """
        if self.start_time is None:
            return None
        return self.timestamp2datetime(self.start_time)

    def get_stop_datetime(self):
        """Get stop datetime
        """
        if self.stop_time is None:
            return None
        return self.timestamp2datetime(self.stop_time)


###########################################################################
#                            VirtualDataBase                              #
###########################################################################


class WagasciDataBase(wagascianpy.database.my_tiny_db.MyTinyDB):
    """Virtual class to manage a database"""

    wagasci_lib = None

    def __init__(self, repo_location, db_location, is_borg_repo=False, update_db=False, rebuild_db=False):
        super(WagasciDataBase, self).__init__(db_location)
        self._repository = repo_location
        self._is_borg_repo = is_borg_repo
        if update_db or rebuild_db:
            self._update_wagasci_db(rebuild_db)

    def _update_wagasci_db(self, rebuild_db=False):
        self._borg = None

        self._run_type = os.path.basename(self._repository)
        self._run_record_list = []

        if ':' in self._repository and not self._is_borg_repo:
            raise NotImplementedError("Remote non borg repositories are "
                                      "not supported at the moment")

        self._borg = wagascianpy.utils.utils.which("borg")
        if self._borg is None and self._is_borg_repo:
            raise RuntimeError("borg program not found")

        # List of runs

        if self._is_borg_repo:
            borg_list = "%s list --short --log-json %s" % (self._borg, self._repository)
            run_list = wagascianpy.utils.utils.run_borg_cmd(borg_list).strip('\n').split('\n')
        else:
            run_list = [os.path.basename(dirs)
                        for dirs in os.scandir(self._repository) if dirs.is_dir()]
        # Loop over every run

        with wagascianpy.utils.utils.Cd(self._tmp_dir):
            for run_name in sorted(run_list):

                # Skip run if it is already in the database and the rebuild_db
                # flag is not set
                if not rebuild_db and self.has_record(os.path.basename(run_name)):
                    print("Skipping run %s" % run_name)
                    continue
                else:
                    print("Run %s not found in database" % run_name)

                run = WagasciRunRecord()
                run.name = run_name
                run.run_number = int(run_name.split('_')[-1])
                run.is_bad = False
                run.run_type = self._run_type
                run.raw_files = {}

                try:
                    file_list = []
                    if self._is_borg_repo:
                        borg_list = "%s list --short --log-json %s::%s" \
                                    % (self._borg, self._repository, run_name)
                        file_list = wagascianpy.utils.utils.run_borg_cmd(borg_list).strip('\n').split('\n')
                        run.run_folder = "not found"
                        if file_list:
                            random_file = file_list[0]
                            if run_name in random_file:
                                run.run_folder = random_file.split(run_name)[0].strip('/')
                                run.run_folder = '/' + run.run_folder
                    else:
                        run_path = os.path.join(self._repository, run_name)
                        run.run_folder = run_path
                        for root, dirs, files in os.walk(run_path, followlinks=False):
                            for filename in files:
                                file_list.append(os.path.join(root, filename))

                    for file_path in file_list:
                        if '.raw' in os.path.basename(file_path):
                            dif_id = _dif_id(file_path)
                            run.raw_files[dif_id] = file_path
                        elif '.log' in os.path.basename(file_path):
                            if self._is_borg_repo:
                                borg_extract = "%s extract --log-json %s::%s %s" \
                                               % (self._borg, self._repository, run_name, file_path)
                                wagascianpy.utils.utils.run_borg_cmd(borg_extract)
                                log_file = self._tmp_dir + "/" + file_path
                            else:
                                log_file = file_path
                            log = xml.etree.ElementTree.parse(log_file).getroot()
                            for param in log.findall("acq/param"):
                                name = param.get('name')
                                if name == "start_time":
                                    run.set_start_time(param.text)
                                if name == "stop_time":
                                    run.set_stop_time(param.text)
                            run.set_duration_h()
                        elif '.xml' in os.path.basename(file_path) and run.xml_config is None:
                            if self._is_borg_repo:
                                borg_extract = "%s extract --log-json %s::%s %s" \
                                               % (self._borg, self._repository, run_name, file_path)
                                wagascianpy.utils.utils.run_borg_cmd(borg_extract)
                                xml = "%s/%s" % (self._tmp_dir, file_path)
                            else:
                                xml = file_path
                            if self.wagasci_lib is not None:
                                run.topology = _get_dif_topology(self.wagasci_lib, xml)
                            else:
                                run.topology = "undef"
                            # TODO: fix bug in _free_topology
                            # _free_topology(WAGASCI_LIB, run.topology)
                            run.xml_config = file_path

                except Exception as error:
                    print('run %s : %s' % (run_name, str(error)))
                    run.set_bad_run()
                finally:
                    if run.is_bad:
                        print("Bad run %s found in repository" % run.name)
                    else:
                        print("Good run %s found in repository" % run.name)
                    self._run_record_list.append(run)
            _check_records(self._run_record_list)

        self.update_database(self._run_record_list, rebuild_db)

    def get_time_interval(self, datetime_start, datetime_stop,
                          only_good=True, include_overlapping=True):
        timestamp_start = WagasciRunRecord.datetime2timestamp(datetime_start)
        timestamp_stop = WagasciRunRecord.datetime2timestamp(datetime_stop)
        return super(WagasciDataBase, self).get_time_interval(timestamp_start, timestamp_stop,
                                                              only_good, include_overlapping)

    def print_run(self, name):
        """ Print info about a run """
        WagasciRunRecord(self.get_record(name)[0]).pretty_print()
