import numpy as np
import pandas as pd
from subprocess import check_call


def export_to_txt(f_name, txt_f_name):
    """
    Converts pcap file into txt with packets features

    :param f_name: str
        filename of source pcap file
    :param txt_f_name: str
        filename of target file
    """
    cmd = "tshark -T fields -e frame.time_relative -e ip.src -e udp.srcport -e udp.dstport -e udp.length -r %s > %s" % (
        f_name, txt_f_name)
    check_call(cmd, shell=True)


# Delete not udp from txt and save to csv with -udp ending
def delete_non_udp(f_name, output_filename, header_names):
    """
    Delete non-udp packets from csv and export it to csv file with -udp ending in name

    :param f_name: str
        filename of source txt file
    :param header_names: list
        of column names from file
    """
    dataset = pd.read_csv(f_name, delimiter='\t', header=None, names=header_names)
    dataset.replace(' ', np.nan, inplace=True)
    dataset = dataset.dropna()
    dataset.to_csv(output_filename, sep='\t', index=False)
