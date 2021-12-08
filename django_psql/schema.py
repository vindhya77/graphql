import graphene
from graphene_django import DjangoObjectType
from app1.graphql.mutations import Mutations
from app1.graphql.queries import Query


schema = graphene.Schema(query=Query, auto_camelcase=False, mutation=Mutations)

