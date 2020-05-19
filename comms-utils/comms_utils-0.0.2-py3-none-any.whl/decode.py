import numpy as np
from typing import List

def decode_pam(incoming_data: List[float], levels: int):
    max_val = (levels-1)
    sampled_data = list()
    for data in incoming_data:
        if data != 0:
            sampled_data.append(data)
    level_options = [i-(levels-1-i) for i in range(0, levels)]
    levels = int(np.log2(levels))
    bit_str = ""
    for level_val in sampled_data:
        level_val = min(level_options, key=lambda x:abs(x-level_val))
        level_val = level_val + max_val
        level_val = int(level_val / 2)
        bit_str = bit_str + bin(level_val)[2:].zfill(levels)
    return bit_str

def decode_pam_file(incoming_data: List[int], file_name: str, levels: int):
    decoded_data = decode_pam(incoming_data, levels)
    with open(file_name, 'w+') as output:
        output.writelines(decoded_data)

def decode_pam_string(incoming_data: List[float], levels: int) -> str:
    bit_str = decode_pam(incoming_data, levels)
    message = ''.join(char for char in [chr(int(bit_str[i:i+7], 2)) for i in range(0, len(bit_str), 7)])
    return message

if __name__ == "__main__":
    print(decode_pam([], 16))
