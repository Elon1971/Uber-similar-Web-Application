from rest_framework import serializers
from .models import AP

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = AP
        fields = '__all__'

