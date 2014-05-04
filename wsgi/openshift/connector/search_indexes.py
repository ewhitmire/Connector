import datetime
from haystack import indexes
from connector.models import *


class SkillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    member = indexes.CharField(model_attr='member')
    category = indexes.CharField(model_attr='category', faceted=True)

    tags = indexes.MultiValueField(indexed=True, faceted=True, stored=True)

    def get_model(self):
        return Skill

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
        
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class OfferIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    member = indexes.CharField(model_attr='member')
    category = indexes.CharField(model_attr='category', faceted=True)
    title = indexes.CharField(model_attr='title')

    tags = indexes.MultiValueField(indexed=True, faceted=True, stored=True)

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    organization = indexes.CharField(model_attr='organization')

    def get_model(self):
        return Offer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()