import graphene
from graphene_django import DjangoObjectType
from links.models import Links


class LinkType(DjangoObjectType):
    class Meta:
        model = Links


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Links.objects.all()
