from dataclasses import field
from statistics import mode
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'