import graphene
from graphene_django import DjangoObjectType
from links.models import Links
from users.schema import UserType


class LinkType(DjangoObjectType):
    class Meta:
        model = Links


class LinkQuery(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Links.objects.all()


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


class LinkMutation(graphene.ObjectType):
    create_link = CreateLink.Field()
