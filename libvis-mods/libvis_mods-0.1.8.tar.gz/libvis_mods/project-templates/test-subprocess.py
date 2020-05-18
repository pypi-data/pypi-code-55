import subprocess
import sys

cmd = ['cookiecutter','source-files']
cmd += sys.argv[1:]

def main():
    subprocess.call(cmd)

if __name__ == '__main__':
    main()
