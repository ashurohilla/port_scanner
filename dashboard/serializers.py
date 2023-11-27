# serializers.py
from rest_framework import serializers

class PortScannerSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=100)
