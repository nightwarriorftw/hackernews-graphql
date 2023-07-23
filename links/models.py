from django.db import models
from common.models import Base
from django.contrib.auth.models import User


class Links(Base):
    """Store information of the links."""

    url = models.URLField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="links",
        on_delete=models.CASCADE,
        help_text="User posted the link",
    )


class Vote(Base):
    """Store information of votes."""

    user = models.ForeignKey(User, related_name="votes", on_delete=models.CASCADE)
    link = models.ForeignKey(Links, related_name="votes", on_delete=models.CASCADE)
