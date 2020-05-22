import argparse
import os
import sys

import pyconrad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev-path', nargs='*',
                        help="Path to CONRAD or CONRADRSL folder (root for classpath). "
                        "Default: current working directroy")
    parser.add_argument(
        'class_with_main', help="Java class with main (e.g. edu.stanford.rsl.apps.gui.ReconstructionPipelineFrame)")
    parser.add_argument('args', nargs='*', help="CLI arguments")
    parser.add_argument('--gui', action='store_true',
                        help="Activate this flag for GUI applications")
    parser.add_argument('--show-jvm-args', action='store_true',
                        help="Shows launch arguments for JVM for debugging")

    args = parser.parse_args()
    if not args.dev_path:
        args.dev_path = [os.getcwd()]
    pyconrad.setup_pyconrad(dev_dirs=args.dev_path)
    if args.show_jvm_args:
        print(pyconrad._pyconrad.PyConrad().jvm_args)

    for dir in args.dev_path:
        sys.path.append(dir)

    if args.gui:
        pyconrad.start_gui()

    args.class_with_main = args.class_with_main.replace('/', '.')
    args.class_with_main = args.class_with_main.replace('\\', '.')
    if args.class_with_main.startswith('src'):
        args.class_with_main = args.class_with_main.replace('src.', '', 1)

    runable_class = pyconrad.JClass(args.class_with_main)
    runable_class.main(args.args)


if __name__ == '__main__':
    main()
