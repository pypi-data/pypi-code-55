import os
import hashlib


def whatever():
    custom_file="mario_custom_output.txt"
    checksum_file="checksums.txt"

    # get a list of all checksums in custom_file
    # go through every checksum in checksum file, see if it exists in list

    custom_file_handler = open(custom_file, "r")
    checksum_file_handler = open(checksum_file, "r")

    custom_checksums_list = []
    for cc in custom_file_handler:
        mapping = cc.split("  -->  ")
        custom_checksums_list.append(str(mapping[1]).strip())
    confirmed_checksums_list = []
    confirmed_mapping = {}
    for cf in checksum_file_handler:
        mapping = cf.split()
        confirmed_checksums_list.append(mapping[-1])
        confirmed_mapping[str(mapping[0]).strip()] = mapping[1]

    i = 0
    missing = []
    for conf in confirmed_mapping:
        if conf not in custom_checksums_list:
            missing.append(confirmed_mapping[conf])
            missing.append(conf)

    print(missing)

def all_hashes():
    checksum_file = "checksums.txt"
    confirmed_checksums_list = {}
    checksum_file_handler = open(checksum_file, "r")
    for cf in checksum_file_handler:
        payload = cf.split()
        confirmed_checksums_list[payload[0]] = payload[1]
    checksum_file_handler.close()
    subs_list = ["ROMS"]
    for rootdir in subs_list:
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                hash_md5 = hashlib.md5()
                with open(os.path.join(subdir, file), "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                d = str(hash_md5.hexdigest())
                if d in confirmed_checksums_list:
                    del confirmed_checksums_list[d]
                
    
    for keys in confirmed_checksums_list:
        print(confirmed_checksums_list[keys], " missing!")

all_hashes()
#Asteroids (1981) (Atari, Brad Stewart - Sears) (CX2649 - 49-75163) ~.bin  -->  dd7884b4f93cab423ac471aa1935e3df
#Asteroids (1981) (Atari, Brad Stewart - Sears) (CX2649 - 49-75163) [no copyright] ~.bin  -->  ccbd36746ed4525821a8083b0d6d2c2c