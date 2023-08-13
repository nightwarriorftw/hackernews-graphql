import graphene
import graphql_jwt
from links.schema import LinkQuery
from links.schema import LinkMutation
from links.schema import VoteMutation
from links.schema_relay import LinkRelayQuery
from links.schema_relay import LinkRelayMutation
from users.schema import UserMutation
from users.schema import UserQuery


class BaseQuery(LinkQuery, UserQuery, LinkRelayQuery, graphene.ObjectType):
    pass


class BaseMutation(
    LinkMutation, UserMutation, VoteMutation, LinkRelayMutation, graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=BaseQuery, mutation=BaseMutation)
