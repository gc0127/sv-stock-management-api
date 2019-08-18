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
    raw_material_type = RawMaterialSerializer()

    class Meta:
        model = RawMaterialMapping
        fields = ('raw_material_type', 'no_of_parts_used')


class ProductLogResponseSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()

    class Meta:
        model = ProductLog
        fields = '__all__'


class RawMaterialLogResponseSerializer(serializers.ModelSerializer):
    raw_material_id = RawMaterialSerializer()

    class Meta:
        model = RawMaterialLog
        fields = '__all__'


class MasterLogResponseSerializer(serializers.ModelSerializer):
    item = ProductSerializer()

    class Meta:
        model = MasterLog
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