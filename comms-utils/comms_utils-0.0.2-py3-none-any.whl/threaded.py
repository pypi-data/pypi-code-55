import os
import copy
import threading
from typing import List
import comms_utils.decode as decode
from comms_utils.signal import Signal 
from comms_utils.ak import AK 
import comms_utils.psd as psd
import numpy as np

def run_sy(sy, x: List[float], rc: List[List[float]], rc_lock, thread_id: int):
    output = list()
    print('thread: {} started'.format(thread_id))
    for val in x:
        output.append(sy[float(val)])
    with rc_lock:
        print('thread: {} finished'.format(thread_id))
        rc[thread_id] = output

def sy(sy, x: List[float]) -> List[float]:
    num_threads = os.cpu_count()
    threads = list()
    rc = [[0.0]] * num_threads
    rc_lock = threading.Lock()
    x_split = np.array_split(x, num_threads)
    thread_id = 0
    for sub_x in x_split:
        thread = threading.Thread(None, run_sy, args=[sy, sub_x, rc, rc_lock, thread_id])
        threads.append(thread)
        thread_id += 1
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    output = list()
    for item in rc:
        output.extend(item)
    return output

def calc_errors(y: List[float], ak: AK, i: int, original_bin: np.ndarray,
        clock_comb: List[float], signal: Signal, db: float, rc_lock):
        
    signal.add_noise(db)
    decoded_data = decode.decode_pam(signal*clock_comb, ak.get_levels())
    bit_array = np.array(list(decoded_data), dtype=int)
    bit_errors = np.sum(bit_array != original_bin)
    bit_error_rate = bit_errors / len(ak)
    with rc_lock:
        y[i] = bit_error_rate
    signal.remove_noise()

def calc_errors_threaded(db_array: List[float], y: List[float], ak: AK,
        original_bin: np.ndarray, clock_comb: List[float],
        signal: Signal) -> List[float]:
    
    y = [0] * len(db_array)
    num_threads = os.cpu_count()
    threads = list()
    rc_lock = threading.Lock()
    thread_id = 0
    i = 0
    while i < len(db_array):
        for _ in range(num_threads):
            if i == len(db_array)-1:
                continue
            thread = threading.Thread(None, calc_errors, args=[y, ak, i,
                original_bin, clock_comb, copy.deepcopy(signal), db_array[i], rc_lock])
            threads.append(thread)
            thread_id += 1
            i += 1
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        threads = list()
    return y