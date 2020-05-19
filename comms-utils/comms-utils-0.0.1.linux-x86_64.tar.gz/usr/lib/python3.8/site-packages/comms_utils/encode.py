import numpy as np

def encode_pam(data: str, levels: int):
    binary_data = ''.join(format(ord(char), 'b').zfill(7) for char in data)
    encoded_data = bin_to_pam(binary_data, levels)
    return encoded_data

def encode_pam_file(file_name: str, levels: int):
    with open(file_name, 'r') as report:
        message = report.read()
        signal = encode_pam(message, levels)
    return signal

def bin_to_pam(binary_data, levels: int):
    max_val = levels
    levels = np.log2(levels)
    levels = int(levels)
    encoded_data = [int(binary_data[i:i+levels], 2) for i in range(0, len(binary_data), levels)]
    output_data = [i-(max_val-1-i) for i in encoded_data]
    return output_data

if __name__ == "__main__":
    print(bin_to_pam('0010110111', 2))
