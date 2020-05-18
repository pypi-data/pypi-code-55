from typing import Dict, Any, Optional, Union, Callable, Type, Sequence

from pyfileconf import Selector, PipelineManager


class PFCRunner:

    def __init__(self):
        self.s = Selector()

    def run(self, path: str) -> Any:
        path_parts = path.split('/')
        if len(path_parts) < 2:
            raise ValueError(f'got invalid path {path}')
        manager_name = path_parts[0]
        run_path = '.'.join(path_parts[1:])
        manager = self.managers[manager_name]
        return manager.run(run_path)

    def create(self, section_path: str, func_or_class: Optional[Union[Callable, Type]] = None):
        path_parts = section_path.split('.')
        if len(path_parts) < 2:
            raise ValueError(f'got invalid section path {section_path}')
        manager_name = path_parts[0]
        create_path = '.'.join(path_parts[1:])
        manager = self.managers[manager_name]
        return manager.create(create_path, func_or_class)

    @property
    def managers(self) -> Dict[str, PipelineManager]:
        return self.s._managers

    def reload(self, manager_names: Optional[Sequence[str]] = None):
        for manager in self.managers.values():
            if manager_names and manager.name not in manager_names:
                continue
            manager.reload()

