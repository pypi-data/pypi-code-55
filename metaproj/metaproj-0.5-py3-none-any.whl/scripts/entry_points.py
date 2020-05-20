import argparse
from ..context import MetaProj

def pyproj():

    parser = argparse.ArgumentParser(description='To Create a Standard Python Project')
    parser.add_argument("name", type=str, help="The PROJECT Name")
    parser.add_argument("-t", "--type", type=str, default='python', choices=['python', 'cpp'], help="Project Type")
    args = parser.parse_args()

    proj_name = args.name

    mp = MetaProj()
    mp.setName(proj_name)
    mp.setType(args.type)
    mp.run()
    
def vimconf():

    parser = argparse.ArgumentParser(description='To Create a Standard Python Project')
    parser.add_argument("-o", "--output", type=str, default='~', help="The Output File Name")
    args = parser.parse_args()

    mp = MetaProj()
    mp.setName(args.output)
    mp.setType('vim')
    mp.run()

def vimprepare():

    # parser = argparse.ArgumentParser(description='To Create a Standard Python Project')
    # parser.add_argument("-o", "--output", type=str, default='~', help="The Output File Name")
    # args = parser.parse_args()

    mp = MetaProj()
    # mp.setName(args.output)
    mp.setType('vimdep')
    mp.run()
