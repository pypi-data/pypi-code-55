import graphene

import db.schema


class Query(db.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
