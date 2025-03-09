from django.db import models
from common.model_mixins import TimestampedModelMixin
from suggestions.managers import SuggestionManager


class Suggestion(TimestampedModelMixin):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # We do not store a ForeignKey to the user, only the anonymized token.
    anon_token = models.CharField(max_length=64, editable=False)

    objects = SuggestionManager()

    def __str__(self):
        return self.title
