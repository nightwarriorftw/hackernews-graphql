import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from django.db.models import Q
from links.models import Links
from links.models import Vote
from users.schema import UserType


class LinkType(DjangoObjectType):
    class Meta:
        model = Links


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class LinkQuery(graphene.ObjectType):
    links = graphene.List(LinkType, search=graphene.String())
    votes = graphene.List(VoteType)

    def resolve_links(self, info, search=None, **kwargs):
        if search is None:
            return Links.objects.all()
        query = Q(Q(url__icontains=search) | Q(description__icontains=search))
        return Links.objects.filter(query)

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user or None
        link = Links(
            url=url,
            description=description,
            user=user,
        )
        link.save()
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            user=link.user,
        )


class CreateVote(graphene.Mutation):
    link = graphene.Field(LinkType)
    user = graphene.Field(UserType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Anonymous user request not allowed !!")
        link = Links.objects.filter(id=link_id).first()
        if not link:
            raise GraphQLError("Invalid link_id !!")
        vote = Vote(link=link, user=user)
        vote.save()
        return CreateVote(link=vote.link, user=vote.user)


class LinkMutation(graphene.ObjectType):
    create_link = CreateLink.Field()


class VoteMutation(graphene.ObjectType):
    create_vote = CreateVote.Field()
