import argparse
import kaistack
import logging
import yaml
from kaistack.components.component_store import ComponentStore
from kaistack.components.kubeflow_converter import create_workflow_template_from_component_spec

logger = logging.getLogger("Component Importer")

def convert_component(path):
    wf = create_workflow_template_from_component_spec(path)
    return wf


def import_component(args):
    spec = ''
    if not args.convert:
        # Sniff the file
        with open(args.path, 'r') as f:
            spec = f.read()
            args.convert = not spec.startswith("apiVersion")
    if args.convert:
        logger.info("Convert the spec")
        spec = convert_component(args.path)

    if not args.apibase:
        args.apibase = args.service
    logger.info("Initialize component store. service:[%s] api_base [%s]", args.service, args.apibase)
    store = ComponentStore(args.service, args.apibase)
    try:
        store.create_component(yaml.dump(spec), args.name)
        logger.info("Create component successfully")
    except kaistack.clients.openapi_clients.pipelinecomponents.exceptions.ApiException:
        store.update_component(yaml.dump(spec), args.name)
        logger.info("Update component successfully")


def main():
    parser = argparse.ArgumentParser(description='Import a kubeflow component')
    parser.add_argument('--path', required=True, help='The input file path')
    parser.add_argument('--service', help='The service name')
    parser.add_argument('--apibase', help='The api endpoint base. Only set if it is different from the service')
    parser.add_argument('--name', help="The component name. If not set, it will by default use the name in the yaml")
    parser.add_argument('--convert', action="store_true",
                        help='If configured, will convert from kfp component spec. If not set, the progam will detect')

    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    args = parser.parse_args()
    import_component(args)


if __name__ == '__main__':
    main()
