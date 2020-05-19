from pathlib import Path
import pkgutil
from typing import Dict, List, Optional, Any

from delairstack.core.errors import ResponseError
from tabulate import tabulate
import typer
import yaml

from delairstack_cli import utils
from delairstack_cli.sdk import delairstack_sdk


app = typer.Typer()


class Input:
    def __init__(self, name: str, *, display_name: str, description: str,
                 required: bool, source: Dict = None, scheme: Dict = None):
        self.name = name
        self.display_name = display_name
        self.required = required
        self.description = description
        if source:
            if source.get('scheme'):
                utils.check_json_schema(source['scheme'])
        self.source = source
        if scheme:
            utils.check_json_schema(scheme)
        self.scheme = scheme

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        kind = str(yaml_desc.get('kind'))
        scheme: Dict[str, Any]
        source: Dict[str, Any]

        if kind == 'dataset':
            scheme = {
                'type': 'string',
                'pattern': '^[0-9a-f]{24}$'
            }
        elif kind == 'dataset-array':
            scheme = {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'pattern': '^[0-9a-f]{24}$'
                }
            }
        else:
            raise KeyError('kind {!r} not supported'.format(kind))

        source = {
            'service': 'data-manager',
            'resource': 'dataset'
        }

        dataset_schema = yaml_desc.get('schema')
        if dataset_schema:
            source.update({
                'scheme': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                }
            })
            for prop_name, possible_values in dataset_schema.items():
                if prop_name == 'categories':
                    if not possible_values:
                        # Ignore categories if empty
                        continue

                    source['scheme']['properties'][prop_name] = {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'contains': {'enum': possible_values}
                    }
                elif prop_name == 'type':
                    source['scheme']['properties'][prop_name] = {
                        'const': possible_values
                    }
                elif prop_name == 'source':
                    source['scheme']['properties']['source'] = {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'const': possible_values
                            }
                        }
                    }
                else:
                    raise KeyError('{!r} not supported'.format(prop_name))
                source['scheme']['required'].append(prop_name)

        return cls(
            name=str(yaml_desc.get('name')),
            display_name=str(yaml_desc.get('display-name')),
            required=bool(yaml_desc.get('required')),
            description=str(yaml_desc.get('description')),
            scheme=scheme,
            source=source
        )


class Deliverable(Input):
    pass


class Parameter:
    def __init__(self, name: str, *, display_name: str, description: str,
                 required: bool, scheme: Dict = None, default_value: Optional[Any]):
        self.name = name
        self.display_name = display_name
        self.required = required
        self.description = description
        if scheme:
            utils.check_json_schema(scheme)
        self.scheme = scheme
        self.default_value = default_value

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        scheme = yaml_desc.get('schema')
        if scheme:
            default_value = scheme.get('default')
        return cls(
            name=str(yaml_desc.get('name')),
            display_name=str(yaml_desc.get('display-name')),
            required=bool(yaml_desc.get('required')),
            description=str(yaml_desc.get('description')),
            scheme=scheme,
            default_value=default_value
        )


class Analytic:
    def __init__(self, name: str, *, display_name: str, description: str,
                 docker_image: str,
                 instance_type: Optional[str] = None,
                 volume_size: Optional[int] = None,
                 tags: Optional[List[str]] = None, groups: List[str] = None,
                 inputs: Optional[List[Input]] = None,
                 parameters: Optional[List[Parameter]] = None,
                 deliverables: Optional[List[Deliverable]] = None):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.docker_image = docker_image
        self.instance_type = instance_type
        self.volume_size = volume_size
        self.tags = tags
        self.groups = groups
        self.inputs = inputs
        self.parameters = parameters
        self.deliverables = deliverables

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        creation_params: Dict[str, Any]
        creation_params = {
            'name': str(yaml_desc.get('name')),
            'display_name': str(yaml_desc.get('display-name')),
            'description': str(yaml_desc.get('description')),
            'docker_image': str(yaml_desc.get('docker-image')),
            'volume_size': yaml_desc.get('volume-size'),
            'instance_type': yaml_desc.get('instance-type'),
            'tags': yaml_desc.get('tags'),
            'groups': yaml_desc.get('groups'),
        }
        yaml_inputs = yaml_desc.get('inputs')
        if isinstance(yaml_inputs, list):
            creation_params['inputs'] = [Input.from_yaml(i) for i in yaml_inputs]
        yaml_deliv = yaml_desc.get('deliverables')
        if isinstance(yaml_deliv, list):
            creation_params['deliverables'] = [
                Deliverable.from_yaml(i) for i in yaml_deliv]
        yaml_params = yaml_desc.get('parameters')
        if isinstance(yaml_params, list):
            creation_params['parameters'] = [
                Parameter.from_yaml(i) for i in yaml_params]
        return cls(**creation_params)


def _get_analytic_schema(schema_path: str) -> Dict:
    file_content = pkgutil.get_data(
        __name__,
        schema_path
    )
    if file_content:
        return yaml.load(file_content, Loader=yaml.Loader)
    else:
        raise FileNotFoundError


