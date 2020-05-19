__version__ = "0.0.30"

import argparse
import json
import os.path
import glob

def findfile( path, suffixes, args):
  # finds files recursively with supplied file suffix
  l = []
  if os.path.isdir(path):
    for fname in  glob.glob(path+'/*'):
      if args.verbose:
        print('found file {}'.format(fname))
      l.extend( findfile( fname ,suffixes, args) )
  else:
    if os.path.basename( path ).split( '.' )[-1] in  suffixes:
      l.append(path)
    
    #else:
    #  if args.verbose:
    #    print('wrong suffix', os.path.basename( path ).split( '.' )[-1], suffixes)
  return( l ) 

def tidypath(path):
  return os.path.abspath(os.path.expanduser(path))

def ask_project_dir(args):
  while True:  
    print ('Enter project directory: <q quits> ')
    project =  input('path:')
    if project == 'q':
      print('Quitting')
      raise SystemExit 
    return project

def ask_project_indir(args):
  while True:  
    print ('Enter location of input images: <q quits> ')
    indir =  input('path:')
    if indir == 'q':
      print('Quitting')
      raise SystemExit
    return indir

def main(args):
  
  if args.project is None:
    cfile = tidypath('limu.conf')
    if os.path.isfile(cfile ):
      args.project = os.path.dirname(cfile)
    else:     
      args.project = ask_project_dir(args)
  args.project = tidypath(args.project)

  if not os.path.isdir(args.project): 
    os.mkdir(args.project)

  args.conf_file= tidypath("{}/limu.conf".format(args.project))

 
  if os.path.isfile(args.conf_file):
    with open(args.conf_file, 'r') as fobj:
      conf_dict = json.load(fobj)
    for key, value in conf_dict.items():
      if key in args.__dict__.keys():
        if (args.__dict__[key] is None) or (args.__dict__[key] == False):
          args.__dict__[key] = value
      else:
        args.__dict__[key] = value
 
  else:
    if args.indir is None:
      args.indir = ask_project_indir(args)

    for sdir in ['datafiles','figures','imagesteps','outdata']:
      tmp = "{}/{}".format(args.project, sdir)
      args.__dict__[sdir] = tmp
      if not os.path.isdir(tmp):
        os.mkdir(tmp)

    with open(args.conf_file, 'w') as fobj:
      json.dump(args.__dict__, fobj, indent=4)
  
  # look for files 
  filesuffixes = ['cr2', # canon raw
                 'jpg','jpeg',
                 'png',
                 'tif','tiff',
                  ]
  uppercase = [suffix.upper() for suffix in filesuffixes]
  filesuffixes.extend(uppercase)
  infiles = findfile(args.indir,filesuffixes,args)
   
  
  
def cli():
  parser = argparse.ArgumentParser(
      prog='limu' ,
      description="""
        Tool to analyse images of cleared 
        and troptophan stained leaves to 
        assess leaf damage.
        """,
      epilog="Good luck analysing!")

  parser.add_argument(
    '-p', '--project', required=False, 
      type=str, 
      dest='project',
      help='path to projects directory, if not supplied one will be requested interactively. If limu.conf file found in current working directory, this will be used')
  parser.add_argument(
    '-i', '--input-dir', required=False, 
      type=str, 
      dest='indir', 
      help='path to infile root directory')

  parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='Print more stuff'
    )
  parser.add_argument(
        '-r', '--recalculate',
        dest='recalculate',
        action='store_true',
        help='Force recalculation'
    ) 

  args = parser.parse_args()
  main(args)
 
if __name__ == '__main__':
  cli()
    
