from typing import List, Union, Tuple
import os
import tempfile
import subprocess
import numpy as np
import pandas as pd


Lines = str


class CytosimReader:
    """
    Read data generated with cytosim. Initialize with the path 
    to the folder containing the output data. Reports can then
    be generated and read with the method ``read_report``.
    """

    def __init__(self, folder: str, report_executable: str='report'):
        """
        Create CytosimReader for an output folder containing data generated
        by cytosim simulations.

        :param folder: Path to folder containing cytosim output (cmo) files.
        :param report_executable: If you renamed your cytosim ``report`` executable,
                                  pass the name with this parameter.
        """
        self.folder = os.path.abspath(folder)
        self._folder_reports = os.path.join(folder, 'reports')
        if not os.path.exists(self._folder_reports):
            os.mkdir(self._folder_reports)
        if not os.path.isdir(self._folder_reports):
            msg = 'CytosimReader wants to put reports into folder "{}".'.format(self._folder_reports)
            msg += ' But there is a file with that name! Please move that file if you want to use CytosimReader.'
            raise RuntimeError(msg)
        self.report_exe = report_executable

    def read_report(self, report_identifier: str,
                    aggregate=False, clear=False) -> Union[List['ReportBlock'], pd.DataFrame]:
        """
        Read data from one report. If the report does not exist yet, it will be generated
        in the subfolder ``reports``. The filename will be ``<report_identifier>.txt``,
        where ``:`` delimiter used by cytosim will be replaced by underscores ``_``.
        Data will be either a list of ReportBlock objects (one per recorded frame), or, 
        if aggregate=True, one pandas.DataFrame containing data of all frames.
        To access the actual data of a RecordBlock, use the member RecordBlock.data .

        :param report_identifier: One of the valid identifiers that can be passed as an argument
                                  to cytosim's ``report`` executable; for example ``fiber:points``,
                                  which will create a report file ``reports/fiber_points.txt`` 
                                  and read its content into a pandas.DataFrame .
        :param aggregate: If True, will return data from the report as one big aggregated
                          DataFrame. Otherwise will return a list of ReportBlock objects, one
                          for each recorded frame.
        :param clear: Remove an existing report and re-generate it.

        :return: Either a list of ReportBlock objects (one per recorded frame), or, if aggregate=True,
                 one pandas.DataFrame containing data of all frames.
        """
        split_report_identifier = report_identifier.split(':')
        split_report_identifier = [s.strip() for s in split_report_identifier]
        fname_report = '_'.join(split_report_identifier) + '.txt'
        fname_report = os.path.join(self._folder_reports, fname_report)

        if clear:
            if os.path.exists(fname_report):
                os.remove(fname_report)
        if not os.path.exists(fname_report):
            self._generate_report(report_identifier, fname_report)

        report_blocks = CytosimReader._parse_report_file(fname_report)

        if aggregate:
            return CytosimReader.aggregate(report_blocks)
            
        return report_blocks

    def export_xyz(self, fname: str,
                   use_fibers: bool = True,
                   use_beads: bool = True,
                   use_couples: bool = True,
                   use_singles: bool = False,
                   color_by_id: bool = False):
        n_frames = None
        if use_fibers:
            fibers = self.read_report('fiber:point')
            n_frames = len(fibers)
        if use_beads:
            beads = self.read_report('bead')
            if n_frames is None:
                n_frames = len(beads)
            else:
                assert n_frames == len(beads)
        if use_couples:
            couples = self.read_report('couple:state')
            if n_frames is None:
                n_frames = len(couples)
            else:
                assert n_frames == len(couples)
        if use_singles:
            raise NotImplementedError

        if n_frames is None:
            msg = "No data selected for export"
            raise RuntimeError(msg)

        with open(fname, 'wt') as fh:
            for i in range(n_frames):
                n_particles = 0
                block_xyz = ""
                if use_fibers:
                    if fibers[i] is not None:

                        n, b = CytosimReader._fiber_point_to_xyz(fibers[i].data, color_by_id)
                        block_xyz += b
                        n_particles += n
                if use_beads:
                    if beads[i] is not None:
                        n, b = CytosimReader._bead_to_xyz(beads[i].data)
                        block_xyz += b
                        n_particles += n
                if use_couples:
                    if couples[i] is not None:
                        n, b = CytosimReader._couple_to_xyz(couples[i].data)
                        block_xyz += b
                        n_particles += n
                block_xyz = "{}\n\n".format(n_particles) + block_xyz
                fh.write(block_xyz)

    @staticmethod
    def _fiber_point_to_xyz(fiber: pd.DataFrame, color_by_id: bool) -> Tuple[int, str]:
        id_fiber = np.array(fiber['identity'])
        fil_change = np.zeros_like(id_fiber, dtype=int)
        fil_change[0] = 1
        fil_change[1:] = id_fiber[1:] - id_fiber[:-1]
        types = np.full_like(fil_change, 'core', dtype='<U4')
        w = np.where(fil_change == 1)[0]
        types[w] = 'tail'
        types[w - 1] = 'head'

        xyz = ""
        count = fiber.shape[0]
        if color_by_id:
            line = "fiber_{} {} {} {}\n"
            for r in fiber.iterrows():
                xyz += line.format(
                    r[1]['identity'],
                    r[1]['posX'],
                    r[1]['posY'],
                    r[1]['posZ']
                )
            return count, xyz

        line = "{} {} {} {}\n"
        for r in fiber.iterrows():
            xyz += line.format(
                types[r[0]],
                r[1]['posX'],
                r[1]['posY'],
                r[1]['posZ']
            )
        return count, xyz

    @staticmethod
    def _bead_to_xyz(bead: pd.DataFrame) -> Tuple[int, str]:
        xyz = ""
        line = "bead_type_{} {} {} {}\n"
        for r in bead.iterrows():
            xyz += line.format(
                r[1]['class'],
                r[1]['posX'],
                r[1]['posY'],
                r[1]['posZ']
            )
        return bead.shape[0], xyz

    @staticmethod
    def _couple_to_xyz(couple: pd.DataFrame) -> Tuple[int, str]:
        xyz = ""
        line = "couple_{} {} {} {}\n"
        bridging = couple[(couple['fiber1'] != 0) & (couple['fiber2'] != 0)]
        for r in bridging.iterrows():
            xyz += line.format(
                r[1]['class'],
                r[1]['posX'],
                r[1]['posY'],
                r[1]['posZ']
            )
        return bridging.shape[0], xyz

    @staticmethod
    def _parse_report_file(fname) -> List['ReportBlock']:
        blocks = []
        current_block = []
        with open(fname, 'rt') as fh:
            for line in fh:
                if not line or line.isspace():
                    continue
                if line.startswith('% end'):
                    blocks.append(ReportBlock.parse(current_block))
                    current_block = []
                    continue
                current_block.append(line)
        return blocks

    def _generate_report(self, report_identifier, fname_report):
        command_args = [self.report_exe, report_identifier]
        with open(fname_report, 'wt') as fh:
            subprocess.call(command_args, cwd=self.folder, stdout=fh)

    @staticmethod
    def aggregate(
            report_blocks: List['ReportBlock']
    ) -> Union[pd.DataFrame, None]:
        cols = None
        df = None
        for block_i in report_blocks:
            if block_i is None:
                continue
            cols = block_i.data.columns
            cols = cols.insert(0, 'time').insert(0, 'frame')
            df = pd.DataFrame(columns=cols)
            break
        if cols is None:
            return None
        for block_i in report_blocks:
            if block_i is None:
                continue
            index = block_i.data.index + len(df)
            block_i.data.index = index
            df_i = pd.DataFrame(columns=cols, index=index)
            df_i['time'] = block_i.time
            df_i['frame'] = block_i.frame
            df_i[block_i.data.columns] = block_i.data[block_i.data.columns]
            df = df.append(df_i)
        return df


