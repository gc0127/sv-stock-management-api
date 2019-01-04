from rest_framework import serializers
from .models import RawMaterial, Products, ProductLog, RawMaterialLog, RawMaterialMapping, MasterLog, ProductHistory


class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class RawMaterialMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialMapping
        fields = '__all__'


class ProductLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLog
        fields = '__all__'


class RawMaterialLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialLog
        fields = '__all__'


class MasterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterLog
        fields = '__all__'


class ProductLogNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLog
        fields = ('product_id', 'quantity', 'date', 'time', 'product_name')


class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHistory
        fields = ('log_id', 'product_id', 'quantity', 'date', 'time', 'product_name')