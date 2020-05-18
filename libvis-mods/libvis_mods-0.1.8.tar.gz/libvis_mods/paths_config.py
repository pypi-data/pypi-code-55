from pathlib import Path
import importlib
import libvis_mods

def get_libvis_path():
    """ Try to find libvis, if not found
        try to import and raise ModuleNotFoundError
    """
    spec = importlib.util.find_spec('libvis')
    if spec is None:
        # Failed to find 'libvis'
        raise ModuleNotFoundError("No module named 'libvis'")
    return Path(spec.submodule_search_locations[0])

# Sources
manager_path = Path(libvis_mods.__file__).parent
web_src = manager_path / 'web'
web_user_mods = web_src /'src'/ 'modules' / 'presenters' / 'installed'

# Target
vis_dir = get_libvis_path()
build_dir = vis_dir / 'front_build'
python_user_mods = vis_dir / 'modules' / 'installed'

# Project templates
templates_path = manager_path / 'project-templates'
files_template = templates_path / 'source-files'
dirs_template = templates_path / 'source-dirs'