_reports_with_fiber_blocks = [
    'fiber:points',
    'fiber:point'
]


class ReportBlock:
    """
    Stores data of a single frame of data generated with cytosim's ``report`` executable.
    Access meta data with members ``frame``, ``time``, ``label``, ``info``, or 
    access the actual data (as a pandas.DataFrame) with member ``data``. E.g., if your
    ReportBlock object is ``block``, access data as ``block.data``.
    """

    def __init__(self, frame: int, time: float, label: str,
                 info: List[str], data: pd.DataFrame):
        self.frame = frame
        self.time = time
        self.label = label
        self.info = info
        self.data = data

    @staticmethod
    def read_data(column_names: str, data_block: str) -> pd.DataFrame:
        tf = tempfile.TemporaryFile('w+t')
        tf.write(column_names)
        tf.write(data_block)
        tf.seek(0)

        data = pd.read_csv(tf, delim_whitespace=True, comment='%')
        return data

    @staticmethod
    def parse(block: List[Lines]) -> Union['ReportBlock', None]:
        frame = ReportBlock._parse_frame(block[0])
        time = ReportBlock._parse_time(block[1])
        label = ReportBlock._parse_label(block[2])
        first_data_line = None
        for i in range(3, len(block)):
            if block[i].startswith('%'):
                continue
            first_data_line = i
            break
        if first_data_line is None:
            return None
        if label in _reports_with_fiber_blocks:
            info = block[3: first_data_line-2]
            column_names = block[first_data_line-2][2:]
            data_block = ''.join(block[first_data_line:])
            df = ReportBlock.read_data(column_names, data_block)
            return ReportBlock(frame, time, label, info, df)

        info = block[3: first_data_line - 1]
        column_names = block[first_data_line - 1][2:]
        data_block = ''.join(block[first_data_line:])
        df = ReportBlock.read_data(column_names, data_block)
        return ReportBlock(frame, time, label, info, df)

    @staticmethod
    def _parse_frame(line) -> int:
        s = line.split()
        assert s[1] == 'frame', "This line does not contain the current frame number."
        return int(s[2])

    @staticmethod
    def _parse_time(line) -> float:
        s = line.split()
        assert s[1] == 'time', "This line does not contain the time of the current frame."
        return float(s[2])

    @staticmethod
    def _parse_label(line):
        s = line.split()
        assert s[1] == 'report', "This line does not contain the report label."
        return ' '.join(s[2:])

    def __str__(self):
        return "ReportBlock \"{}\", frame {}".format(self.label, self.frame)

    def __repr__(self):
        return self.__str__()

