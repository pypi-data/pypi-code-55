import click
import subprocess
import pydotplus
from pathlib import Path
from veazy import Veazy
import os

@click.command()
@click.argument('src', nargs=-1, type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--output-file', 'dst', type=click.Path(writable=True, resolve_path=True))
@click.option('-c', '--complexity-offset', type=int, default=0)
@click.option('-d', '--depth', type=int)
@click.option('-t', '--output-type',
              type =click.Choice(['dot', 'svg'], case_sensitive = False),
              default = 'svg')
def cli(src, dst, complexity_offset, depth, output_type):
    """Its a wrap. For direct use in pytest."""
    _cli(src, dst, complexity_offset, depth, output_type)

def _cli(src, dst, complexity_offset, depth, output_type):
    input_files, main_dir = get_all_files(src)

    cmd = [
        f'cd "{main_dir}"; '
    	'pyan3',
    	*input_files,
    	'--uses --no-defines --colored --nested-groups --annotated --dot'
	]

    dot_lines = (
    	subprocess
    	.run(' '.join(cmd), shell = True, stdout=subprocess.PIPE)
    	.stdout
    	.decode('utf-8')
	)

    pygraph = pydotplus.graphviz.graph_from_dot_data(dot_lines)
    vh = Veazy(pygraph)

    if not depth:
        depth = vh.max_depth + complexity_offset
    
    # now process this graph
    output = vh.get_pruned_graph(depth)
    
    if output_type == 'dot':
        if not dst:
            click.echo(output.to_string())
        else:                
            with open(dst, 'w') as fo:
                fo.write(output.to_string(), '\n')
    else:
        if dst==None:
            dst = 'graph.svg'
        output.write_svg(dst)
        click.launch(f'{dst}', wait=True)
        
    click.echo(f'Veazy is done after going {depth} deep. Bleeep.')
    return 0


def get_all_files(src):
    """
    src is a tuple of files and directories. 
    Directories are recursively expanded for all contained .py files. 
    When src is empty, use '.'.
    """


    if len(src)==0:
        src = '.'
    dirs = [d for d in src if Path(d).is_dir()]
    nondirs = [Path(f) for f in src if not Path(f).is_dir()]
    exp_dir = [file for d in dirs for file in Path(d).rglob('*.py')] 
    files = [str(x.resolve()) for x in set(exp_dir + nondirs)]
    # first sort alphabetically
    files.sort()
    # then sort on file depth
    depth = [i.count("/") for i in files]
    files = [i for _, i in sorted(zip(depth, files))]
    files.reverse()
    # finally strip unnecessary prefixes
    prefix = os.path.commonprefix(files)
    files = [i[len(prefix):] for i in files]

    return files, prefix

if __name__ == '__main__':
	cli()
