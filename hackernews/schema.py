import graphene
import graphql_jwt
from links.schema import LinkQuery
from links.schema import LinkMutation
from users.schema import UserMutation
from users.schema import UserQuery


class BaseQuery(LinkQuery, UserQuery, graphene.ObjectType):
    pass


class BaseMutation(LinkMutation, UserMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=BaseQuery, mutation=BaseMutation)