ANALYTIC_DESC_SCHEMA = _get_analytic_schema('share/analytic_schema.yaml')


@app.command(name='list')
def list_analytics(
    limit: int = typer.Option(default=100, help='Max number of analytics returned')
):
    """ List the analytics """
    sdk = delairstack_sdk()
    with utils.spinner():
        found_analytics = sdk.analytics.search(
            filter={'is_backoffice': {'$ne': True}},
            return_total=True,
            limit=limit,
            sort={'display_name': 1}
        )
        results = found_analytics.results

    if len(results) > 0:
        table = {
            'Analytic display name': [
                typer.style(r.display_name, fg=typer.colors.GREEN, bold=True)
                for r in results
            ],
            'Name': [r.name for r in results],
            'Identifier': [r.id for r in results]
        }
        print(tabulate(
            table,
            headers='keys',
            tablefmt='pretty',
            colalign=('left', 'left')
        ))

        print()
        print('{}/{} analytics displayed'.format(
            len(results),
            found_analytics.total
        ))

    else:
        print('No analytic found.')


@app.command()
def create(
    description: Path = typer.Option(
        ...,   # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help='Path of the Analytic description (YAML file)'),
    company: str = typer.Option(default=None, help='Company identifier'),
):
    """ Create a new analytic """
    analytic_desc = parse_analytic_yaml(description)
    analytic = Analytic.from_yaml(analytic_desc)
    typer.secho('✓ Analytic description is valid', fg=typer.colors.GREEN)
    sdk = delairstack_sdk()
    found_analytics = sdk.analytics.search(name=analytic.name)
    if found_analytics:
        typer.secho(
            '⚠ {} already exists on {}'.format(
                analytic.name, sdk._connection._base_url
            ),
            fg=typer.colors.YELLOW
        )
        replace_confirm_msg = typer.style(
            'Would you like to replace it?', fg=typer.colors.YELLOW)
        typer.confirm(replace_confirm_msg, abort=True)
        sdk.analytics.delete(analytic=found_analytics[0].id)
    else:
        typer.secho(
            '✓ No analytic with the name {!r} on {!r}'.format(
                analytic.name, sdk._connection._base_url
            ),
            fg=typer.colors.GREEN
        )

    analytic_creation_params = {
        'name': analytic.name,
        'display_name': analytic.display_name,
        'description': analytic.description,
        'docker_image': analytic.docker_image,
    }

    inputs = None
    deliverables = None
    parameters = None

    if analytic.inputs:
        inputs = [i.to_dict() for i in analytic.inputs]
    if analytic.parameters:
        parameters = [p.to_dict() for p in analytic.parameters]
    if analytic.deliverables:
        deliverables = [d.to_dict() for d in analytic.deliverables]

    for sdk_param, obj_val in (('instance_type', analytic.instance_type),
                               ('volume_size', analytic.volume_size),
                               ('inputs', inputs),
                               ('parameters', parameters),
                               ('deliverables', deliverables),
                               ('tags', analytic.tags),
                               ('groups', analytic.groups),
                               ('company', company)):
        if obj_val is not None:
            analytic_creation_params[sdk_param] = obj_val

    created_analytic = sdk.analytics.create(**analytic_creation_params)
    typer.secho('✓ Analytic created successfully', fg=typer.colors.GREEN)
    return created_analytic


def parse_analytic_yaml(analytic_yaml_path: Path) -> Dict:
    with open(analytic_yaml_path) as f:
        analytic = yaml.load(f, Loader=yaml.Loader)
    errors = utils.validate_against_schema(
        analytic,
        json_schema=ANALYTIC_DESC_SCHEMA
    )
    if errors:
        typer.secho(
            '✖ Cannot create the analytic with the supplied YAML file. '
            'Found error(s):',
            fg=typer.colors.RED
        )
        print(errors)
        raise typer.Exit(2)
    else:
        return analytic


@app.command()
def delete(analytic_name: str = typer.Argument(...)):
    """ Delete an analytic """
    sdk = delairstack_sdk()
    with utils.spinner():
        found_analytics = sdk.analytics.search(
            name=analytic_name,
            return_total=True,
            limit=10,
        )
        results = found_analytics.results

    if found_analytics.total == 1:
        if not results[0].external:
            deletion_confirm_msg = typer.style(
                'Analytic {!r} is NOT an external analytic. '
                'Are you sure you want to delete it anyway?'.format(analytic_name),
                fg=typer.colors.YELLOW)
            typer.confirm(deletion_confirm_msg, abort=True)
        try:
            analytic_id = results[0].id
            sdk.analytics.delete(analytic=analytic_id)
        except ResponseError as e:
            typer.secho(
                '✖ Cannot delete the analytic {!r}'.format(analytic_name),
                fg=typer.colors.RED
            )
            typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
            raise typer.Exit(2)

        typer.secho(
            '✓ Analytic {!r} deleted successfully'.format(analytic_name),
            fg=typer.colors.GREEN
        )

    else:
        typer.secho(
            '✖ Cannot find the analytic {!r}'.format(analytic_name),
            fg=typer.colors.RED
        )


if __name__ == "__main__":
    app()
