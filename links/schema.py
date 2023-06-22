import graphene
from graphene_django import DjangoObjectType
from links.models import Links


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

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        link = Links(url=url, description=description)
        link.save()

        return CreateLink(id=link.id, url=link.url, description=link.description)


class LinkMutation(graphene.ObjectType):
    create_link = CreateLink.Field()
