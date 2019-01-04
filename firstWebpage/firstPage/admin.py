from django.contrib import admin
from .models import RawMaterial, Products, RawMaterialLog, ProductLog, RawMaterialMapping, MasterLog

admin.site.register(RawMaterial)
admin.site.register(Products)
admin.site.register(RawMaterialLog)
admin.site.register(ProductLog)
admin.site.register(RawMaterialMapping)
admin.site.register(MasterLog)

# Register your models here.
