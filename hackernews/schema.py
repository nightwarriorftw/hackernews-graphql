import graphene
from links.schema import LinkQuery
from links.schema import LinkMutation
from users.schema import UserMutation
from users.schema import UserQuery


class Query(LinkQuery, UserQuery, graphene.ObjectType):
    pass


class BaseMutation(LinkMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=BaseMutation)
