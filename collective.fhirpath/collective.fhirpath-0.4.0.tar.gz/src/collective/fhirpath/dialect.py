# _*_ coding: utf-8 _*_
from fhirpath.dialects.elasticsearch import ElasticSearchDialect as BaseDialect


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class ElasticSearchDialect(BaseDialect):
    """ """

    def _clean_up(self, body_structure):
        """ """
        # add default sort
        if "_score" not in str(body_structure["sort"]):
            body_structure["sort"].append("_score")
        super(ElasticSearchDialect, self)._clean_up(body_structure)
