from showdata.models import Entry
from rest_framework import serializers

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('access_id', 'kingdom', 'specie', 'sequence')


