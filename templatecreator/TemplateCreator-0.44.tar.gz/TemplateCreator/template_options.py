from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TemplateInfo:
    # name should be the same as template file name (no extension)
    name: str
    # name of the file to create
    file_name: Optional[str]
    # if set to true a directory will be created
    is_batch: bool = field(default=True)
    # suffix appended to class names
    suffix: str = field(default='')


@dataclass
class Suffixes:
    component = 'Component'
    reducer = 'Reducer'
    service = 'Service'
    state = 'State'


@dataclass
class TemplateOptions:
    shared_component: TemplateInfo
    function_component: TemplateInfo
    ts_function_component: TemplateInfo
    class_component: TemplateInfo
    styles: TemplateInfo
    css_module: TemplateInfo
    readme: TemplateInfo
    test: TemplateInfo
    state: TemplateInfo
    actions: TemplateInfo
    ts_actions: TemplateInfo
    ts_state: TemplateInfo
    ts_connected_component: TemplateInfo
    ts_reducer: TemplateInfo
    reducer: TemplateInfo
    service: TemplateInfo

    def __init__(self, folder_name: str):
        self.shared_component = TemplateInfo(
            name='shared-component',
            file_name=None
        )
        self.ts_state = TemplateInfo(
            name='ts-state',
            file_name=None
        )
        self.ts_reducer = TemplateInfo(
            name='ts-reducer',
            file_name=f'{folder_name}.reducer.ts',
        )
        self.function_component = TemplateInfo(
            name='function-component',
            file_name=f'{folder_name}.component.jsx',
            suffix=Suffixes.component
        )
        self.class_component = TemplateInfo(
            name='class-component',
            file_name=f'{folder_name}.component.jsx',
            suffix=Suffixes.component
        )
        self.styles = TemplateInfo(name='styles', file_name=f'{folder_name}.styles.js')
        self.css_module = TemplateInfo(name='css-module', file_name=f'{folder_name}.styles.scss')
        self.readme = TemplateInfo(
            name='readme',
            file_name=f'{folder_name}.readme.md',
            suffix=Suffixes.component
        )
        self.test = TemplateInfo(
            name='test',
            file_name=f'{folder_name}.test.jsx',
            suffix=Suffixes.component
        )
        self.state = TemplateInfo(
            name='state',
            file_name=f'{folder_name}.state.js',
            suffix=Suffixes.state
        )
        self.actions = TemplateInfo(name='actions', file_name=f'{folder_name}.actions.js')
        self.reducer = TemplateInfo(
            name='reducer',
            file_name=f'{folder_name}.reducer.js',
            suffix=Suffixes.reducer
        )
        self.service = TemplateInfo(
            name='service',
            file_name=f'{folder_name}.service.js',
            suffix=Suffixes.service,
            is_batch=False
        )
        self.ts_function_component = TemplateInfo(
            name='ts-function-component',
            file_name=f'{folder_name}.component.tsx',
            suffix=Suffixes.component,
            is_batch=True
        )
        self.ts_connected_component = TemplateInfo(
            name='ts-connected-component',
            file_name=f'{folder_name}.component.tsx',
            suffix=Suffixes.component,
            is_batch=True
        )
        self.ts_actions = TemplateInfo(
            name='ts-actions',
            file_name=f'{folder_name}.actions.ts'
        )
        self.ts_state = TemplateInfo(
            name='ts-state',
            file_name=f'{folder_name}.state.ts'
        )

    def get_suffix(self, template_name):
        try:
            template = self.get_template_info(template_name)
            return template.suffix
        except ModuleNotFoundError:
            return ""

    def get_template_info(self, template_name) -> Optional[TemplateInfo]:
        try:
            return self.__getattribute__(template_name)
        except ModuleNotFoundError:
            return None

    def get_batch_templates_dictionary(self):
        return {
            'shared-component': [
                self.function_component,
                self.styles,
                self.readme,
                self.test
            ],
            'class-component': [
                self.class_component,
                self.css_module
            ],
            'function-component': [
                self.function_component,
                self.css_module
            ],
            'ts-function-component': [
                self.ts_function_component,
                self.styles
            ],
            'ts-connected-component': [
                self.ts_connected_component,
                self.styles
            ],
            'ts-state': [
                self.ts_actions,
                self.ts_state,
                self.ts_reducer
            ],
            'state': [
                self.state,
                self.reducer,
                self.actions
            ],
            'service': [
                self.service
            ]
        }
