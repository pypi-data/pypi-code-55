import numpy as np
from scipy import special
from typing import List
import matplotlib.pyplot as plt
from comms_utils.ak import AK
from comms_utils.pulse import Pulse
from comms_utils.signal import Signal
from comms_utils.comb import Comb
import comms_utils.threaded as threaded
import comms_utils.decode as decode

def eye_diagram(signal: Signal, pulse: Pulse, clock_comb: List[float], num_periods:
        int=3, plot_sample_lines: bool=False, title: str=None, pgf_plot: str=None):
    corrected_clock = pulse.apply_conv_delay(len(signal), clock_comb)
    start_index = corrected_clock.index(1.0)
    finish_index = len(corrected_clock) - corrected_clock[::-1].index(1.0)
    sig_data, sig_time = signal.get_data()
    count = 0
    
    clock_edges = np.where(np.array(corrected_clock, dtype=float)==1.0)[0]
    last_clock = clock_edges[0]
    period = np.array(sig_time[last_clock:clock_edges[num_periods]]) - sig_time[last_clock]
    if plot_sample_lines == True:
        for i in range(1, num_periods):
            time = sig_time[clock_edges[i]]-sig_time[last_clock]
            plt.axvline(x=time, color='r', linestyle='--')
    for i in clock_edges[1:]:
        count += 1
        if count == num_periods:
            plt.plot(period, sig_data[last_clock:i])
            last_clock = i
            count = 0
    if title != None:
        plt.title(title)
    else:
        plt.title("{}-PAM Eye Diagram".format(signal.get_levels()))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    if pgf_plot != None:
        plt.savefig(pgf_plot)
    else:
        plt.show()


def calc_errors(y: List[float], ak: AK, original_bin: np.ndarray,
        comb: Comb, signal: Signal, pulse: Pulse, db: float):
    signal.add_noise(db)
    recv_sig = signal.convolve(pulse)
    delayed_clock = pulse.apply_conv_delay(len(recv_sig), comb.get_clock_comb())

    decoded_data = decode.decode_pam(recv_sig*delayed_clock, ak.get_levels())
    bit_array = np.array(list(decoded_data), dtype=int)
    bit_errors = np.sum(bit_array != original_bin)
    bit_error_rate = bit_errors / len(ak)
    y.append(bit_error_rate)
    signal.remove_noise()


def analytical_bit_error(db_array: List[float], ak: AK, title: str=None):
    numerical = list()
    for db in db_array:
        db_num = 10 ** (db/10)
        numerical.append(0.5*special.erfc(np.sqrt(db_num)))
    plt.plot(db_array, numerical, '-b')
    plt.yscale("log")
    plt.grid(True, which='both')
    plt.xlabel("$E_b/N_0$ (dB)")
    plt.ylabel("BER")
    if title == None:
        plt.title("{}-PAM Bit Error Rate".format(ak.get_levels()))
    else:
        plt.title(title)
    plt.show()


def bit_errors(signal: Signal, comb: Comb, pulse: Pulse, db_array: List[float], title: str=None, 
        numerical_line: bool=False, pgf_plot: str=None, threading: bool=False):
    ak = comb.get_ak()
    original_bin = decode.decode_pam(ak.get_data(), ak.get_levels())
    original_bin = np.array(list(original_bin), dtype=int)
    if signal.get_snr_db() != None:
        signal.remove_noise()
        print("Removed initial noise from signal")
    y = list()
    numerical = list()
    if threading == True:
        threaded.calc_errors_threaded(db_array.copy(), y, ak, original_bin,
            comb, signal)
    else:
        for db in db_array:
            if numerical_line == True:
                db_num = 10 ** (db/10)
                numerical.append(0.5*special.erfc(np.sqrt(db_num)))
            calc_errors(y, ak, original_bin, comb, signal, pulse, db)
    plt.plot(db_array, y, 'o-b')
    if numerical_line == True:
        plt.plot(db_array, numerical, '--r')
    plt.yscale("log")
    plt.grid(True, which='both')
    plt.xlabel("$E_b/N_0$ (dB)")
    plt.ylabel("BER")
    
    if title != None:
        plt.title(title)
    else:
        plt.title("{}-PAM Bit Error Rate".format(ak.get_levels()))
    if pgf_plot != None:
        plt.savefig(pgf_plot)
    else:
        plt.show()
    



