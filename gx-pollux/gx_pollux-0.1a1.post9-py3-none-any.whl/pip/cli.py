import os, sys
import typer
from pollux import inputer
from pollux.license import license_setup, license_text
import pollux.pip.utils as putils

main = typer.Typer()


@main.command()
def init(name: str):
    """
    Init a new pip project with given name
    :param name: Project name
    """
    setup_dict = dict()
    pwd = os.getcwd()
    project_path = os.path.join(pwd, name)
    typer.echo(f"Init Project {name} in {project_path}")
    os.mkdir(project_path)
    os.chdir(project_path)  # cd {name}
    typer.echo("Collecting necessary information...")
    lic = inputer.select_license()
    if lic != 'n':
        whole_lic = license_text[lic]
        lic_setup = license_setup[lic]
        setup_dict['license'] = lic_setup
        with open('LICENSE', 'w') as lis:
            print(whole_lic, file=lis)
        print("LICENSE file created!")
    py_version = inputer.input_py_version()
    setup_dict['python'] = py_version
    setup_dict['author'] = input("Please input author name:\n")
    setup_py = putils.build_setup(name=name,
                                  lic=setup_dict['license'],
                                  author=setup_dict['author'])
    with open('setup.py', 'w') as spy:
        print(setup_py, file=spy)
    print("setup.py created!")
    with open('.gitignore', 'w') as ig:
        print(putils.gitignore, file=ig)
    with open("VERSION", 'w') as ver:
        print('0.1a1', file=ver)
    print("Operation finished!")


@main.command()
def build(i: bool = typer.Option(
        default=False,
        help="If True, Install package after building"
), cl: bool = True):
    """
    Build wheel
    """
    # python setup.py sdist
    # python setup.py bdist_wheel
    pkg_path = os.path.join(os.getcwd(), 'dist')  # $(pwd)/dist
    if cl:
        # remove all files in pkg_path
        os.system(f"rm {pkg_path}/*.whl")
    cmd = "python setup.py bdist_wheel"
    os.system(cmd)
    if i:
        os.system(f"pip install -U {pkg_path}/*.whl")


@main.command()
def install():
    """
    Install .whl
    """
    pkg_path = os.path.join(os.getcwd(), 'dist')  # $(pwd)/dist
    os.system(f"pip install -U {pkg_path}/*.whl")


@main.command()
def clean():
    """
    remove dist directory
    """
    pkg_path = os.path.join(os.getcwd(), 'dist')  # $(pwd)/dist
    os.system(f"rm {pkg_path}/*.whl")


@main.command()
def upload():
    """
    Upload file to pypi
    """
    pass
