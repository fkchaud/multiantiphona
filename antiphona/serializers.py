from djongo import models
from rest_framework import (
    fields,
    serializers,
)

from antiphona.models import (
    Antiphona,
    Celebration,
)


# Monkey patch to handle djongo stuff
serializers.HyperlinkedModelSerializer.serializer_field_mapping[models.JSONField] = fields.JSONField


class AntiphonaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Antiphona
        fields = ['url', 'text', 'link']


class CelebrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Celebration
        fields = ['url', 'liturgical_season', 'name', 'antiphonas']
