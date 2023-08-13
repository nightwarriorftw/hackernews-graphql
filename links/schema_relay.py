import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from links.models import Links
from links.models import Vote


class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Links
        fields = ["url", "description"]


class LinkNode(DjangoObjectType):
    class Meta:
        model = Links
        interfaces = [graphene.relay.Node]


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = [graphene.relay.Node]


class LinkRelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNode)
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)


class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **kwargs):
        user = info.context.user or None
        link = Links(
            url=kwargs.get("url"),
            description=kwargs.get("description"),
            user=user
        )
        link.save()
        return RelayCreateLink(link=link)


class LinkRelayMutation(graphene.ObjectType):
    relay_create_link = RelayCreateLink.Field()
