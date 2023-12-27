# serializers.py
from rest_framework import serializers
from files.models import File


class MicrosoftSerializer(serializers.Serializer):
    class Meta:
        model = File
        fields = '__all__'