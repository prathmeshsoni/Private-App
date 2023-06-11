from rest_framework import serializers
from Private.models import PrivateModel

class PrivateSerialize(serializers.ModelSerializer):
    class Meta:
        model = PrivateModel
        fields = '__all__'
