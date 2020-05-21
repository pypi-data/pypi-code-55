try:
    from sniffer import Sniffer
except ImportError:
    from .sniffer import Sniffer
from time import sleep

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--interface", help="specify interface type", default="enp4s0")
parser.add_argument("--filter_protocol", help="specify filtered protocol type", default="icmp")
parser.add_argument("--mongo_protocol", help="specify mongo port", default=27017)
args = parser.parse_args()


def main():

    sniffer = Sniffer(**vars(args))
    print("[*] Start sniffing...")
    sniffer.start()
    try:
        while True:
            sleep(100)
    except KeyboardInterrupt:
        print("[*] Stop sniffing")
        sniffer.join(2.0)

        if sniffer.is_alive():
            sniffer.socket.close()


if __name__ == "__main__":
    main()
