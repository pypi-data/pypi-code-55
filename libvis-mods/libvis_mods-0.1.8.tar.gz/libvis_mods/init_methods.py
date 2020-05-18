from cookiecutter.main import cookiecutter

from libvis_mods.paths_config import (
    files_template, dirs_template
)

def init_file(name, output_dir='.', **kwargs):
    _install_template(files_template,
                      name=name, output_dir=output_dir,
                      **kwargs)

def init_dir(name, output_dir='.', **kwargs):
    _install_template(dirs_template,
                      name=name, output_dir=output_dir,
                      **kwargs)

def init(name, output_dir='.', **kwargs):
    init_dir(name, output_dir, **kwargs)

def _install_template(template, interactive=False, **kwargs):
    out_dir = kwargs.pop('output_dir')
    print(template, kwargs, out_dir)
    cookiecutter(str(template),
                 output_dir=out_dir,
                 extra_context=kwargs,
                 no_input=not interactive
                )
