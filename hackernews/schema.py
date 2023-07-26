import graphene
import graphql_jwt
from links.schema import LinkQuery
from links.schema import VoteQuery
from links.schema import LinkMutation
from links.schema import VoteMutation
from users.schema import UserMutation
from users.schema import UserQuery


class BaseQuery(LinkQuery, VoteQuery, UserQuery, graphene.ObjectType):
    pass


class BaseMutation(LinkMutation, UserMutation, VoteMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=BaseQuery, mutation=BaseMutation)
