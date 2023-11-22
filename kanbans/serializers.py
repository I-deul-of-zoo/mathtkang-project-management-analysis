from rest_framework import serializers
from kanbans.models import Column

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'name', 'order', 'team']