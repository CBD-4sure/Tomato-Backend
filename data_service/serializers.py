from rest_framework import serializers

from .models import MenuDataTable, RestdataTable

class ResDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestdataTable
        fields = '__all__'

class MenuDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDataTable
        fields = '__all__'