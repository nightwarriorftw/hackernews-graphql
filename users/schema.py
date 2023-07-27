import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")
        return user

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, email, username, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
