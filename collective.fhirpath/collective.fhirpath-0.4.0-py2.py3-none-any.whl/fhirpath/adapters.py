# _*_ coding: utf-8 _*_
from .dialect import ElasticSearchDialect
from .engine import ElasticsearchEngine
from .interfaces import IZCatalogFhirSearch
from .zcatalog import zcatalog_fhir_search
from collective.elasticsearch.interfaces import IElasticSearchCatalog
from fhirpath.connectors.factory.es import ElasticsearchConnection
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import IEngine
from fhirpath.interfaces import IFhirSearch
from fhirpath.interfaces import ISearchContext
from fhirpath.interfaces import ISearchContextFactory
from fhirpath.search import fhir_search
from fhirpath.search import SearchContext
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from zope.component import adapter
from zope.interface import implementer


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def create_engine(es_catalog, fhir_release=None):
    """ """
    if fhir_release is None:
        fhir_release = FHIR_VERSION.DEFAULT.value
    if isinstance(fhir_release, str):
        fhir_release = FHIR_VERSION[fhir_release]

    def es_conn_factory(engine):
        return ElasticsearchConnection.from_prepared(engine.es_catalog.connection)

    def es_dialect_factory(engine):
        """ """
        return ElasticSearchDialect(connection=engine.connection)

    engine_ = ElasticsearchEngine(
        es_catalog, fhir_release, es_conn_factory, es_dialect_factory
    )

    return engine_


@implementer(IElasticsearchEngineFactory)
@adapter(IElasticSearchCatalog)
class ElasticsearchEngineFactory:
    """ """

    def __init__(self, es_catalog):
        """ """
        self.es_catalog = es_catalog

    def __call__(self, fhir_release=None):
        """ """
        return create_engine(self.es_catalog, fhir_release=fhir_release)


@implementer(ISearchContextFactory)
@adapter(IEngine)
class SearchContextFactory:
    """ """

    def __init__(self, engine):
        """ """
        self.engine = engine

    def get(self, resource_type, unrestricted=False):
        """ """
        return SearchContext(
            self.engine, resource_type, unrestricted=unrestricted, async_result=False
        )

    def __call__(self, resource_type, unrestricted=False):
        return self.get(resource_type, unrestricted)


@implementer(IFhirSearch)
@adapter(ISearchContext)
class FhirSearch:
    """ """

    def __init__(self, context):
        """ """
        self.context = context

    @at_least_one_of("query_string", "params")
    @mutually_exclusive_parameters("query_string", "params")
    def __call__(self, params=None, query_string=None):
        """ """
        return fhir_search(self.context, params=params, query_string=query_string)


@implementer(IZCatalogFhirSearch)
@adapter(ISearchContext)
class ZCatalogFhirSearch:
    """ """

    def __init__(self, context):
        """ """
        self.context = context

    @at_least_one_of("query_string", "params")
    @mutually_exclusive_parameters("query_string", "params")
    def __call__(self, query_string=None, params=None):
        """ """
        return zcatalog_fhir_search(
            self.context, query_string=query_string, params=params
        )
