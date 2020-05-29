"""
Management command for parsing RDF into the store.
"""
from django.core.management.base import BaseCommand, CommandError
import sys
from django.db import transaction
from rdflib.graph import Graph
from rdflib.term import URIRef, BNode
from rdflib_django import utils


class Command(BaseCommand):
    """
    Command object for importing RDF.
    """

    help = """Imports an RDF resource.

Examples:
    {0} rdf_import my_file.rdf
    {0} rdf_import --format n3 my_file.n3
    {0} rdf_import --context http://zoowizard.eu http://zoowizard.eu/datasource/zoochat/294
    """.format(sys.argv[0])  # noqa: E501

    def add_arguments(self, parser):
        parser.add_argument(
            '--store', '-s', dest='store',
            help='RDF data will be imported into the store with this identifier. If not specified, the default store is used.'  # noqa: E501
        )

        parser.add_argument(
            '--context', '-c', dest='context',
            help='RDF data will be imported into a context with this identifier. If not specified, a new blank context is created.'  # noqa: E501
        )

        parser.add_argument(
            '--format', '-f', dest='format', default='xml',
            help='Format of the RDF data. This option accepts all formats allowed by rdflib. Defaults to xml.'  # noqa: E501
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not args:
            raise CommandError("No file or resource specified.")

        info = options.get('verbosity') >= 2
        store_id = options.get('store')
        context_id = options.get('context')
        source = args[0]

        if info:
            print("Parsing {}".format(source))

        intermediate = Graph()
        try:
            intermediate.parse(source, format=options.get('format'))
        except Exception as e:
            raise CommandError(e)

        if info:
            print("Parsed {} triples".format(len(intermediate)))

        identifier = URIRef(context_id) if context_id else BNode()
        graph = utils.get_named_graph(identifier, store_id=store_id)

        if info:
            print("Storing {} triples".format(len(intermediate)))
        for triple in intermediate:
            graph.add(triple)
        if info:
            print("Done")
