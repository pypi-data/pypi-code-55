import sys
import random
import argparse
import configparser
from pathlib import Path
from colorama import init, Fore
from hpass.hpass_gui import gui_start

init(autoreset=True)

h_pass_dir = Path(__file__).resolve().parents[0]
config_dir = h_pass_dir / 'config.ini'


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(description='Hello Password')
    parser.add_argument('-v', '--version', help='查看版本信息', action='version', version='%(prog)s v0.0.2')
    parser.add_argument('-r', '--random_password', help='随机生成包含大小写字母/数字/符号的密码 (E.g hpass -r 10)', action='store',
                        dest='password_length')
    parser.add_argument('-i', '--initialization', help='在当前目录下创建一个新的密码存储文件', action='store', dest='file_name')
    parser.add_argument('-g', '--gui', help='启动GUI工作台', action='store', dest='primary_password')
    args = parser.parse_args()
    if args.file_name:
        file_name = args.file_name
        cf = configparser.ConfigParser()
        cf.add_section("deploy")
        cf.set('deploy', 'file', file_name)
        with open(str(config_dir), "w+") as f:
            cf.write(f)
    if args.password_length:
        try:
            _password_length = int(args.password_length)
            base_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'h', 'j', 'k', 'l',
                         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4',
                         '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*']
            rp = ''
            for j in range(_password_length):
                m = random.randint(0, len(base_char) - 1)
                rp = rp + base_char[m]
            print(Fore.GREEN + rp)
        except ValueError:
            print(Fore.RED + '参数 password_length 需要一个数字 (E.g hpass -r 16)')
    if args.primary_password:
        gui_start()


if __name__ == '__main__':
    main()
